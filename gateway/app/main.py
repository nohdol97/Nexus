from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

from app.core.circuit_breaker import CircuitBreaker
from app.core.config import settings
from app.core.rate_limiter import RateLimitExceeded, RateLimiter
from app.core.security import require_api_key
from app.schemas import ChatCompletionRequest
from app.services.proxy import ProxyClient, UpstreamError
from app.services.router import RouteSelector

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.proxy = ProxyClient(timeout_seconds=settings.request_timeout_seconds)
    try:
        yield
    finally:
        await app.state.proxy.close()


app = FastAPI(title="Nexus Gateway", version="0.1.0", lifespan=lifespan)

rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_per_minute,
    window_seconds=settings.rate_limit_window_seconds,
)
route_selector = RouteSelector()

circuit_breakers: dict[str, CircuitBreaker] = {
    upstream.name: CircuitBreaker(
        max_failures=settings.circuit_breaker_max_failures,
        reset_timeout_seconds=settings.circuit_breaker_reset_seconds,
    )
    for upstream in route_selector.all()
}


@app.middleware("http")
async def add_request_ids(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    trace_id = request.headers.get("x-trace-id") or request_id
    request.state.request_id = request_id
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-trace-id"] = trace_id
    return response


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": str(exc)},
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/circuit-breakers")
async def circuit_status() -> dict[str, Any]:
    return {name: asdict(breaker.snapshot()) for name, breaker in circuit_breakers.items()}


@app.post("/v1/chat/completions")
async def chat_completions(
    payload: ChatCompletionRequest,
    request: Request,
    response: Response,
    api_key: str = Depends(require_api_key),
) -> dict[str, Any]:
    snapshot = rate_limiter.check(api_key)
    response.headers["x-ratelimit-remaining"] = str(snapshot.remaining)
    response.headers["x-ratelimit-reset"] = str(snapshot.reset_seconds)

    upstream = route_selector.select(payload.model)
    if upstream is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No upstream configured for requested model",
        )

    breaker = circuit_breakers.setdefault(
        upstream.name,
        CircuitBreaker(
            max_failures=settings.circuit_breaker_max_failures,
            reset_timeout_seconds=settings.circuit_breaker_reset_seconds,
        ),
    )

    if not breaker.allow_request():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Upstream circuit open",
        )

    proxy: ProxyClient = request.app.state.proxy
    forward_headers = {
        "x-request-id": request.state.request_id,
        "x-trace-id": request.state.trace_id,
    }

    try:
        result = await proxy.forward(upstream, "/v1/chat/completions", payload, forward_headers)
    except UpstreamError as exc:
        breaker.record_failure()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    breaker.record_success()
    response.headers["x-upstream"] = upstream.name
    return result
