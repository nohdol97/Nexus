#!/usr/bin/env bash
set -euo pipefail

KIBANA_URL=${KIBANA_URL:-http://localhost:5601}
DATA_VIEW_TITLE=${DATA_VIEW_TITLE:-gateway-logs-*}
DATA_VIEW_NAME=${DATA_VIEW_NAME:-gateway-logs}
TIME_FIELD=${TIME_FIELD:-timestamp}

existing=$(curl -s "${KIBANA_URL}/api/saved_objects/_find?type=index-pattern&search=${DATA_VIEW_TITLE}&search_fields=title" \
  -H 'kbn-xsrf: true' | tr -d '\n')

if echo "${existing}" | grep -Fq "${DATA_VIEW_TITLE}"; then
  echo "Data view already exists: ${DATA_VIEW_TITLE}"
  exit 0
fi

curl -s -X POST "${KIBANA_URL}/api/data_views/data_view" \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d "{\"data_view\":{\"title\":\"${DATA_VIEW_TITLE}\",\"name\":\"${DATA_VIEW_NAME}\",\"timeFieldName\":\"${TIME_FIELD}\"}}"

echo

echo "Created data view: ${DATA_VIEW_TITLE}"
