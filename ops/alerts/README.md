# 알림 (Prometheus + Alertmanager)

이 폴더는 로컬 환경에서 Prometheus 경보를 Alertmanager로 전달하고 라우팅 규칙을 확인하기 위한 최소 구성입니다. 운영 환경에서는 실제 수신자(Slack/Email/Webhook) 설정으로 교체하세요.

## 파일
- `ops/alertmanager.yml`: 기본 Alertmanager 설정
- `ops/prometheus_alerts.yml`: Prometheus 알림 규칙

## 로컬 실행
Alertmanager는 docker compose로 실행되며 Prometheus의 알림을 수신합니다.

```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml up -d alertmanager
```

## 접속
- Alertmanager UI: http://localhost:9093

## 수신자 추가 (예시)
`ops/alertmanager.yml`에 receiver 블록을 추가하세요. 웹훅 예시는 다음과 같습니다.

```yaml
receivers:
  - name: default
    webhook_configs:
      - url: "https://example.com/webhook"
        send_resolved: true
```

변경 후 Alertmanager를 재시작합니다.

```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml restart alertmanager
```

## 템플릿
- `ops/alerts/receiver_templates.md`

## 테스트 알림
```bash
./ops/alerts/test_alert.sh
```
