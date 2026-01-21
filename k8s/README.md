# Kubernetes Deployment

This directory contains a minimal Kubernetes setup for the Nexus Gateway and Redis.

## Apply

```bash
kubectl apply -k k8s/
```

## Local kind cluster (Mac/Windows/Linux)

kind is a local Kubernetes cluster for quick verification.

```bash
# 1) Create cluster
kind create cluster --name nexus

# 2) Build gateway image locally
docker build -t nexus-gateway:latest -f gateway/Dockerfile gateway

# 3) Load image into kind
kind load docker-image nexus-gateway:latest --name nexus

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
    - 172.18.255.200-172.18.255.250
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

## Update deployment image

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/k8s_set_gateway_image.sh
```

## Notes
- Update `gateway/deployment.yaml` to point at a real image (for example, a registry image).
- Redis is deployed as a single instance for rate limiting.

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
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```
