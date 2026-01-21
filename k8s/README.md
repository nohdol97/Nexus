# Kubernetes Deployment

This directory contains a minimal Kubernetes setup for the Nexus Gateway and Redis.

## Apply

```bash
kubectl apply -k k8s/
```

## Build & push image

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/build_push_gateway.sh
```

## Update deployment image

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/k8s_set_gateway_image.sh
```

## Notes
- Update `gateway/deployment.yaml` to point at a real image (for example, a registry image).
- Redis is deployed as a single instance for rate limiting.

## GPU scheduling (model workers)

When you add model workers (vLLM/SGLang/Triton), schedule them to GPU nodes:

```yaml
resources:
  limits:
    nvidia.com/gpu: "1"
nodeSelector:
  nodepool: gpu
```

## Smoke test

```bash
kubectl -n nexus port-forward svc/nexus-gateway 8000:80
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "X-API-Key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```
