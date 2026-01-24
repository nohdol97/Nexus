# Gateway Log Schema

이 문서는 Gateway가 출력하는 구조화 로그의 주요 필드를 정리합니다.

## 필드 목록

| 필드 | 설명 | 예시 |
| --- | --- | --- |
| timestamp | 로그 발생 시각 (UTC) | `2026-01-25T08:25:14.064Z` |
| level | 로그 레벨 | `INFO` |
| message | 이벤트 이름 | `request_completed` |
| event | 이벤트 유형 | `request` |
| request_id | 요청 고유 ID | `83aee063-fdd2-4219-9135-a52179fffbe5` |
| trace_id | 추적 ID (request_id와 동일할 수 있음) | `83aee063-fdd2-4219-9135-a52179fffbe5` |
| method | HTTP 메서드 | `POST` |
| path | 요청 경로 | `/v1/chat/completions` |
| status | HTTP 응답 코드 | `200` |
| duration_ms | 처리 시간(ms) | `307` |
| upstream | 라우팅된 업스트림 | `mock` |
| client_ip | 클라이언트 IP | `172.64.66.1` |

## 활용 예시

- 5xx 에러만 보기
  ```
  status >= 500
  ```

- 느린 요청 보기
  ```
  duration_ms > 1000
  ```

- 특정 엔드포인트 추적
  ```
  path : "/v1/chat/completions"
  ```

## 참고
- 로그 스키마는 `gateway/app/core/logging.py`에서 정의됩니다.
- 필요 시 필드를 확장하고, Kibana 데이터 뷰에 필드를 반영하세요.
