#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${SGLANG_IMAGE:-}" ]]; then
  echo "SGLANG_IMAGE is required (e.g. your SGLang image)" >&2
  exit 1
fi

SGLANG_COMMAND=${SGLANG_COMMAND:-}
SGLANG_HEALTH_URL=${SGLANG_HEALTH_URL:-"http://localhost:8002/health"}
SGLANG_HEALTH_FALLBACK_URL=${SGLANG_HEALTH_FALLBACK_URL:-"http://localhost:8002/v1/models"}
SGLANG_HEALTH_TIMEOUT=${SGLANG_HEALTH_TIMEOUT:-30}

export SGLANG_IMAGE
export SGLANG_COMMAND

# Start services

docker compose -f docker-compose.yml -f docker-compose.sglang.yml up -d

# Healthcheck loop

echo "Checking SGLang health..."
for _ in $(seq 1 "${SGLANG_HEALTH_TIMEOUT}"); do
  if curl -fsS "${SGLANG_HEALTH_URL}" >/dev/null; then
    echo "SGLang healthy: ${SGLANG_HEALTH_URL}"
    exit 0
  fi
  if curl -fsS "${SGLANG_HEALTH_FALLBACK_URL}" >/dev/null; then
    echo "SGLang healthy: ${SGLANG_HEALTH_FALLBACK_URL}"
    exit 0
  fi
  sleep 1
done

echo "SGLang healthcheck failed" >&2
exit 1
