# Metrics ↔ Logs Correlation Guide

이 문서는 **Prometheus 지표**와 **Kibana 로그**를 함께 보면서 원인을 좁히는 방법을 정리합니다.

## 1) 에러율 급증

### 1-1. Prometheus에서 확인
- `gateway_requests_total`의 5xx 비율이 상승했는지 확인
- 알림: `GatewayHighErrorRate`

### 1-2. Kibana에서 확인
- KQL
  ```
  status >= 500
  ```
- 특정 엔드포인트 확인
  ```
  path : "/v1/chat/completions"
  ```
- 업스트림 에러 확인
  ```
  upstream : "mock"
  ```

## 2) 지연시간(p95) 급증

### 2-1. Prometheus에서 확인
- 지표: `gateway_request_latency_seconds` p95
- 알림: `GatewayHighLatencyP95`

### 2-2. Kibana에서 확인
- 느린 요청 필터
  ```
  duration_ms > 1000
  ```
- 특정 경로/업스트림으로 좁히기
  ```
  path : "/v1/chat/completions"
  upstream : "mock"
  ```

## 3) 업스트림 장애 징후

### 3-1. Prometheus에서 확인
- 지표: `gateway_upstream_requests_total{status="error"}` 비율
- 알림: `UpstreamErrorRateHigh`

### 3-2. Kibana에서 확인
- 업스트림 필터
  ```
  upstream : "mock"
  ```
- 오류 응답만 보기
  ```
  status >= 500
  ```

## 4) 레이트 리밋 급증

### 4-1. Prometheus에서 확인
- 지표: `gateway_rate_limited_total`
- 알림: `GatewayRateLimitSpike`

### 4-2. Kibana에서 확인
- 레이트 리밋 응답(429)
  ```
  status = 429
  ```
- 특정 클라이언트 IP 추적
  ```
  client_ip : "<ip>"
  ```

## 5) 회로 차단기 열림

### 5-1. Prometheus에서 확인
- 지표: `gateway_circuit_open_total`
- 알림: `GatewayCircuitBreakerOpen`

### 5-2. Kibana에서 확인
- Circuit Breaker 로그
  ```
  message : "circuit"
  ```

## 참고
- 먼저 시간 범위를 줄이고(최근 15분) → 에러/지연 필터 → 경로/업스트림으로 좁히는 순서를 권장합니다.
