# Nexus Gateway

Minimal FastAPI gateway skeleton with auth, routing, rate limiting, and circuit breaker.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## Configuration

All settings use the `GATEWAY_` prefix.

- `GATEWAY_API_KEYS` (comma-separated, default: `dev-key`)
- `GATEWAY_RATE_LIMIT_PER_MINUTE` (default: `60`)
- `GATEWAY_CIRCUIT_BREAKER_MAX_FAILURES` (default: `5`)
- `GATEWAY_CIRCUIT_BREAKER_RESET_SECONDS` (default: `30`)
- `GATEWAY_REQUEST_TIMEOUT_SECONDS` (default: `10`)
- `GATEWAY_UPSTREAMS` (example: `llama=http://localhost:8001;mock=mock://local`)
- `GATEWAY_DEFAULT_UPSTREAM` (optional upstream name)

## Example request

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "X-API-Key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```
