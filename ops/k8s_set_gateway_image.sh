#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${IMAGE_REPO:-}" ]]; then
  echo "IMAGE_REPO is required. Example: IMAGE_REPO=ghcr.io/your-org/nexus-gateway" >&2
  exit 1
fi

IMAGE_TAG=${IMAGE_TAG:-latest}
IMAGE_REF="${IMAGE_REPO}:${IMAGE_TAG}"
NAMESPACE=${NAMESPACE:-nexus}

kubectl -n "${NAMESPACE}" set image deployment/nexus-gateway gateway="${IMAGE_REF}"

printf "Updated deployment/nexus-gateway to %s\n" "${IMAGE_REF}"
