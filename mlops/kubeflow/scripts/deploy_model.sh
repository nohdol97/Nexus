#!/bin/sh
set -e

echo "[step] deployment"

MODEL_URI_FILE="${MODEL_URI_FILE:-/workspace/model_uri.txt}"
if [ -f "$MODEL_URI_FILE" ]; then
  MODEL_URI="$(cat "$MODEL_URI_FILE")"
else
  MODEL_URI="${MODEL_URI:-models:/nexus-llm/1}"
fi

echo "deploying $MODEL_URI"
