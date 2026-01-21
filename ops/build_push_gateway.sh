#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${IMAGE_REPO:-}" ]]; then
  echo "IMAGE_REPO is required. Example: IMAGE_REPO=ghcr.io/your-org/nexus-gateway" >&2
  exit 1
fi

IMAGE_TAG=${IMAGE_TAG:-latest}
IMAGE_REF="${IMAGE_REPO}:${IMAGE_TAG}"

# Build and push the gateway image
docker build -t "${IMAGE_REF}" -f gateway/Dockerfile gateway

docker push "${IMAGE_REF}"

printf "Pushed %s\n" "${IMAGE_REF}"
