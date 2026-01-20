from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "gateway_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
IN_FLIGHT = Gauge(
    "gateway_in_flight_requests",
    "In-flight HTTP requests",
)
UPSTREAM_REQUESTS = Counter(
    "gateway_upstream_requests_total",
    "Upstream requests",
    ["upstream", "status"],
)
UPSTREAM_LATENCY = Histogram(
    "gateway_upstream_latency_seconds",
    "Upstream latency in seconds",
    ["upstream"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
RATE_LIMITED = Counter(
    "gateway_rate_limited_total",
    "Rate limited requests",
)
CIRCUIT_OPEN = Counter(
    "gateway_circuit_open_total",
    "Requests blocked by circuit breaker",
    ["upstream"],
)
FALLBACK_USED = Counter(
    "gateway_fallback_used_total",
    "Fallback models used",
    ["from_model", "to_model"],
)
