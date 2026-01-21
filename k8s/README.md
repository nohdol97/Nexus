# Kubernetes Deployment

This directory contains a minimal Kubernetes setup for the Nexus Gateway, model worker, and Redis.

## Apply

```bash
kubectl apply -k k8s/
```

## Kustomize overlays

Two overlays are provided:

- `k8s/overlays/mock`: CPU-only mock worker (default behavior)
- `k8s/overlays/gpu`: vLLM GPU worker (requires NVIDIA GPU nodes)

Apply one of them like this:

```bash
kubectl apply -k k8s/overlays/mock
# or
kubectl apply -k k8s/overlays/gpu
```

Optional SGLang worker (GPU):

```bash
kubectl apply -k k8s/overlays/gpu/sglang
```

## Gateway routing example (vLLM + SGLang)

If you enable both workers, add them to `GATEWAY_UPSTREAMS` and set a routing policy
for the model ID you serve (example below uses Llama 3):

```yaml
GATEWAY_UPSTREAMS: "vllm=http://model-worker:8001;sglang=http://sglang-worker:8002"
GATEWAY_DEFAULT_UPSTREAM: "vllm"
GATEWAY_ROUTE_POLICIES: |
  {"meta-llama/Meta-Llama-3-8B-Instruct":
    {"strategy":"canary","primary":"vllm","canary":"sglang","percent":10}
  }
```

Note: The policy key must match the `model` string in the request payload.

## Local kind cluster (Mac/Windows/Linux)

kind is a local Kubernetes cluster for quick verification.

```bash
# 1) Create cluster
kind create cluster --name nexus

# 2) Build gateway + model worker images locally
docker build -t nexus-gateway:latest -f gateway/Dockerfile gateway
docker build -t nexus-model-worker:latest -f serving/mock-worker/Dockerfile serving/mock-worker

# 3) Load images into kind
kind load docker-image nexus-gateway:latest --name nexus
kind load docker-image nexus-model-worker:latest --name nexus

# 4) Apply manifests
kubectl apply -k k8s/
kubectl rollout status -n nexus deployment/nexus-gateway
```

### Ingress (kind)

```bash
# Install ingress-nginx for kind
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=120s

# Port-forward ingress and test host routing
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
curl -H "Host: gateway.local" http://localhost:8080/health
```

### Service (ClusterIP) smoke test

```bash
kubectl -n nexus port-forward svc/nexus-gateway 8000:80
curl http://localhost:8000/health
```

### Notes for kind
- LoadBalancer services stay in `<pending>` without MetalLB.
- If you want to use `gateway.local` in a browser, add it to `/etc/hosts`.

### LoadBalancer with MetalLB (kind)

```bash
# Install MetalLB
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
kubectl wait --namespace metallb-system --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=120s

# Find the kind network IPv4 subnet (use a free IP range inside it)
docker network inspect kind -f '{{range .IPAM.Config}}{{if .Gateway}}{{.Subnet}}{{end}}{{end}}'

# Example: if subnet is 172.20.0.0/16, pick a small range like 172.20.255.200-172.20.255.250
cat <<'EOF' | kubectl apply -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: nexus-pool
  namespace: metallb-system
spec:
  addresses:
    - 172.20.255.200-172.20.255.250
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: nexus-adv
  namespace: metallb-system
EOF

# Check EXTERNAL-IP for the LoadBalancer service
kubectl get svc -n nexus
```

Note: replace the example IP range with one that fits your `kind` subnet.

## Build & push image

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/build_push_gateway.sh
```

## Model worker image (mock)

```bash
docker build -t nexus-model-worker:latest -f serving/mock-worker/Dockerfile serving/mock-worker
```

## GPU worker notes (vLLM)

- `MODEL_ID` in `k8s/overlays/gpu/model-worker-deployment.yaml`
- Optional token in `k8s/overlays/gpu/model-worker-secret.yaml`
  - `HF_TOKEN` is a Hugging Face access token for gated/private models

## Update deployment image

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/k8s_set_gateway_image.sh
```

## Notes
- Update `gateway/deployment.yaml` to point at a real image (for example, a registry image).
- Redis is deployed as a single instance for rate limiting.
- GPU overlay requires NVIDIA device plugin and GPU nodes.
- Model worker HPA scales on CPU utilization by default.
- vLLM GPU worker uses `/data` for model cache and `HF_TOKEN` from `model-worker-secrets`.

## GPU node pool 운영 가이드

권장 운영 방식:
- GPU 노드풀을 별도로 분리하고 `nodepool=gpu` 라벨을 부여
- GPU 전용 노드에는 `nvidia.com/gpu=true:NoSchedule` 같은 taint 적용
- GPU 워크로드는 `nodeSelector` + `tolerations` 조합으로만 스케줄

예시:

```yaml
nodeSelector:
  nodepool: gpu
tolerations:
  - key: "nvidia.com/gpu"
    operator: "Exists"
    effect: "NoSchedule"
```

운영 팁:
- A100/H100/B300 등 세대별로 노드풀을 분리하면 비용/성능 튜닝이 쉬움
- 모델 워커별 리소스 스펙을 노드풀에 맞춰 표준화 (예: 1 GPU / 16Gi / 4 vCPU)

## Expose the gateway

Two options are provided:

- LoadBalancer service: `k8s/gateway/service-lb.yaml`
- Ingress (nginx): `k8s/gateway/ingress.yaml` (host: `gateway.local`)

If you only want one, remove the other from `k8s/kustomization.yaml`.

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
  -d '{"model":"mock-worker","messages":[{"role":"user","content":"hello"}]}'
```
