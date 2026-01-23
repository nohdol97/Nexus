#!/bin/sh
set -e

echo "[step] model registration"

MODEL_NAME="${MODEL_NAME:-nexus-llm}"
MODEL_VERSION="${MODEL_VERSION:-1}"
MODEL_URI="models:/${MODEL_NAME}/${MODEL_VERSION}"

MODEL_URI_FILE="${MODEL_URI_FILE:-/workspace/model_uri.txt}"
echo "$MODEL_URI" > "$MODEL_URI_FILE"
echo "model_uri=$MODEL_URI"
