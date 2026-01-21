import jwt
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
    settings.api_key_policies = ""
    settings.route_policies = ""
    settings.jwt_secret = None
    settings.jwt_public_key = None
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
    settings.api_key_policies = ""
    settings.route_policies = ""
    settings.jwt_secret = None
    settings.jwt_public_key = None
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
    settings.api_key_policies = ""
    settings.route_policies = ""
    settings.jwt_secret = None
    settings.jwt_public_key = None
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


def test_metrics_endpoint() -> None:
    settings.upstreams = "mock=mock://local"
    settings.default_upstream = "mock"
    settings.fallbacks = ""
    settings.api_key_policies = ""
    settings.route_policies = ""
    settings.jwt_secret = None
    settings.jwt_public_key = None
    _reset_state()
    with TestClient(main.app) as client:
        response = client.get("/metrics")
    assert response.status_code == 200
    assert "gateway_requests_total" in response.text


def test_route_policy_canary() -> None:
    settings.upstreams = "primary=mock://local;canary=mock://local"
    settings.default_upstream = None
    settings.fallbacks = ""
    settings.route_policies = (
        '{"chat": {"strategy":"canary","primary":"primary","canary":"canary","percent":100}}'
    )
    settings.api_key_policies = ""
    settings.jwt_secret = None
    settings.jwt_public_key = None
    _reset_state()
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/chat/completions",
            json={"model": "chat", "messages": [{"role": "user", "content": "hi"}]},
            headers={"X-API-Key": "dev-key", "X-Request-Id": "req-1"},
        )
    assert response.status_code == 200
    assert response.headers.get("x-upstream") == "canary"


def test_jwt_auth_allowed_model() -> None:
    settings.upstreams = "mock=mock://local"
    settings.default_upstream = "mock"
    settings.fallbacks = ""
    settings.route_policies = ""
    settings.api_key_policies = ""
    settings.jwt_secret = "secret"
    settings.jwt_algorithms = "HS256"
    settings.jwt_public_key = None
    token = jwt.encode({"sub": "user-1", "models": ["mock"]}, "secret", algorithm="HS256")
    _reset_state()
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/chat/completions",
            json={"model": "mock", "messages": [{"role": "user", "content": "hi"}]},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 200


def test_jwt_auth_forbidden_model() -> None:
    settings.upstreams = "mock=mock://local"
    settings.default_upstream = "mock"
    settings.fallbacks = ""
    settings.route_policies = ""
    settings.api_key_policies = ""
    settings.jwt_secret = "secret"
    settings.jwt_algorithms = "HS256"
    settings.jwt_public_key = None
    token = jwt.encode({"sub": "user-1", "models": ["other"]}, "secret", algorithm="HS256")
    _reset_state()
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/chat/completions",
            json={"model": "mock", "messages": [{"role": "user", "content": "hi"}]},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 403
