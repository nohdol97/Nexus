# Kibana Saved Objects 자동 생성

이 문서는 Kibana Saved Objects(저장 객체)를 자동으로 생성하는 스크립트 설명입니다.

## 대상
- Saved Query (KQL)
- Saved Search (Discover)
- Dashboard (기본 패널 포함)

## 스크립트
- `ops/logging/bootstrap_kibana_saved_objects.sh`

## 사용 방법
```bash
# 기본 실행
./ops/logging/bootstrap_kibana_saved_objects.sh

# Kibana URL 변경
KIBANA_URL=http://localhost:5601 ./ops/logging/bootstrap_kibana_saved_objects.sh

# Data View ID를 알고 있을 때 (선택)
DATA_VIEW_ID=<data-view-id> ./ops/logging/bootstrap_kibana_saved_objects.sh
```

## 생성되는 객체
- Saved Queries
  - Gateway Errors (status >= 500)
  - Gateway Slow Requests (duration_ms > 1000)
  - Gateway Chat Completions (path 필터)
  - Gateway Rate Limit (status = 429)
- Saved Search
  - Gateway Errors (5xx)
- Dashboard
  - Gateway Logs Dashboard (에러 로그 패널 1개 포함)

## 참고
- 대시보드에는 기본 패널 1개만 포함됩니다. 필요 시 Kibana UI에서 패널을 추가하세요.
