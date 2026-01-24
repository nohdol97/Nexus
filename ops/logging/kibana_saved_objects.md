# Kibana Saved Objects 자동 생성

이 문서는 Kibana Saved Objects(저장 객체)를 자동으로 생성하는 스크립트 설명입니다.

## 대상
- Saved Query (KQL)
- Dashboard (빈 템플릿)

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
- Dashboard
  - Gateway Logs Dashboard (빈 템플릿)

## 참고
- Dashboard에 패널은 아직 자동으로 붙이지 않습니다. 필요 시 Kibana UI에서 패널을 추가하세요.
