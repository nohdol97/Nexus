# Nexus SLO & Runbook (Gateway + Logging)

## Scope
- 대상: Gateway API와 로그 파이프라인(Kafka -> Elasticsearch -> Kibana)
- 목적: 운영 품질 기준(SLO)과 장애 대응 절차(Runbook) 정의

## 핵심 용어 (한글 설명)
- **SLI(Service Level Indicator, 서비스 수준 지표)**: 품질을 수치로 측정하는 지표
- **SLO(Service Level Objective, 서비스 수준 목표)**: SLI에 대한 목표값
- **SLA(Service Level Agreement, 서비스 수준 계약)**: 외부 고객과 합의한 보장 수준
- **Error Budget(에러 예산)**: SLO에서 허용하는 실패 범위
- **Runbook(런북)**: 장애 대응 절차를 정리한 문서

## Observability Sources
- Metrics: Prometheus `/metrics`
  - `gateway_requests_total`
  - `gateway_request_latency_seconds`
  - `gateway_in_flight_requests`
  - `gateway_upstream_requests_total`
  - `gateway_upstream_latency_seconds`
  - `gateway_rate_limited_total`
  - `gateway_circuit_open_total`
  - `gateway_fallback_used_total`
- Logs: Elasticsearch index `gateway-logs-YYYY.MM.DD`
- UI: Grafana (metrics), Kibana (logs, Elasticsearch 데이터를 웹으로 조회/검색)

## Initial SLOs (tune later)

### Availability
- SLI(지표): 1 - (5xx / total)
- Target(목표): 99.9% monthly
- Notes(설명): 4xx는 클라이언트 오류로 제외, 429는 별도 Rate Limit 지표로 관리

### Latency
- SLI(지표): `gateway_request_latency_seconds` p95
- Target(목표): p95 < 1.0s (v1/chat/completions)

### Error Rate
- SLI(지표): 5xx ratio
- Target(목표): < 0.1% (rolling 5 minutes)

### Saturation
- SLI(지표): `gateway_in_flight_requests`
- Target(목표): 평균 < 50, 순간 피크 < 200

### Upstream Health
- SLI(지표): `gateway_upstream_requests_total{status="error"}` 비율
- Target(목표): < 1% (rolling 5 minutes)

## Alert Suggestions (example)
- 5xx ratio > 1% for 5m
- p95 latency > 1.5s for 5m
- circuit_breaker open > 5/min for 10m
- rate_limited spike > 5% for 10m
- upstream error > 2% for 5m

---

# Runbook

## Runbook 항목 설명
- **Symptoms(증상)**: 문제가 발생했을 때 관찰되는 현상/징후
- **Checks(확인)**: 원인 파악을 위한 점검 명령/항목
- **Mitigation(완화/복구)**: 서비스를 정상화하기 위한 대응 방법

## 1) Gateway Down or Unreachable

### Symptoms
- `/health` 5xx or timeout
- Prometheus target down

### Checks
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/health
docker compose -f docker-compose.yml -f docker-compose.logging.yml ps
```

### Mitigation
- Restart gateway container
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml restart gateway
```

---

## 2) High Error Rate (5xx)

### Symptoms
- 5xx ratio spike
- Gateway logs show upstream errors

### Checks
```bash
curl -s http://localhost:8000/metrics | rg gateway_requests_total
docker logs --tail 200 nexus-gateway-1
```

### Mitigation
- Check upstream availability (mock/vLLM/etc)
- Enable fallback routing if configured
- Reduce traffic or tighten rate limits

---

## 3) High Latency

### Symptoms
- p95 latency breach
- Upstream latency spike

### Checks
```bash
curl -s http://localhost:8000/metrics | rg gateway_request_latency_seconds
curl -s http://localhost:8000/metrics | rg gateway_upstream_latency_seconds
```

### Mitigation
- Scale up gateway (more replicas)
- Investigate upstream capacity
- Apply load shedding for large payloads

---

## 4) Circuit Breaker Open

### Symptoms
- `gateway_circuit_open_total` 증가
- 특정 upstream으로 요청이 차단됨

### Checks
```bash
curl -s http://localhost:8000/v1/circuit-breakers
```

### Mitigation
- 해당 upstream 상태 확인 후 복구
- 임시로 fallback 경로 유지

---

## 5) Rate Limiting Spike

### Symptoms
- `gateway_rate_limited_total` 급증

### Checks
```bash
curl -s http://localhost:8000/metrics | rg gateway_rate_limited_total
```

### Mitigation
- 정상 트래픽인지 확인
- 키/사용자별 제한 완화 혹은 차단 조정

---

## 6) Logging Pipeline Missing Logs

### Symptoms
- Kibana에서 로그가 보이지 않음
- Elasticsearch index 미생성

### Checks
```bash
# Kafka topic
 docker exec nexus-kafka-1 kafka-topics --bootstrap-server localhost:9092 --list

# Consumer group lag
 docker exec nexus-kafka-1 kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group vector-elasticsearch

# Elasticsearch index
 curl -s "http://localhost:9200/_cat/indices?v" | rg gateway
```

### Mitigation
- Vector ingest/indexer 로그 확인
```bash
docker logs --tail 200 nexus-vector-ingest-1
docker logs --tail 200 nexus-vector-indexer-1
```
- Kafka/Elasticsearch 재시작
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml restart kafka elasticsearch
```

---

## 7) Kibana UI Unavailable

### Symptoms
- Kibana 접속 실패

### Checks
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5601/api/status
```

### Mitigation
- Kibana 재시작
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml restart kibana
```

---

## Notes
- 로컬 환경 기준이며, 운영 환경에서는 SLO/Alert 기준을 조정해야 합니다.
- 로그 파이프라인은 `gateway` 컨테이너 로그(JSON)를 기준으로 동작합니다.
- 로컬 재현 요약: `ops/runbook_quickstart.md`
