#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-"http://localhost:8000"}
API_KEY=${API_KEY:-"dev-key"}
REQUEST_ID=${REQUEST_ID:-"req-$(date +%s)"}
TRACE_ID=${TRACE_ID:-"trace-$(date +%s)"}

curl -s -X POST "${BASE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${API_KEY}" \
  -H "X-Request-Id: ${REQUEST_ID}" \
  -H "X-Trace-Id: ${TRACE_ID}" \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
