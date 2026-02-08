# Kubernetes 배포

이 디렉토리는 Nexus Gateway, 모델 워커, Redis를 위한 최소 Kubernetes 구성입니다. 로컬 검증과 기본 배포 흐름을 빠르게 확인하기 위한 스캐폴딩이며, 운영 환경에서는 이미지/리소스/보안 설정을 실제 값으로 교체해야 합니다.

## 적용

```bash
kubectl apply -k k8s/
```

## Kustomize 오버레이

다음 오버레이가 제공됩니다.

- `k8s/overlays/mock`: CPU 전용 mock 워커 (기본)
- `k8s/overlays/gpu`: vLLM GPU 워커 (NVIDIA GPU 노드 필요)
- `k8s/overlays/bentoml`: BentoML 워커 (CPU, 옵션)

적용 예시:

```bash
kubectl apply -k k8s/overlays/mock
# 또는
kubectl apply -k k8s/overlays/gpu
# 또는
kubectl apply -k k8s/overlays/bentoml
```

옵션 SGLang 워커 (GPU):

```bash
kubectl apply -k k8s/overlays/gpu/sglang
```

옵션 BentoML 워커 (CPU):

```bash
kubectl apply -k k8s/overlays/bentoml
```

## 게이트웨이 라우팅 예시 (vLLM + SGLang)

두 워커를 모두 활성화했다면 `GATEWAY_UPSTREAMS`에 추가하고,
모델 ID별 라우팅 정책을 설정하세요 (아래 예시는 Llama 3 기준).

```yaml
GATEWAY_UPSTREAMS: "vllm=http://model-worker:8001;sglang=http://sglang-worker:8002"
GATEWAY_DEFAULT_UPSTREAM: "vllm"
GATEWAY_ROUTE_POLICIES: |
  {"meta-llama/Meta-Llama-3-8B-Instruct":
    {"strategy":"canary","primary":"vllm","canary":"sglang","percent":10}
  }
```

참고: 정책 키는 요청 payload의 `model` 문자열과 정확히 일치해야 합니다.

## 로컬 kind 클러스터 (Mac/Windows/Linux)

kind는 로컬에서 빠르게 검증하기 위한 경량 Kubernetes 클러스터입니다.

```bash
# 1) 클러스터 생성
kind create cluster --name nexus

# 2) gateway + model worker 이미지 로컬 빌드
docker build -t nexus-gateway:latest -f gateway/Dockerfile gateway
docker build -t nexus-model-worker:latest -f serving/mock-worker/Dockerfile serving/mock-worker

# 3) kind에 이미지 로드
kind load docker-image nexus-gateway:latest --name nexus
kind load docker-image nexus-model-worker:latest --name nexus

# 4) 매니페스트 적용
kubectl apply -k k8s/
kubectl rollout status -n nexus deployment/nexus-gateway
```

### Ingress (kind)

```bash
# kind용 ingress-nginx 설치
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=120s

# Ingress 포트포워딩 후 호스트 라우팅 테스트
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
curl -H "Host: gateway.local" http://localhost:8080/health
```

### Service (ClusterIP) 스모크 테스트

```bash
kubectl -n nexus port-forward svc/nexus-gateway 8000:80
curl http://localhost:8000/health
```

### kind 참고 사항
- LoadBalancer 서비스는 MetalLB 없이 `<pending>` 상태로 남습니다.
- 브라우저에서 `gateway.local`을 쓰려면 `/etc/hosts`에 추가해야 합니다.

### MetalLB 로드밸런서 (kind)

```bash
# MetalLB 설치
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
kubectl wait --namespace metallb-system --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=120s

# kind 네트워크 IPv4 서브넷 확인 (그 안에서 사용 가능한 IP 범위를 선택)
docker network inspect kind -f '{{range .IPAM.Config}}{{if .Gateway}}{{.Subnet}}{{end}}{{end}}'

# 예시: 서브넷이 172.20.0.0/16이라면 172.20.255.200-172.20.255.250 같은 작은 범위를 선택
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

# LoadBalancer 서비스의 EXTERNAL-IP 확인
kubectl get svc -n nexus
```

참고: 예시 IP 범위는 실제 `kind` 서브넷에 맞게 변경하세요.

## 이미지 빌드 및 푸시

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/build_push_gateway.sh
```

## 모델 워커 이미지 (mock)

```bash
docker build -t nexus-model-worker:latest -f serving/mock-worker/Dockerfile serving/mock-worker
```

## GPU 워커 참고 (vLLM)

- `MODEL_ID`는 `k8s/overlays/gpu/model-worker-deployment.yaml`에서 설정
- 옵션 토큰은 `k8s/overlays/gpu/model-worker-secret.yaml`에 추가
  - `HF_TOKEN`은 게이티드/프라이빗 모델용 Hugging Face 토큰

## KServe/BentoML 스캐폴딩

- KServe 템플릿: `k8s/kserve/inferenceservice.yaml`
- BentoML 플레이스홀더: `serving/bentoml/README.md`

## 배포 이미지 업데이트

```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/k8s_set_gateway_image.sh
```

## 참고 사항
- `gateway/deployment.yaml`을 실제 레지스트리 이미지로 변경하세요.
- Redis는 속도 제한을 위한 단일 인스턴스로 배포됩니다.
- GPU 오버레이는 NVIDIA device plugin과 GPU 노드가 필요합니다.
- 모델 워커 HPA는 기본적으로 CPU 사용률 기반입니다.
- vLLM GPU 워커는 `/data`에 모델 캐시를 저장하며 `HF_TOKEN`을 사용합니다.

## 왜 GPU 노드풀을 쓰나요?

- GPU는 비용이 크고 리소스 특성이 달라서 일반 워크로드와 분리 운영하는 것이 안정적입니다.
- 노드풀 분리 + `nodeSelector`/`tolerations`로 **GPU 워크로드만** GPU 노드에 배치합니다.

## nodeSelector / taints / tolerations 간단 설명

- **nodeSelector**: 특정 라벨이 있는 노드에만 배치하도록 제한
- **taint**: 해당 노드에 일반 워크로드가 올라오지 못하도록 차단
- **toleration**: taint가 걸린 노드에 “이 워크로드는 올라가도 됨”을 허용

## 서빙 표준화란?

- 모델 배포/롤백/트래픽 전환을 **한 가지 표준 방식**으로 통일하는 것입니다.
- KServe/BentoML 같은 도구로 표준화하면 운영 비용과 장애 대응 시간이 줄어듭니다.

## 워커 스캐폴딩이란?

- 실제 모델 서버를 만들기 전, **배포 구조와 틀**을 먼저 준비해 두는 작업입니다.
- 이후 모델이나 프레임워크가 바뀌어도 운영 경로를 유지할 수 있습니다.

## GPU node pool 운영 가이드

권장 운영 방식:
- GPU 노드풀을 별도로 분리하고 `nodepool=gpu` 라벨을 부여
- GPU 전용 노드에는 `nvidia.com/gpu=true:NoSchedule` 같은 taint 적용
- GPU 워크로드는 `nodeSelector` + `tolerations` 조합으로만 스케줄
