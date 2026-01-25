#!/usr/bin/env bash
set -euo pipefail

ALERTMANAGER_URL=${ALERTMANAGER_URL:-http://localhost:9093}

payload='[
  {
    "labels": {
      "alertname": "NexusTestAlert",
      "severity": "info",
      "service": "gateway"
    },
    "annotations": {
      "summary": "Test alert from Nexus",
      "description": "This is a local test alert to verify Alertmanager routing."
    },
    "startsAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
  }
]'

curl -s -X POST "${ALERTMANAGER_URL}/api/v1/alerts" \
  -H 'Content-Type: application/json' \
  -d "${payload}"

echo "Test alert sent to ${ALERTMANAGER_URL}"
