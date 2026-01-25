#!/usr/bin/env bash
set -euo pipefail

PROTO_DIR="contracts"
PROTO_FILE="${PROTO_DIR}/nexus_inference.proto"

python3 -m grpc_tools.protoc \
  -I "${PROTO_DIR}" \
  --python_out=gateway/app/grpc/gen \
  --grpc_python_out=gateway/app/grpc/gen \
  "${PROTO_FILE}"

python3 -m grpc_tools.protoc \
  -I "${PROTO_DIR}" \
  --python_out=serving/mock-worker/grpc_gen \
  --grpc_python_out=serving/mock-worker/grpc_gen \
  "${PROTO_FILE}"

echo "gRPC code generated."
