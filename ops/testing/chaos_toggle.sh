#!/usr/bin/env bash
set -euo pipefail

# Helper for starting mock worker with chaos knobs.
# Example:
#   WORKER_DELAY_MS=500 WORKER_FAIL_RATE=0.1 ./ops/testing/chaos_toggle.sh

WORKER_PORT=${WORKER_PORT:-8001}
WORKER_MODEL_NAME=${WORKER_MODEL_NAME:-mock-worker}

export WORKER_MODEL_NAME

(
  cd serving/mock-worker
  python3 -m uvicorn app:app \
    --host 0.0.0.0 \
    --port "${WORKER_PORT}" \
    --log-level info
)
