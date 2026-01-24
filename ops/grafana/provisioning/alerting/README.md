# Grafana Alerting Provisioning

This config provisions Grafana alert contact points and notification policies.

## Files
- `contact-points.yml`: default webhook contact point
- `notification-policies.yml`: default routing policy

## Notes
- The webhook points to Alertmanager running at `http://alertmanager:9093/api/v1/alerts`.
- Replace this with Slack/Email receivers when needed.
