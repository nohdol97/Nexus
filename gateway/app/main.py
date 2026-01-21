from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.core.circuit_breaker import CircuitBreaker
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.metrics import (
    CIRCUIT_OPEN,
    FALLBACK_USED,
    IN_FLIGHT,
    RATE_LIMITED,
    REQUEST_COUNT,
    REQUEST_LATENCY,
    UPSTREAM_LATENCY,
    UPSTREAM_REQUESTS,
)
from app.core.rate_limiter import (
    RateLimitBackendError,
    RateLimitExceeded,
    RateLimiter,
    RateLimiterBase,
    RedisRateLimiter,
)
from app.core.security import AuthContext, require_auth
from app.schemas import ChatCompletionRequest
from app.services.proxy import ProxyClient, UpstreamError
from app.services.router import RouteSelector

logger = configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.proxy = ProxyClient(timeout_seconds=settings.request_timeout_seconds)
    try:
        yield
    finally:
        await app.state.proxy.close()
        await rate_limiter.close()


app = FastAPI(title="Nexus Gateway", version="0.1.0", lifespan=lifespan)

def _build_rate_limiter() -> RateLimiterBase:
    if settings.redis_url:
        return RedisRateLimiter(
            redis_url=settings.redis_url,
            max_requests=settings.rate_limit_per_minute,
            window_seconds=settings.rate_limit_window_seconds,
        )
    return RateLimiter(
        max_requests=settings.rate_limit_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )


rate_limiter = _build_rate_limiter()
route_selector = RouteSelector()

circuit_breakers: dict[str, CircuitBreaker] = {
    upstream.name: CircuitBreaker(
        max_failures=settings.circuit_breaker_max_failures,
        reset_timeout_seconds=settings.circuit_breaker_reset_seconds,
    )
    for upstream in route_selector.all()
}


def _log_extra(request: Request, status_code: int, duration_ms: int) -> dict[str, Any]:
    extra = {
        "event": "request",
        "request_id": getattr(request.state, "request_id", None),
        "trace_id": getattr(request.state, "trace_id", None),
        "method": request.method,
        "path": request.url.path,
        "status": status_code,
        "duration_ms": duration_ms,
        "upstream": getattr(request.state, "upstream", None),
        "fallback_model": getattr(request.state, "fallback_model", None),
        "rate_limited": getattr(request.state, "rate_limited", None),
        "client_ip": request.client.host if request.client else None,
    }
    return {key: value for key, value in extra.items() if value is not None}


@app.middleware("http")
async def add_request_ids(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    trace_id = request.headers.get("x-trace-id") or request_id
    request.state.request_id = request_id
    request.state.trace_id = trace_id
    start = time.perf_counter()
    IN_FLIGHT.inc()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = int((time.perf_counter() - start) * 1000)
        REQUEST_COUNT.labels(request.method, request.url.path, "500").inc()
        REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration_ms / 1000)
        logger.exception("request_failed", extra=_log_extra(request, 500, duration_ms))
        raise
    finally:
        IN_FLIGHT.dec()
    duration_ms = int((time.perf_counter() - start) * 1000)
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(duration_ms / 1000)
    logger.info("request_completed", extra=_log_extra(request, response.status_code, duration_ms))
    response.headers["x-request-id"] = request_id
    response.headers["x-trace-id"] = trace_id
    return response


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    RATE_LIMITED.inc()
    request.state.rate_limited = True
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": str(exc)},
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/v1/circuit-breakers")
async def circuit_status() -> dict[str, Any]:
    return {name: asdict(breaker.snapshot()) for name, breaker in circuit_breakers.items()}


@app.post("/v1/chat/completions")
async def chat_completions(
    payload: ChatCompletionRequest,
    request: Request,
    response: Response,
    auth: AuthContext = Depends(require_auth),
) -> dict[str, Any]:
    try:
        snapshot = await rate_limiter.check(
            auth.rate_limit_key, limit_override=auth.rate_limit_per_minute
        )
    except RateLimitBackendError as exc:
        logger.warning(
            "rate_limit_backend_error",
            extra={
                "event": "rate_limit_backend_error",
                "error": str(exc),
                "request_id": request.state.request_id,
                "trace_id": request.state.trace_id,
            },
        )
    else:
        response.headers["x-ratelimit-remaining"] = str(snapshot.remaining)
        response.headers["x-ratelimit-reset"] = str(snapshot.reset_seconds)

    proxy: ProxyClient = request.app.state.proxy
    forward_headers = {
        "x-request-id": request.state.request_id,
        "x-trace-id": request.state.trace_id,
    }
    fallback_map = settings.fallback_map()
    candidates = [payload.model] + fallback_map.get(payload.model, [])
    allowed_models = auth.allowed_models
    errors: list[str] = []
    seen: set[str] = set()

    for model_name in candidates:
        if model_name in seen:
            continue
        seen.add(model_name)
        if allowed_models is not None and model_name not in allowed_models:
            errors.append(f"{model_name}: forbidden")
            continue

        upstream = route_selector.select(model_name, request.state.request_id)
        if upstream is None:
            errors.append(f"{model_name}: no upstream")
            continue
        request.state.upstream = upstream.name

        breaker = circuit_breakers.setdefault(
            upstream.name,
            CircuitBreaker(
                max_failures=settings.circuit_breaker_max_failures,
                reset_timeout_seconds=settings.circuit_breaker_reset_seconds,
            ),
        )

        if not breaker.allow_request():
            CIRCUIT_OPEN.labels(upstream.name).inc()
            errors.append(f"{model_name}: circuit open")
            continue

        candidate_payload = payload
        if model_name != payload.model:
            candidate_payload = payload.model_copy(update={"model": model_name})

        try:
            upstream_start = time.perf_counter()
            result = await proxy.forward(
                upstream,
                "/v1/chat/completions",
                candidate_payload,
                forward_headers,
            )
        except UpstreamError as exc:
            breaker.record_failure()
            UPSTREAM_REQUESTS.labels(upstream.name, "error").inc()
            UPSTREAM_LATENCY.labels(upstream.name).observe(
                (time.perf_counter() - upstream_start)
            )
            logger.warning(
                "upstream_error",
                extra={
                    "event": "upstream_error",
                    "upstream": upstream.name,
                    "error": str(exc),
                    "request_id": request.state.request_id,
                    "trace_id": request.state.trace_id,
                },
            )
            errors.append(f"{model_name}: {exc}")
            continue

        breaker.record_success()
        UPSTREAM_REQUESTS.labels(upstream.name, "success").inc()
        UPSTREAM_LATENCY.labels(upstream.name).observe(
            (time.perf_counter() - upstream_start)
        )
        response.headers["x-upstream"] = upstream.name
        if model_name != payload.model:
            response.headers["x-fallback-model"] = model_name
            request.state.fallback_model = model_name
            FALLBACK_USED.labels(payload.model, model_name).inc()
        return result

    if errors and all("no upstream" in error for error in errors):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No upstream configured for requested model",
        )
    if errors and all("forbidden" in error for error in errors):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Model access denied",
        )
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="; ".join(errors) if errors else "Upstream unavailable",
    )
