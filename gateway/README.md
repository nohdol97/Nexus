# Nexus Gateway

Minimal FastAPI gateway skeleton with auth, routing, rate limiting, and circuit breaker.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## Docker quick start

```bash
docker compose up --build
```

- Gateway: http://localhost:8000
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default: admin / admin)
  - Dashboard: Nexus Gateway (auto-provisioned)

## Docker with vLLM upstream

This requires a GPU host with the NVIDIA container runtime.

```bash
MODEL_ID=meta-llama/Meta-Llama-3-8B-Instruct \\
  docker compose -f docker-compose.yml -f docker-compose.vllm.yml up --build
```

## Configuration

All settings use the `GATEWAY_` prefix.

- `GATEWAY_API_KEYS` (comma-separated, default: `dev-key`)
- `GATEWAY_RATE_LIMIT_PER_MINUTE` (default: `60`)
- `GATEWAY_CIRCUIT_BREAKER_MAX_FAILURES` (default: `5`)
- `GATEWAY_CIRCUIT_BREAKER_RESET_SECONDS` (default: `30`)
- `GATEWAY_REQUEST_TIMEOUT_SECONDS` (default: `10`)
- `GATEWAY_UPSTREAMS` (example: `llama=http://localhost:8001;mock=mock://local;gpt-4o-mini=litellm://gpt-4o-mini`)
- `GATEWAY_DEFAULT_UPSTREAM` (optional upstream name)
- `GATEWAY_FALLBACKS` (example: `llama=gpt-4o-mini,mock`)
- `GATEWAY_REDIS_URL` (optional; enables Redis-backed rate limiting)
- `GATEWAY_API_KEY_POLICIES` (optional JSON for per-key rules)
- `GATEWAY_ROUTE_POLICIES` (optional JSON for weighted/canary routing)
- `GATEWAY_JWT_SECRET` / `GATEWAY_JWT_PUBLIC_KEY` (optional; enable JWT validation)
- `GATEWAY_JWT_ALGORITHMS` (default: `HS256`)
- `GATEWAY_JWT_ISSUER` / `GATEWAY_JWT_AUDIENCE` (optional)

## Observability

- Metrics: `GET /metrics` (Prometheus format)
- Logs: JSON structured logs on stdout

## LiteLLM upstreams

Use `litellm://` to route to external providers via LiteLLM. The model name can be part of the URL:

```
GATEWAY_UPSTREAMS="gpt-4o-mini=litellm://gpt-4o-mini"
```

Fallback example:

```
GATEWAY_UPSTREAMS="llama=http://localhost:8001;gpt-4o-mini=litellm://gpt-4o-mini"
GATEWAY_FALLBACKS="llama=gpt-4o-mini"
```

## Routing policies (weighted/canary)

Route policies are JSON that map a requested model to upstream targets.
Targets must match upstream names defined in `GATEWAY_UPSTREAMS`.

```bash
GATEWAY_ROUTE_POLICIES='{
  "chat": {
    "strategy": "weighted",
    "targets": [{"name":"primary","weight":90},{"name":"canary","weight":10}]
  }
}'
```

Canary policy example:

```bash
GATEWAY_ROUTE_POLICIES='{
  "chat": {"strategy":"canary","primary":"primary","canary":"canary","percent":5}
}'
```

## API key policies

```bash
GATEWAY_API_KEY_POLICIES='{
  "dev-key": {"allowed_models":["chat"], "rate_limit_per_minute": 30}
}'
```

## JWT

```bash
GATEWAY_JWT_SECRET="my-secret"
GATEWAY_JWT_ALGORITHMS="HS256"
```

## Example request

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "X-API-Key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```
