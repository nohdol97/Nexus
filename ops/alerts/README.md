# Alerting (Prometheus + Alertmanager)

This folder provides a minimal Alertmanager setup for local alert routing.

## Files
- `ops/alertmanager.yml`: default Alertmanager config
- `ops/prometheus_alerts.yml`: Prometheus alert rules

## Local run
Alertmanager runs via docker compose and receives alerts from Prometheus.

```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml up -d alertmanager
```

## Access
- Alertmanager UI: http://localhost:9093

## Add a receiver (example)
Edit `ops/alertmanager.yml` and add a receiver block. Example for a webhook:

```yaml
receivers:
  - name: default
    webhook_configs:
      - url: "https://example.com/webhook"
        send_resolved: true
```

Then restart alertmanager:
```bash
docker compose -f docker-compose.yml -f docker-compose.logging.yml restart alertmanager
```
