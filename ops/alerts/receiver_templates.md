# Alertmanager Receiver Templates

이 문서는 Alertmanager 수신자(receiver) 템플릿을 정리합니다.

## 1) Webhook (기본)
```yaml
receivers:
  - name: default
    webhook_configs:
      - url: "https://example.com/webhook"
        send_resolved: true
```

## 2) Slack (Webhook)
```yaml
receivers:
  - name: slack
    slack_configs:
      - api_url: "https://hooks.slack.com/services/XXX/YYY/ZZZ"
        channel: "#alerts"
        username: "nexus-alerts"
        title: "[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }}"
        text: "{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}"
        send_resolved: true
```

## 3) Email (SMTP)
```yaml
receivers:
  - name: email
    email_configs:
      - to: "oncall@example.com"
        from: "alertmanager@example.com"
        smarthost: "smtp.example.com:587"
        auth_username: "alertmanager@example.com"
        auth_password: "<PASSWORD>"
        send_resolved: true
```

## 참고
- 실제 토큰/비밀번호는 커밋하지 말고 환경 변수나 Secret으로 관리하세요.
- 적용 후 `docker compose ... restart alertmanager`로 재시작 필요.
