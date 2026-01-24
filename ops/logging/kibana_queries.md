# Kibana Query Templates (Gateway Logs)

이 문서는 Kibana Discover에서 바로 사용할 수 있는 검색 템플릿(KQL)을 정리합니다.

## 기본 전제
- 데이터 뷰: `gateway-logs-*`
- 주요 필드: `status`, `duration_ms`, `path`, `upstream`, `request_id`, `trace_id`, `client_ip`, `message`, `event`

---

## 1) 에러(5xx)만 보기
```
status >= 500
```

## 2) 느린 요청(p95 후보)
```
duration_ms > 1000
```

## 3) 특정 엔드포인트만 보기
```
path : "/v1/chat/completions"
```

## 4) 업스트림별 필터
```
upstream : "mock"
```

## 5) 특정 요청 추적(request_id)
```
request_id : "<request-id>"
```

## 6) 분산 추적(trace_id)
```
trace_id : "<trace-id>"
```

## 7) 클라이언트 IP 기준
```
client_ip : "<ip>"
```

## 8) 메시지 유형 필터
```
message : "request_completed"
```

---

## 활용 팁
- 시간 범위를 먼저 줄이면(예: Last 15 minutes) 검색 속도가 빨라집니다.
- `status` + `path` 조합으로 오류 구간을 빠르게 찾을 수 있습니다.
- `duration_ms` 필터로 느린 요청을 잡아낸 뒤, `upstream` 또는 `path`로 원인을 좁혀가세요.
