#!/usr/bin/env bash
set -euo pipefail

KIBANA_URL=${KIBANA_URL:-http://localhost:5601}
DATA_VIEW_ID=${DATA_VIEW_ID:-}

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

create_dashboard() {
  local id="$1"
  local title="$2"
  local description="$3"

  local search_source
  if [[ -n "${DATA_VIEW_ID}" ]]; then
    search_source="{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[],\"index\":\"${DATA_VIEW_ID}\"}"
  else
    search_source="{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
  fi

  curl -s -X POST "${KIBANA_URL}/api/saved_objects/dashboard/${id}?overwrite=true" \
    -H 'kbn-xsrf: true' \
    -H 'Content-Type: application/json' \
    -d "{\"attributes\":{\"title\":\"${title}\",\"description\":\"${description}\",\"panelsJSON\":\"[]\",\"optionsJSON\":\"{}\",\"timeRestore\":false,\"kibanaSavedObjectMeta\":{\"searchSourceJSON\":\"${search_source//"/\\\"}\"}}}" \
    >/dev/null

  echo "Dashboard created: ${title}"
}

create_saved_query "gateway-errors" "Gateway Errors" "status >= 500" "5xx 에러 로그"
create_saved_query "gateway-slow" "Gateway Slow Requests" "duration_ms > 1000" "1초 초과 요청"
create_saved_query "gateway-chat" "Gateway Chat Completions" "path : \"/v1/chat/completions\"" "채팅 엔드포인트"
create_saved_query "gateway-rate-limit" "Gateway Rate Limit" "status = 429" "레이트 리밋 응답"

create_dashboard "gateway-dashboard" "Gateway Logs Dashboard" "로그 기반 대시보드 템플릿"
