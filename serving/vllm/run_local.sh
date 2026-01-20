#!/usr/bin/env bash
set -euo pipefail

MODEL_ID=${MODEL_ID:-"meta-llama/Meta-Llama-3-8B-Instruct"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8001"}

python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_ID" \
  --host "$HOST" \
  --port "$PORT"
