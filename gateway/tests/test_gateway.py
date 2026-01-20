from fastapi.testclient import TestClient

import app.main as main
from app.core.circuit_breaker import CircuitBreaker
from app.core.config import settings
from app.core.rate_limiter import RateLimiter
from app.services.router import RouteSelector


def _reset_state() -> None:
    main.route_selector = RouteSelector()
    main.rate_limiter = RateLimiter(
        max_requests=settings.rate_limit_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )
    main.circuit_breakers = {
        upstream.name: CircuitBreaker(
            max_failures=settings.circuit_breaker_max_failures,
            reset_timeout_seconds=settings.circuit_breaker_reset_seconds,
        )
        for upstream in main.route_selector.all()
    }


def test_missing_api_key() -> None:
    settings.upstreams = "mock=mock://local"
    settings.default_upstream = "mock"
    settings.fallbacks = ""
    _reset_state()
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/chat/completions",
            json={"model": "mock", "messages": [{"role": "user", "content": "hi"}]},
        )
    assert response.status_code == 401


def test_chat_completion_mock() -> None:
    settings.upstreams = "mock=mock://local"
    settings.default_upstream = "mock"
    settings.fallbacks = ""
    _reset_state()
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/chat/completions",
            json={"model": "mock", "messages": [{"role": "user", "content": "hi"}]},
            headers={"X-API-Key": "dev-key"},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["model"] == "mock"
    assert payload["choices"][0]["message"]["role"] == "assistant"


def test_fallback_on_failure() -> None:
    settings.upstreams = "primary=mock://fail;fallback=mock://local"
    settings.default_upstream = None
    settings.fallbacks = "primary=fallback"
    _reset_state()
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/chat/completions",
            json={"model": "primary", "messages": [{"role": "user", "content": "hi"}]},
            headers={"X-API-Key": "dev-key"},
        )
    assert response.status_code == 200
    assert response.headers.get("x-upstream") == "fallback"
    assert response.headers.get("x-fallback-model") == "fallback"
