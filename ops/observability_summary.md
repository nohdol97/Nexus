# Observability Summary (Current)

현재 로컬 기준으로 구성된 관측 스택을 요약합니다.

## 구성 요소
- Metrics: Prometheus → Grafana
- Logs: Vector → Kafka → Elasticsearch → Kibana
- Alerts: Prometheus → Alertmanager (Grafana Webhook 연계)

## 실행 명령
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml up -d
```

## 접근 URL
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Kibana: http://localhost:5601
- Alertmanager: http://localhost:9093

## 핵심 문서
- SLO/Runbook: `ops/slo_runbook.md`
- Runbook Quickstart: `ops/runbook_quickstart.md`
- Log Schema: `ops/logging/log_schema.md`
- Kibana Queries: `ops/logging/kibana_queries.md`
- Kibana Dashboard Template: `ops/logging/kibana_dashboard.md`
- Correlation Guide: `ops/logging/correlation_guide.md`
- Observability Status: `ops/observability_status.md`
