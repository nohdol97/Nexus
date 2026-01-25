# Observability Status (Local)

이 문서는 로컬 환경에서 관측 스택 상태를 빠르게 확인하기 위한 체크리스트입니다.

## 1) 서비스 상태
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml ps
```

## 2) Metrics (Prometheus)
- URL: http://localhost:9090
- Targets: `Status -> Targets` 에서 `gateway`가 UP인지 확인

## 3) Dashboards (Grafana)
- URL: http://localhost:3000
- 기본 대시보드: `Nexus` (provisioned)

## 4) Logs (Kibana)
- URL: http://localhost:5601
- Data view: `gateway-logs-*`
- Discover 탭에서 로그 조회

## 5) Alerts (Alertmanager)
- URL: http://localhost:9093
- Active Alerts 탭 확인

## 6) Alert Test (Alertmanager)
```bash
./ops/alerts/test_alert.sh
```

## 7) Quick Log Flow Test
```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: dev-key' \
  -d '{"model":"mock","messages":[{"role":"user","content":"log test"}]}' | head -n 1

curl -s "http://localhost:9200/_cat/indices?v" | rg gateway
```
