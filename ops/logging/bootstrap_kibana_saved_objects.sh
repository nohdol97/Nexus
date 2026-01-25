#!/usr/bin/env bash
set -euo pipefail

KIBANA_URL=${KIBANA_URL:-http://localhost:5601}
DATA_VIEW_TITLE=${DATA_VIEW_TITLE:-gateway-logs-*}
DATA_VIEW_ID=${DATA_VIEW_ID:-}
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

fetch_data_view_id() {
  curl -s "${KIBANA_URL}/api/saved_objects/_find?type=index-pattern&search=${DATA_VIEW_TITLE}&search_fields=title" \
    -H 'kbn-xsrf: true' | python3 -c 'import json,sys; data=json.load(sys.stdin); items=data.get("saved_objects",[]); print(items[0].get("id","") if items else "")'
}

# Ensure data view exists
if [[ -z "${DATA_VIEW_ID}" ]]; then
  DATA_VIEW_ID=$(fetch_data_view_id)
  if [[ -z "${DATA_VIEW_ID}" ]]; then
    "${SCRIPT_DIR}/bootstrap_kibana.sh" >/dev/null
    DATA_VIEW_ID=$(fetch_data_view_id)
  fi
fi

if [[ -z "${DATA_VIEW_ID}" ]]; then
  echo "Failed to find or create data view: ${DATA_VIEW_TITLE}" >&2
  exit 1
fi

create_saved_query() {
  local id="$1"
  local title="$2"
  local query="$3"
  local description="$4"

  curl -s -X POST "${KIBANA_URL}/api/saved_objects/query/${id}?overwrite=true" \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -d "{\"attributes\":{\"title\":\"${title}\",\"description\":\"${description}\",\"query\":{\"language\":\"kuery\",\"query\":\"${query}\"},\"filters\":[]}}" \
    >/dev/null

  echo "Saved query created: ${title}"
}

create_saved_query "gateway-errors" "Gateway Errors" "status >= 500" "5xx 에러 로그"
create_saved_query "gateway-slow" "Gateway Slow Requests" "duration_ms > 1000" "1초 초과 요청"
create_saved_query "gateway-chat" "Gateway Chat Completions" "path : \\\"/v1/chat/completions\\\"" "채팅 엔드포인트"
create_saved_query "gateway-rate-limit" "Gateway Rate Limit" "status = 429" "레이트 리밋 응답"

# Import dashboard + saved search
TMP_FILE=$(mktemp)
sed "s/__DATA_VIEW_ID__/${DATA_VIEW_ID}/g" "${SCRIPT_DIR}/kibana_saved_objects.ndjson" > "${TMP_FILE}"

curl -s -X POST "${KIBANA_URL}/api/saved_objects/_import?overwrite=true" \
  -H 'kbn-xsrf: true' \
  -F file=@"${TMP_FILE}" \
  >/dev/null

rm -f "${TMP_FILE}"

echo "Saved objects imported (dashboard + search)."
