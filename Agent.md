# Nexus Implementation Rules

These rules guide all implementation work in this repo.

## Scope
- Keep the system aligned with the ML Platform role: gateway, serving, Kubernetes ops, MLOps automation, and observability.

## Gateway
- Build on FastAPI + LiteLLM.
- Enforce auth (API key/JWT), routing policy, rate limiting, and request validation.
- Implement circuit breaker + fallback and cap retries.
- Propagate request-id and trace-id.

## Serving
- Support vLLM/SGLang/Triton behind a common interface.
- Version models and configs; no silent changes.
- Tune for latency and throughput with documented benchmarks.

## Kubernetes
- Set requests/limits, GPU resources, and node selectors/taints.
- Use HPA and PDB for stability.
- Separate GPU node pools for different tiers when applicable.

## Observability and Logging
- Expose Prometheus metrics for latency, TPS, error rate, and GPU utilization.
- Emit structured logs and ship serving events through Kafka to Elasticsearch/Kibana.
- Define SLOs and alerts; keep a runbook for incidents.

## Reliability and Security
- Use timeouts, backoff with jitter, and load shedding.
- Do not commit secrets; use env vars or secret manager.
- Redact PII from logs and keep audit trails.

## Process
- Update `plan.md` when architecture or milestones change.
- Add tests for routing, fallback, and critical workflows.
