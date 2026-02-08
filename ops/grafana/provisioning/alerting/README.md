# Grafana 알림 프로비저닝

이 설정은 Grafana의 알림 연락처(Contact Points)와 알림 정책(Notification Policies)을 자동으로 프로비저닝합니다.

## 파일
- `contact-points.yml`: 기본 웹훅 연락처
- `notification-policies.yml`: 기본 라우팅 정책

## 참고
- 웹훅은 `http://alertmanager:9093/api/v1/alerts`의 Alertmanager로 전송됩니다.
- 필요 시 Slack/Email 등의 수신자로 교체하세요.
