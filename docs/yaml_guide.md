# YAML 쉽게 이해하기 (비개발자용)

이 문서는 “YAML 파일이 무엇이고, 어떤 구조로 되어 있는지”를 쉽게 설명합니다.

---

## 1) YAML이란?

- **사람이 읽기 쉬운 설정 파일 형식**입니다.
- 프로그램을 실행하거나 서버를 배포할 때 필요한 **규칙/설정**을 적어 둡니다.
- 핵심은 “**키: 값**” 형태의 구조입니다.

예시:

```yaml
name: nexus
replicas: 2
```

---

## 2) YAML의 기본 규칙

### (1) 들여쓰기(Indent)로 구조를 만든다
- YAML은 **띄어쓰기(스페이스)** 로 계층 구조를 표현합니다.
- 같은 수준은 같은 들여쓰기, 하위는 더 깊게 들여쓰기.

```yaml
app:
  name: gateway
  port: 8000
```

### (2) 리스트는 `-` 로 표현한다
```yaml
ports:
  - 8000
  - 8001
```

### (3) 주석은 `#` 로 시작한다
```yaml
# 이건 주석입니다
name: gateway
```

---

## 3) Kubernetes YAML의 공통 구조

Kubernetes에서는 거의 모든 YAML이 아래 구조를 갖습니다:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: example
spec:
  ...
```

### 각 항목의 의미
- **apiVersion**: 이 설정이 어떤 버전 규칙을 따르는지
- **kind**: 어떤 리소스인지 (예: Deployment, Service, Secret)
- **metadata**: 이름/라벨 같은 정보
- **spec**: 실제 동작 규칙(가장 중요한 부분)

---

## 4) Pod는 어디에 정의되나요?

Pod는 Kubernetes의 **최소 실행 단위**입니다.  
하지만 보통 **Pod를 직접 만들지 않고 Deployment가 Pod를 만들어 줍니다.**

즉, Pod 구조는 아래 위치에 들어 있습니다:

```yaml
kind: Deployment
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: gateway
          image: ...
```

- **replicas**: Pod 개수
- **template**: Pod의 설계도(컨테이너/포트/환경변수 등)

---

## 5) 우리 프로젝트에서 자주 보는 YAML 종류

### (1) Deployment (앱 실행)
앱을 몇 개 띄울지, 어떤 이미지로 띄울지 적습니다.

```yaml
kind: Deployment
spec:
  replicas: 2
```

### (2) Service (주소 만들기)
여러 Pod를 하나의 주소로 묶습니다.

```yaml
kind: Service
spec:
  ports:
    - port: 80
```

### (3) labels / selectors (연결 고리)
Service는 **라벨을 가진 Pod**를 찾아서 연결합니다.

```yaml
metadata:
  labels:
    app: gateway
spec:
  selector:
    app: gateway
```

### (3) ConfigMap / Secret (설정/비밀)
앱 설정 값이나 비밀 키를 분리해서 관리합니다.

```yaml
kind: ConfigMap
data:
  KEY: "value"
```

### (4) Ingress (외부 접속)
도메인으로 들어오는 요청을 서비스로 연결합니다.

```yaml
kind: Ingress
spec:
  rules:
    - host: gateway.local
```

### (5) HPA (자동 확장)
Pod 수를 자동으로 늘리거나 줄입니다.

```yaml
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 1
  maxReplicas: 3
```

### (6) Resources (CPU/메모리/GPU)
어떤 자원을 얼마나 쓸지 정합니다.

```yaml
resources:
  requests:
    cpu: "1000m"
    memory: "4Gi"
  limits:
    nvidia.com/gpu: "1"
```

### (7) Probes (헬스체크)
앱이 정상인지 확인하는 검사입니다.

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
```

### (8) 환경변수 (env / envFrom)
앱 실행에 필요한 설정을 주입합니다.

```yaml
env:
  - name: GATEWAY_UPSTREAMS
    value: "worker=http://model-worker:8001"
envFrom:
  - configMapRef:
      name: nexus-gateway-config
```

### (9) 볼륨/볼륨마운트
컨테이너가 데이터를 저장하거나 캐시를 공유할 때 사용합니다.

```yaml
volumes:
  - name: model-cache
    emptyDir: {}
containers:
  - name: model-worker
    volumeMounts:
      - name: model-cache
        mountPath: /data
```

### (10) imagePullPolicy
이미지를 언제 받아올지 정합니다.

```yaml
imagePullPolicy: IfNotPresent
```

---

## 6) Namespace(네임스페이스)

리소스를 **공간별로 구분**하는 구조입니다.  
예: `nexus` 네임스페이스 안에 Gateway, Redis, Worker가 함께 존재.

```yaml
metadata:
  namespace: nexus
```

---

## 7) Service 타입 (ClusterIP / LoadBalancer)

- **ClusterIP**: 클러스터 내부에서만 접근 가능
- **LoadBalancer**: 외부에서 접근 가능한 IP를 붙임

```yaml
kind: Service
spec:
  type: LoadBalancer
```

## 8) Ingress vs LoadBalancer

- **LoadBalancer**: 서비스 하나에 외부 IP를 직접 붙임
- **Ingress**: 여러 서비스로 들어오는 요청을 한入口에서 라우팅

요약:  
Ingress는 “문지기(라우터)”, LoadBalancer는 “단독 출입구”

---

## 9) Kustomize(오버레이) 구조

우리 프로젝트는 기본 설정을 두고, 환경별로 “덮어쓰기”합니다.

- 기본: `k8s/`
- mock 환경: `k8s/overlays/mock/`
- GPU 환경: `k8s/overlays/gpu/`

즉, **같은 구조를 유지하면서 필요한 값만 교체**합니다.

---

## 10) CRD(확장 리소스)

Kubernetes 기본 리소스 외에, 확장된 리소스도 있습니다.

예시:
- **KServe**의 `InferenceService`
- **Argo/Kubeflow**의 `Workflow`

이들은 **추가로 설치된 도구가 이해하는 YAML** 입니다.

---

## 11) YAML은 “직접 실행”되는 게 아니다

YAML 파일은 그냥 **설정 파일**입니다.  
Kubernetes나 다른 컨트롤러가 이 파일을 읽고 **Pod 같은 실제 작업을 실행**합니다.

예시:
```bash
kubectl apply -f some.yaml
```

---

## 12) 자주 하는 실수

- 들여쓰기 오류 (스페이스 수가 다르면 구조가 깨짐)
- `-` 리스트 표기 누락
- 대소문자/띄어쓰기 실수
- Secret에 민감 정보 그대로 넣기 (실사용 시 주의)

---

## 13) 이 프로젝트에 적용되는 예

- **Gateway 배포**: `k8s/gateway/deployment.yaml`
- **모델 워커 배포**: `k8s/model-worker/deployment.yaml`
- **GPU 오버레이**: `k8s/overlays/gpu/`
- **KServe 템플릿**: `k8s/kserve/inferenceservice.yaml`
- **Kubeflow 파이프라인**: `mlops/kubeflow/pipeline.yaml`

---

## 한 줄 요약

YAML은 **“서버를 어떻게 띄울지 적어 둔 설명서”** 입니다.  
Kubernetes가 이 설명서를 읽고 실제 서버를 실행합니다.
