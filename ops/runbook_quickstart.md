# Runbook Quickstart (Local)

이 문서는 로컬에서 장애 상황을 빠르게 재현/확인하기 위한 최소 절차입니다.

## 1) Gateway Down
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml stop gateway
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/health
```

## 2) Error Rate Spike (5xx)
```bash
# mock upstream를 임의로 실패시키는 테스트는 현재 미구현
# 대신, 의도적으로 잘못된 upstream을 호출하거나 잘못된 모델명을 호출해 확인
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: dev-key' \
  -d '{"model":"unknown","messages":[{"role":"user","content":"fail"}]}' | head -n 1
```

## 3) Latency Spike (직접 재현은 어려움)
- mock upstream이므로 실제 지연 재현은 제한됨
- 실제 GPU 환경에서만 의미있는 결과를 얻을 수 있음

## 4) Log Flow Test
```bash
curl -s -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: dev-key' \
  -d '{"model":"mock","messages":[{"role":"user","content":"log test"}]}' | head -n 1

curl -s "http://localhost:9200/_cat/indices?v" | rg gateway
```

## 5) Alert Test
```bash
./ops/alerts/test_alert.sh
```

## 6) Restore
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml start gateway
```
