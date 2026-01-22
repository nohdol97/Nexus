# 비개발자용 요약 (전체 작업 맥락)

> 참고: 아래 용어 설명은 지속적으로 업데이트합니다. 새로운 작업이 추가되면 관련 용어/맥락도 함께 반영합니다.

## 한 줄 요약
- Nexus는 여러 AI 모델을 안전하고 안정적으로 연결해 주는 **중앙 관문(Gateway)** 을 만들고, 그 상태를 **관찰(모니터링)** 할 수 있게 하는 프로젝트입니다.

## 왜 필요한가요?
- 여러 모델/서비스를 한 곳에서 통합 관리하면 운영이 쉬워지고 장애 대응이 빨라집니다.
- 트래픽이 몰려도 안정적으로 동작하도록 **제한(Rate Limit)**, **장애 차단(Circuit Breaker)**, **대체 경로(Fallback)** 를 둡니다.
- 문제가 생겼을 때 원인을 빠르게 찾기 위해 **지표(Metrics)** 와 **로그(Logs)** 를 수집합니다.

## 어디에 쓰이나요?
- 회사 내부/서비스에서 모델 호출이 많을 때 “한 곳(게이트웨이)”으로 모아 관리합니다.
- 운영 대시보드(Grafana)에서 요청 수, 지연 시간, 에러율 등을 확인합니다.

---

# 용어 설명 (쉬운 버전)

- **Gateway(게이트웨이)**: 모든 요청이 처음 들어오는 “관문 서버”.
  - **왜 필요?** 인증/정책/라우팅을 한곳에서 처리해 관리가 쉬워짐.
  - **어디에?** `gateway/` 폴더의 FastAPI 앱.

- **Upstream(업스트림)**: 실제로 응답을 만들어 주는 모델 서버.
  - **왜 필요?** 게이트웨이는 요청을 전달만 하고, 결과는 업스트림이 생성.
  - **어디에?** `GATEWAY_UPSTREAMS` 설정에 등록.

- **Model Worker(모델 워커)**: 모델 추론을 실제로 수행하는 서버.
  - **왜 필요?** Gateway가 요청을 전달하면 Worker가 결과를 만들어 줌.
  - **어디에?** `k8s/model-worker/` 매니페스트, `serving/mock-worker/` 코드.

- **API**: 서비스가 서로 통신하기 위한 규칙(주소/형식).
  - **왜 필요?** 통일된 방식으로 요청/응답을 주고받기 위해.
  - **어디에?** `/v1/chat/completions` 같은 엔드포인트.

- **API Key(키)**: 간단한 인증 수단(비밀번호 같은 역할).
  - **왜 필요?** 아무나 호출하지 못하도록 접근 제어.
  - **어디에?** `X-API-Key` 헤더로 전송.

- **JWT(JSON Web Token)**: 서명된 인증 토큰.
  - **왜 필요?** 사용자/권한 정보를 안전하게 전달.
  - **어디에?** `Authorization: Bearer <token>` 헤더.

- **Rate Limiting(호출 제한)**: 일정 시간에 허용하는 요청 수 제한.
  - **왜 필요?** 과부하/남용 방지.
  - **어디에?** 게이트웨이에서 자동 차단.

- **Redis**: 빠른 메모리 DB.
  - **왜 필요?** 여러 서버가 동시에 Rate Limit을 공유하기 위해.
  - **어디에?** `GATEWAY_REDIS_URL` 설정.

- **Circuit Breaker(회로 차단기)**: 오류가 반복되면 해당 업스트림으로의 호출을 잠시 차단.
  - **왜 필요?** 장애가 있을 때 연쇄 실패를 막기 위해.
  - **어디에?** 업스트림 요청 전에 체크.

- **Fallback(대체 경로)**: 주 모델이 실패하면 다른 모델로 자동 전환.
  - **왜 필요?** 서비스 연속성 확보.
  - **어디에?** `GATEWAY_FALLBACKS` 설정.

- **Canary(카나리 배포)**: 새 버전으로 “일부”만 보내 테스트.
  - **왜 필요?** 전체 장애 없이 안전한 배포.
  - **어디에?** `GATEWAY_ROUTE_POLICIES`에서 비율 설정.

- **Weighted Routing(가중치 라우팅)**: 여러 업스트림에 비율로 트래픽 분배.
  - **왜 필요?** 특정 모델에 트래픽을 더/덜 보내고 싶을 때.
  - **어디에?** `GATEWAY_ROUTE_POLICIES`.

- **Prometheus(프로메테우스)**: 지표 수집기.
  - **왜 필요?** 요청 수, 지연 시간 같은 숫자를 모음.
  - **어디에?** `/metrics` 엔드포인트에서 수집.

- **Grafana(그라파나)**: 지표 시각화 대시보드.
  - **왜 필요?** Prometheus 데이터를 그래프로 쉽게 보기 위해.
  - **어디에?** `http://localhost:3000`에서 대시보드 확인.

- **Logging(로그)**: 발생한 이벤트 기록.
  - **왜 필요?** 장애 원인을 추적하기 위해.
  - **어디에?** JSON 형태로 표준 출력.

- **Docker/Compose**: 여러 서비스를 한 번에 실행하는 도구.
  - **왜 필요?** Gateway + Prometheus + Grafana를 쉽게 실행.
  - **어디에?** `docker-compose.yml` 사용.

- **Healthcheck(헬스체크)**: 서비스가 정상인지 확인하는 간단한 검사.
  - **왜 필요?** 준비가 안 된 서비스를 구분하기 위해.
  - **어디에?** `docker-compose.vllm.yml`의 vLLM healthcheck.

- **Kubernetes(K8s)**: 컨테이너 앱을 여러 서버에서 자동으로 운영하는 플랫폼.
  - **왜 필요?** 서비스 배포/확장/복구를 자동화하기 위해.
  - **어디에?** `k8s/` 폴더 매니페스트.

- **Namespace(네임스페이스)**: Kubernetes 안에서 리소스를 구분하는 공간.
  - **왜 필요?** 서비스/환경별로 자원을 분리하기 위해.
  - **어디에?** `k8s/namespace.yaml`.

- **Deployment(디플로이먼트)**: 애플리케이션을 원하는 개수의 Pod로 유지하는 리소스.
  - **왜 필요?** 장애 시 자동 복구와 롤링 업데이트를 위해.
  - **어디에?** `k8s/gateway/deployment.yaml`, `k8s/redis/deployment.yaml`.

- **Pod(파드)**: Kubernetes에서 실행되는 가장 작은 단위(컨테이너 묶음).
  - **왜 필요?** 실제 앱이 구동되는 단위이기 때문.
  - **어디에?** Deployment가 Pod를 생성.

- **Service(서비스)**: 여러 Pod를 하나의 주소로 묶어주는 네트워크 엔드포인트.
  - **왜 필요?** Pod가 바뀌어도 동일한 주소로 접근하기 위해.
  - **어디에?** `k8s/gateway/service.yaml`, `k8s/redis/service.yaml`.

- **LoadBalancer**: 외부에서 접근 가능한 IP를 서비스에 붙여주는 방식.
  - **왜 필요?** 클러스터 밖에서도 접근 가능하게 하려고.
  - **어디에?** `k8s/gateway/service-lb.yaml`.

- **ConfigMap**: 설정 값을 담는 Kubernetes 리소스.
  - **왜 필요?** 설정과 코드를 분리해 운영하기 위해.
  - **어디에?** `k8s/gateway/configmap.yaml`.

- **Secret(시크릿)**: 비밀번호/키 같은 민감 정보를 담는 리소스.
  - **왜 필요?** 민감 정보를 안전하게 관리하기 위해.
  - **어디에?** `k8s/gateway/secret.yaml`.

- **HPA(Horizontal Pod Autoscaler)**: 트래픽에 따라 Pod 수를 자동 조절.
  - **왜 필요?** 부하가 많을 때 자동 확장하기 위해.
  - **어디에?** `k8s/gateway/hpa.yaml`.

- **Kustomize(커스터마이즈)**: 여러 K8s 파일을 묶어 쉽게 배포하는 도구.
  - **왜 필요?** 환경별 설정을 관리하기 위해.
  - **어디에?** `k8s/kustomization.yaml`, `kubectl apply -k k8s/`.

- **GPU 노드풀(GPU Pool)**: GPU가 장착된 노드만 묶어 운영하는 전용 풀.
  - **왜 필요?** 비용이 큰 GPU 자원을 일반 워크로드와 분리해 효율/안정성을 높이기 위해.
  - **어디에?** `nodeSelector`/`taints`로 분리 운영.

- **Overlay(오버레이)**: Kustomize에서 “기본 설정 위에 덧씌우는” 환경별 설정.
  - **왜 필요?** mock/gpu 같은 환경별 차이를 분리 관리하기 위해.
  - **어디에?** `k8s/overlays/`.

- **NodeSelector**: 특정 노드 라벨을 가진 노드에만 배치하는 규칙.
  - **왜 필요?** GPU 노드에만 모델 워커를 띄우기 위해.
  - **어디에?** `k8s/overlays/gpu/model-worker-deployment.yaml`.

- **Toleration**: 특정 taint가 있는 노드에 스케줄될 수 있게 하는 설정.
  - **왜 필요?** GPU 전용 노드에 워크로드를 허용하기 위해.
  - **어디에?** `k8s/overlays/gpu/model-worker-deployment.yaml`.

- **Taint(테인트)**: 특정 노드에 “아무나 올라오지 못하게” 거는 제한.
  - **왜 필요?** GPU 같은 전용 노드를 일반 워크로드로부터 보호하기 위해.
  - **어디에?** GPU 노드에 `NoSchedule` 등의 taint 적용.

- **HF_TOKEN(Hugging Face 토큰)**: Hugging Face에서 모델을 내려받기 위한 인증 토큰.
  - **왜 필요?** 승인(gated) 모델은 인증 없이는 다운로드가 불가.
  - **어디에?** `k8s/overlays/gpu/model-worker-secret.yaml`.

- **KServe**: Kubernetes 기반 모델 서빙 표준(추론 서비스 관리).
  - **왜 필요?** 모델 배포/롤백/트래픽 전환을 표준화하기 위해.
  - **어디에?** `k8s/kserve/`.

- **BentoML**: 모델 패키징/서빙을 위한 프레임워크.
  - **왜 필요?** 모델을 서비스로 쉽게 만들고 배포하기 위해.
  - **어디에?** `serving/bentoml/`.

- **Worker Scaffolding(워커 스캐폴딩)**: 실제 구현 전에 배포 구조/틀만 먼저 만드는 작업.
  - **왜 필요?** 운영 경로와 배포 구조를 미리 고정해 이후 구현 리스크를 줄이기 위해.
  - **어디에?** `k8s/overlays/gpu/sglang/`, `serving/bentoml/`.

- **Serving Standardization(서빙 표준화)**: 다양한 모델을 동일한 방식으로 배포/운영하는 체계.
  - **왜 필요?** 배포/모니터링/롤백을 표준화해 운영 비용을 낮추기 위해.
  - **어디에?** KServe/BentoML 도입 영역.

- **Kubeflow**: ML 파이프라인 실행/오케스트레이션 플랫폼.
  - **왜 필요?** 학습/검증/배포 단계를 자동화하기 위해.
  - **어디에?** `mlops/README.md`.

- **Argo CD**: GitOps 기반 배포 자동화 도구.
  - **왜 필요?** Git 변경을 배포에 자동 반영하기 위해.
  - **어디에?** `mlops/argocd/`, `mlops/README.md`.

- **Argo Workflows**: 쿠버네티스 배치 워크플로우 엔진.
  - **왜 필요?** 대용량 작업을 단계별로 실행/관리하기 위해.
  - **어디에?** `mlops/README.md`.

- **Airflow**: 배치/스케줄링 오케스트레이션 도구.
  - **왜 필요?** 정기 배치 작업(재학습 등)을 운영하기 위해.
  - **어디에?** `mlops/README.md`.

- **MLflow**: 모델 버전/메타데이터 관리(모델 레지스트리).
  - **왜 필요?** 모델 버전과 배포 이력을 관리하기 위해.
  - **어디에?** `mlops/README.md`.

- **GitOps(깃옵스)**: Git 저장소를 “배포의 단일 소스”로 삼는 운영 방식.
  - **왜 필요?** 변경 이력 추적과 자동 배포를 표준화하기 위해.
  - **어디에?** `mlops/argocd/` (Argo CD가 GitOps를 실행).

- **kind**: 로컬 PC에서 Kubernetes 클러스터를 빠르게 띄우는 도구.
  - **왜 필요?** 실제 클라우드 없이도 K8s 배포/검증을 하기 위해.
  - **어디에?** `kind create cluster` 로 실행.

- **Ingress Controller**: Ingress 규칙을 실제로 처리해 주는 “입구 관리자”.
  - **왜 필요?** Ingress만 만들면 동작하지 않고, 이를 처리할 컨트롤러가 꼭 필요.
  - **어디에?** kind 환경에서는 `ingress-nginx` 설치로 활성화.

- **MetalLB**: 로컬/온프레미스 K8s에서 LoadBalancer를 흉내 내는 구성요소.
  - **왜 필요?** kind 같은 로컬 클러스터에서 외부 IP를 붙이기 위해.
  - **어디에?** `kubectl apply -f metallb...`로 설치.

- **Node(노드)**: Kubernetes에서 실제로 컨테이너가 실행되는 서버(머신).
  - **왜 필요?** Pod가 배치되는 실제 실행 공간.
  - **어디에?** 클러스터의 워커 노드.

- **GPU Scheduling( GPU 스케줄링 )**: GPU가 있는 노드에만 특정 작업을 배치하는 것.
  - **왜 필요?** 모델 서빙은 GPU가 필요하기 때문.
  - **어디에?** `k8s/README.md`의 예시.

- **vLLM / SGLang / Triton**: LLM 모델을 빠르게 서빙하는 엔진(프레임워크).
  - **왜 필요?** 대규모 추론 성능 최적화를 위해.
  - **어디에?** 향후 모델 워커로 추가 예정(업스트림으로 연결).

---

# 작업 기록: FastAPI Gateway 골격 구현

## 작업 목적
- `plan.md`의 1번 실행 단계(게이트웨이 골격 구축)를 구현하기 위해 최소 기능이 동작하는 FastAPI 기반 Gateway를 추가했습니다.
- 인증/라우팅/Rate Limit/Circuit Breaker를 기본 동작 가능한 수준으로 마련하고 테스트로 확인했습니다.

## 구현 범위 요약
- FastAPI 기반 Gateway 패키지 구조 생성
- API Key 인증, 라우팅, Rate Limit, Circuit Breaker 기본 로직 구현
- Upstream 프록시 전송 및 mock upstream 지원
- 기본 엔드포인트 구성 및 테스트 추가
- Python 패키징과 실행 가이드 작성

## 파일/디렉터리 구성
- `gateway/app/main.py`
  - FastAPI 앱 생성 및 전체 요청 흐름 구성
  - 요청 ID/트레이스 ID 부여 미들웨어
  - `/health`, `/v1/chat/completions`, `/v1/circuit-breakers` 엔드포인트 제공
  - Lifespan 기반으로 HTTPX 클라이언트 생성/종료
- `gateway/app/core/config.py`
  - `GATEWAY_` 프리픽스 환경변수 설정 로딩
  - 업스트림 문자열(`name=url;...`) 파싱 로직 제공
- `gateway/app/core/security.py`
  - `X-API-Key` 또는 `Authorization: Bearer ...` 기반 인증
- `gateway/app/core/rate_limiter.py`
  - 인메모리 슬라이딩 윈도우 기반 Rate Limit
  - 남은 요청 수/리셋 시간을 계산해 헤더에 반영
- `gateway/app/core/circuit_breaker.py`
  - CLOSED/OPEN/HALF_OPEN 상태 전이
  - 실패 횟수 기반 차단 및 재시도 타이머
- `gateway/app/services/router.py`
  - 모델명 기반 업스트림 선택(없을 경우 기본 업스트림)
- `gateway/app/services/proxy.py`
  - 업스트림으로 POST 프록시 전송
  - `mock://` 스킴일 경우 더미 응답 반환
- `gateway/app/schemas.py`
  - 채팅 요청용 Pydantic 스키마 정의
- `gateway/pyproject.toml`
  - 패키징 및 의존성 정의
- `gateway/README.md`
  - 실행 방법, 설정 값, 예시 요청 정리
- `gateway/tests/test_gateway.py`
  - 인증 누락 시 401 확인
  - mock upstream 정상 응답 확인

## 동작 흐름 상세
1) 클라이언트 요청이 들어오면 `x-request-id`, `x-trace-id`를 생성/전파합니다.
2) `X-API-Key` 또는 Bearer 토큰을 검사해 인증합니다.
3) Rate Limit을 적용하고 남은 요청 수/리셋 시간 헤더를 내려줍니다.
4) 모델명에 맞는 업스트림을 선택합니다.
5) Circuit Breaker 상태를 확인해 OPEN이면 503 반환합니다.
6) 업스트림으로 요청을 프록시 전달합니다.
7) 실패 시 Circuit Breaker 실패를 기록하고 502 반환합니다.
8) 성공 시 Circuit Breaker 상태를 복구하고 응답을 반환합니다.

## 설정 값(환경변수)
- `GATEWAY_API_KEYS` (기본값: `dev-key`)
- `GATEWAY_RATE_LIMIT_PER_MINUTE` (기본값: `60`)
- `GATEWAY_CIRCUIT_BREAKER_MAX_FAILURES` (기본값: `5`)
- `GATEWAY_CIRCUIT_BREAKER_RESET_SECONDS` (기본값: `30`)
- `GATEWAY_REQUEST_TIMEOUT_SECONDS` (기본값: `10`)
- `GATEWAY_UPSTREAMS` (예: `llama=http://localhost:8001;mock=mock://local`)
- `GATEWAY_DEFAULT_UPSTREAM` (옵션)

## 테스트 결과
- `gateway` 디렉터리에서 `pytest` 실행
- 결과: 2 tests passed

## 현재 제약/가정
- Rate Limit과 Circuit Breaker는 인메모리로 동작합니다(분산 환경에서는 Redis/외부 상태 저장 필요).
- Mock upstream은 `mock://` 스킴으로만 지원합니다.
- 본 단계에서는 LiteLLM 통합, 메트릭/로그 수집, Docker 이미지화는 포함하지 않았습니다.

## 다음 단계 제안
- LiteLLM 라우팅/Failover 정책 구현
- Prometheus 메트릭 + 구조화 로그 추가
- Dockerfile/compose로 실행 환경 구성

---

# 작업 기록: LiteLLM 라우팅 및 Fallback 추가

## 작업 목적
- 다음 단계(멀티 모델 라우팅 및 Fallback 정책 구현)를 완료하기 위해 LiteLLM 업스트림과 실패 시 대체 모델로 전환되는 Fallback 로직을 추가했습니다.

## 구현 범위 요약
- LiteLLM 업스트림 지원(`litellm://` 스킴)
- 모델별 Fallback 체인 설정(`GATEWAY_FALLBACKS`)
- 실패 시 자동 전환 및 헤더 노출(`x-fallback-model`)
- 문서/테스트 업데이트

## 변경 파일
- `gateway/app/core/config.py`
  - `GATEWAY_FALLBACKS` 파싱 로직 추가
- `gateway/app/main.py`
  - Fallback 후보 리스트 구성 및 순차 시도
  - 실패 누적 시 에러 메시지 집계
  - fallback 사용 시 `x-fallback-model` 헤더 추가
- `gateway/app/services/proxy.py`
  - `litellm://` 스킴 지원
  - `mock://fail`로 강제 실패 시뮬레이션
- `gateway/pyproject.toml`
  - `litellm` 의존성 추가
- `gateway/tests/test_gateway.py`
  - 실패 시 fallback 정상 동작 확인 테스트 추가
- `gateway/README.md`
  - LiteLLM 업스트림 및 fallback 설정 예시 추가

## 동작 방식 상세
1) 요청 모델명을 기준으로 fallback 후보 리스트를 생성합니다.
2) 후보 순서대로 업스트림을 선택하고 Circuit Breaker 상태를 확인합니다.
3) 업스트림 호출 실패 시 다음 후보로 자동 전환합니다.
4) 대체 모델이 사용되면 `x-fallback-model` 헤더를 내려줍니다.
5) 모든 후보 실패 시 502 반환, 업스트림이 설정되지 않았을 경우 404 반환합니다.

## 환경변수 추가
- `GATEWAY_FALLBACKS`
  - 예: `llama=gpt-4o-mini,mock`

## 테스트 결과
- `gateway` 디렉터리에서 `pytest` 실행
- 결과: 3 tests passed

## 현재 제약/가정
- LiteLLM 호출은 라이브러리 설치 및 외부 API 키 설정이 필요합니다.
- Fallback 체인은 단순 순차 시도 방식이며, 라우팅 정책(AB/가중치)은 포함하지 않았습니다.

## 다음 단계 제안
- Prometheus 메트릭과 구조화 로그 추가
- Gateway Dockerfile/compose 구성
- UI ↔ Gateway 연결(서버 라우트 경유)

---

# 작업 기록: Prometheus 메트릭과 구조화 로그 추가

## 작업 목적
- 게이트웨이의 관측성을 높이기 위해 Prometheus 메트릭과 JSON 구조화 로그를 추가했습니다.

## 구현 범위 요약
- `/metrics` 엔드포인트 추가(Prometheus 형식)
- HTTP 요청/업스트림 호출에 대한 메트릭 수집
- JSON 구조화 로그 출력(요청/응답, 에러)
- 관련 테스트 및 문서 업데이트

## 변경 파일
- `gateway/app/core/metrics.py`
  - 요청/업스트림/Rate Limit/Circuit/Fallback 메트릭 정의
- `gateway/app/core/logging.py`
  - JSON 로그 포맷터 및 로거 설정
- `gateway/app/main.py`
  - 요청 미들웨어에서 메트릭/로그 수집
  - `/metrics` 엔드포인트 추가
  - 업스트림 성공/실패, fallback 사용 시 메트릭 기록
- `gateway/tests/test_gateway.py`
  - `/metrics` 응답 테스트 추가
- `gateway/README.md`
  - Observability 섹션 추가
- `gateway/pyproject.toml`
  - `prometheus-client` 의존성 추가

## 수집 메트릭 목록
- `gateway_requests_total` (method/path/status)
- `gateway_request_latency_seconds` (method/path)
- `gateway_in_flight_requests`
- `gateway_upstream_requests_total` (upstream/status)
- `gateway_upstream_latency_seconds` (upstream)
- `gateway_rate_limited_total`
- `gateway_circuit_open_total` (upstream)
- `gateway_fallback_used_total` (from_model/to_model)

## 로그 출력 필드(주요)
- `timestamp`, `level`, `message`, `logger`
- `request_id`, `trace_id`, `method`, `path`, `status`, `duration_ms`
- `upstream`, `fallback_model`, `client_ip`
- 에러 발생 시 `exc_info`

## 테스트 결과
- `gateway` 디렉터리에서 `pytest` 실행
- 결과: 4 tests passed

## 현재 제약/가정
- 메트릭은 단일 프로세스 기준으로 수집됩니다(멀티 프로세스 환경은 별도 구성 필요).
- 로그는 표준 출력(JSON)으로만 제공합니다.

## 다음 단계 제안
- 구조화 로그에 사용자/모델별 샘플링 정책 추가
- Prometheus/Grafana 대시보드 스케치 작성
- Docker/compose 구성 및 관측 스택 연결

---

# 작업 기록: Gateway Docker/Compose 구성

## 작업 목적
- 로컬에서 Gateway + Prometheus + Grafana를 빠르게 실행할 수 있도록 Docker/Compose 구성을 추가했습니다.

## 구현 범위 요약
- Gateway 컨테이너 이미지용 Dockerfile 추가
- Prometheus/Grafana와 함께 실행하는 docker-compose 구성
- Prometheus 스크랩 설정 및 Grafana 데이터소스 자동 프로비저닝
- 실행 방법 문서화

## 변경 파일
- `gateway/Dockerfile`
  - Gateway 컨테이너 이미지 빌드 정의
- `docker-compose.yml`
  - Gateway/Prometheus/Grafana 스택 구성
- `ops/prometheus.yml`
  - Gateway `/metrics` 스크랩 설정
- `ops/grafana/provisioning/datasources/datasource.yml`
  - Grafana에서 Prometheus 데이터소스 자동 등록
- `gateway/README.md`
  - Docker quick start 섹션 추가

## 실행 방법
```bash
docker compose up --build
```

## 접속 주소
- Gateway: http://localhost:8000
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / admin)

## 현재 제약/가정
- 기본 업스트림은 `mock://`로 설정되어 있습니다.
- Grafana 대시보드는 아직 제공되지 않으며 데이터소스만 자동 등록됩니다.

## 다음 단계 제안
- Grafana 기본 대시보드 추가
- 실서비스 업스트림(vLLM) 연동 예시 제공

---

# 작업 기록: Grafana 기본 대시보드 추가

## 작업 목적
- Prometheus 메트릭을 시각화할 수 있도록 Grafana 대시보드를 자동 프로비저닝으로 추가했습니다.

## 구현 범위 요약
- Grafana 대시보드 프로비저닝 설정 추가
- Nexus Gateway 기본 대시보드 JSON 생성
- 데이터소스 UID 고정하여 대시보드 연결 안정화
- 문서에 대시보드 위치 안내 추가

## 변경 파일
- `ops/grafana/provisioning/dashboards/dashboards.yml`
  - 대시보드 자동 로드 설정
- `ops/grafana/provisioning/dashboards/nexus-gateway.json`
  - Nexus Gateway 기본 대시보드 정의
- `ops/grafana/provisioning/datasources/datasource.yml`
  - Prometheus 데이터소스 UID 지정
- `gateway/README.md`
  - Grafana 대시보드 안내 추가

## 대시보드 구성
- Requests per second
- 5xx error rate
- Request latency p95
- Upstream latency p95
- Upstream errors
- Rate limited requests
- Circuit open
- Fallback usage
- In-flight requests

## 실행 방법
```bash
docker compose up --build
```

## 접속
- Grafana: http://localhost:3000 (admin / admin)
- 대시보드: "Nexus Gateway" (자동 등록)

## 다음 단계 제안
- 대시보드 알람 룰 추가
- 서비스/테넌트별 라벨 확장

---

# 작업 기록: vLLM 연결 가이드 및 Compose 추가

## 작업 목적
- 모델 서빙 엔진 단계의 시작으로 vLLM 실행/연결 방법을 문서화하고, Docker Compose로 연동할 수 있도록 구성했습니다.

## 구현 범위 요약
- vLLM 실행 가이드 및 로컬 스크립트 추가
- vLLM 포함 Compose override 파일 추가
- Gateway 문서에 vLLM Compose 실행 방법 추가

## 변경 파일
- `serving/vllm/README.md`
  - vLLM 로컬/도커 실행 및 Gateway 연동 예시
- `serving/vllm/run_local.sh`
  - vLLM OpenAI API 서버 실행 스크립트
- `docker-compose.vllm.yml`
  - vLLM 서비스와 Gateway 연동용 Compose override
- `gateway/README.md`
  - vLLM Compose 실행 방법 추가

## 실행 방법
```bash
MODEL_ID=meta-llama/Meta-Llama-3-8B-Instruct \
  docker compose -f docker-compose.yml -f docker-compose.vllm.yml up --build
```

## 현재 제약/가정
- GPU가 있는 환경과 NVIDIA container runtime이 필요합니다.
- 모델 가중치 다운로드에 시간이 걸릴 수 있습니다.

## 다음 단계 제안
- vLLM/SGLang/Triton 성능 비교 스크립트 추가
- K8s 배포 매니페스트 초안 작성

---

# 작업 기록: vLLM Healthcheck 추가

## 작업 목적
- vLLM 서비스가 준비되었는지 확인할 수 있도록 Docker Compose에 healthcheck를 추가했습니다.

## 변경 파일
- `docker-compose.vllm.yml`
  - `/v1/models` 엔드포인트로 상태 확인 healthcheck 추가

## 동작 방식
- 컨테이너 내부에서 `python -c`로 `/v1/models` 호출
- 호출이 성공하면 healthy, 실패하면 unhealthy로 표시

---

# 작업 기록: Redis 기반 Rate Limiting 도입

## 작업 목적
- Gateway의 Rate Limit을 분산 환경에서도 동작하도록 Redis 백엔드를 추가했습니다.

## 구현 범위 요약
- In-memory RateLimiter를 async로 변경
- Redis 기반 RateLimiter 추가
- Redis 장애 시 fail-open 로그 처리
- 설정/문서 업데이트

## 변경 파일
- `gateway/app/core/rate_limiter.py`
  - RedisRateLimiter 및 RateLimitBackendError 추가
  - 기존 RateLimiter를 async로 변경
- `gateway/app/core/config.py`
  - `GATEWAY_REDIS_URL` 설정 추가
- `gateway/app/main.py`
  - Redis 사용 여부에 따라 rate limiter 생성
  - rate limit backend 오류 로그 처리
- `gateway/README.md`
  - Redis 설정 문서화

## 설정 값
- `GATEWAY_REDIS_URL` (예: `redis://localhost:6379/0`)

## 현재 제약/가정
- Redis 연결 실패 시 요청은 허용되며 로그에 오류가 남습니다.

---

# 작업 기록: Auth 정책 강화 및 라우팅 정책 추가

## 작업 목적
- API Key/JWT 인증 정책을 강화하고, 모델 요청에 대해 가중치/카나리 라우팅을 지원하도록 개선했습니다.

## 구현 범위 요약
- API Key 정책(JSON) 지원: 허용 모델/개별 Rate Limit
- JWT 검증 지원(HS256/RS256)
- 가중치/카나리/직접 라우팅 정책 추가
- 관련 설정 및 문서/테스트 업데이트

## 변경 파일
- `gateway/app/core/security.py`
  - JWT 검증 및 API Key 정책 적용
  - AuthContext 추가
- `gateway/app/core/config.py`
  - `GATEWAY_API_KEY_POLICIES`, `GATEWAY_ROUTE_POLICIES`, JWT 설정 추가
- `gateway/app/services/router.py`
  - weighted/canary/direct 라우팅 정책 구현
- `gateway/app/core/rate_limiter.py`
  - per-key override 지원
- `gateway/app/main.py`
  - JWT/정책 기반 인증 및 모델 접근 제어 반영
- `gateway/tests/test_gateway.py`
  - 라우팅 정책 및 JWT 테스트 추가
- `gateway/README.md`
  - 정책/라우팅/JWT 설정 예시 추가
- `gateway/pyproject.toml`
  - `pyjwt` 의존성 추가

## 설정 예시
```bash
GATEWAY_API_KEY_POLICIES='{"dev-key": {"allowed_models":["chat"], "rate_limit_per_minute": 30}}'
GATEWAY_ROUTE_POLICIES='{"chat": {"strategy":"canary","primary":"primary","canary":"canary","percent":5}}'
GATEWAY_JWT_SECRET="my-secret"
```

## 테스트 결과
- `pytest` 실행 기준: 기존 테스트 + JWT/라우팅 테스트 통과

## 현재 제약/가정
- 라우팅 정책의 target 이름은 `GATEWAY_UPSTREAMS`에 정의된 이름과 일치해야 합니다.
- JWT는 설정된 키/알고리즘에 따라 유효성 검증만 수행합니다.

---

---

# 작업 기록: Kubernetes 배포 초안 추가

## 작업 목적
- 3단계(쿠버네티스 인프라 이식)를 시작하기 위해 Gateway와 Redis의 K8s 배포 초안을 마련했습니다.

## 구현 범위 요약
- Namespace, Gateway, Redis, HPA 리소스 작성
- ConfigMap/Secret 기반 환경 변수 구성
- Kustomize 적용 가능하도록 구성

## 변경 파일
- `k8s/namespace.yaml`
- `k8s/gateway/configmap.yaml`
- `k8s/gateway/secret.yaml`
- `k8s/gateway/deployment.yaml`
- `k8s/gateway/service.yaml`
- `k8s/gateway/hpa.yaml`
- `k8s/redis/deployment.yaml`
- `k8s/redis/service.yaml`
- `k8s/kustomization.yaml`
- `k8s/README.md`

## 실행 방법
```bash
kubectl apply -k k8s/
```

## 현재 제약/가정
- Gateway 이미지 이름은 로컬 빌드 기준이며, 실제 레지스트리 이미지로 변경 필요합니다.
- Redis는 단일 인스턴스이며 HA 구성은 추후 적용합니다.

## 다음 단계 제안
- Gateway 이미지 빌드/푸시 파이프라인 추가
- 모델 워커(vLLM/SGLang/Triton) K8s 매니페스트 확장

---

# 작업 기록: Gateway 이미지 빌드/푸시 스크립트 추가

## 작업 목적
- Kubernetes 배포를 위해 Gateway 이미지를 레지스트리에 빌드/푸시하고, 배포 이미지 업데이트를 쉽게 하도록 스크립트를 추가했습니다.

## 변경 파일
- `ops/build_push_gateway.sh`
  - Gateway 이미지 빌드 및 레지스트리 푸시
- `ops/k8s_set_gateway_image.sh`
  - K8s deployment 이미지 업데이트
- `k8s/README.md`
  - 빌드/푸시/업데이트 방법 문서화

## 사용 방법
```bash
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/build_push_gateway.sh
IMAGE_REPO=ghcr.io/your-org/nexus-gateway IMAGE_TAG=latest ./ops/k8s_set_gateway_image.sh
```

---

# 작업 기록: Gateway 서비스 노출(Ingress/LoadBalancer) 추가

## 작업 목적
- Kubernetes에서 Gateway를 외부에 노출하기 위해 Ingress 및 LoadBalancer 옵션을 추가했습니다.

## 변경 파일
- `k8s/gateway/ingress.yaml`
  - NGINX Ingress 기반 호스트 노출 (gateway.local)
- `k8s/gateway/service-lb.yaml`
  - LoadBalancer 타입 서비스
- `k8s/kustomization.yaml`
  - 신규 리소스 포함
- `k8s/README.md`
  - 노출 방법 설명 추가

## 사용 방법
- Ingress 사용 시: `gateway.local` 도메인을 로컬 DNS/hosts에 연결
- LoadBalancer 사용 시: 클라우드 환경에서 외부 IP 할당

## 주의사항
- 둘 중 하나만 쓰려면 `k8s/kustomization.yaml`에서 다른 리소스를 제거하세요.

---

# 작업 기록: kind 로컬 K8s 검증 및 API Key 파싱 개선

## 작업 목적
- Mac 환경에서 로컬 K8s(kind)로 배포가 실제로 동작하는지 확인했습니다.
- `GATEWAY_API_KEYS` 환경변수가 단순 문자열일 때도 정상 동작하도록 파싱 방식을 개선했습니다.

## 변경 내용
- Gateway 설정에서 API Key를 문자열/콤마 구분으로 받아도 동작하도록 파싱 로직을 수정.

## 확인 방법(실행)
- kind 클러스터 생성 후 `kubectl apply -k k8s/`로 배포.
- Ingress 사용을 위해 `ingress-nginx` 컨트롤러 설치.
- Port-forward로 `/health` 응답 확인:
  - `kubectl port-forward -n nexus svc/nexus-gateway 8000:80`
  - `curl http://localhost:8000/health`
  - `kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80`
  - `curl -H 'Host: gateway.local' http://localhost:8080/health`

## 결과
- `/health`가 정상 응답해 Gateway가 실행 중임을 확인.
- kind 환경에서는 LoadBalancer가 `<pending>` 상태이므로, Ingress/Port-forward 방식으로 검증함.

---

# 작업 기록: kind에서 MetalLB로 LoadBalancer 테스트 경로 정리

## 작업 목적
- 로컬 kind 환경에서도 LoadBalancer 서비스를 테스트할 수 있도록 MetalLB 설정 방법을 문서화했습니다.

## 변경 파일
- `k8s/README.md`
  - MetalLB 설치, IP 풀 설정, EXTERNAL-IP 확인 절차 추가

## 핵심 요약
- kind는 기본적으로 LoadBalancer가 `<pending>` 상태라 외부 IP가 생기지 않습니다.
- MetalLB를 설치하고 IP 풀을 지정하면 로컬에서도 LoadBalancer IP를 받을 수 있습니다.

## 검증 결과
- `nexus-gateway-lb`에 EXTERNAL-IP가 할당됨(예: `172.20.255.200`).
- Mac(Docker Desktop) 환경에서는 해당 IP가 호스트에서 바로 열리지 않을 수 있어, 필요 시 Ingress/Port-forward로 확인.

---

# 작업 기록: 모델 워커(mock) 추가 및 K8s 연결

## 작업 목적
- GPU 없이도 Gateway ↔ 모델 워커 구조를 K8s에서 검증할 수 있도록 CPU 기반 mock 워커를 추가했습니다.

## 변경 파일
- `serving/mock-worker/`
  - OpenAI 호환 `/v1/chat/completions` 제공
- `k8s/model-worker/deployment.yaml`
- `k8s/model-worker/service.yaml`
- `k8s/kustomization.yaml`
- `k8s/gateway/configmap.yaml`
  - 기본 업스트림을 `model-worker`로 연결
- `k8s/README.md`
  - kind 환경에서 워커 이미지 빌드/로드 안내 추가

## 사용 흐름(요약)
1) `nexus-model-worker` 이미지를 빌드하고 kind에 로드
2) `kubectl apply -k k8s/`로 Gateway + Worker 배포
3) Gateway가 `model-worker`로 요청을 전달

---

# 작업 기록: GPU 오버레이 스캐폴딩 추가

## 작업 목적
- mock 환경과 GPU 환경을 분리하기 위해 Kustomize overlay 구조를 추가했습니다.

## 변경 파일
- `k8s/overlays/mock/kustomization.yaml`
- `k8s/overlays/gpu/kustomization.yaml`
- `k8s/overlays/gpu/model-worker-deployment.yaml`
  - vLLM 이미지 + GPU 리소스 + nodeSelector/toleration 설정
- `k8s/overlays/gpu/gateway-configmap.yaml`
  - GPU 워커 업스트림 이름을 `vllm`로 분리
- `k8s/README.md`
  - overlay 적용 방법 문서화

## 사용 흐름(요약)
1) mock: `kubectl apply -k k8s/overlays/mock`
2) gpu: `kubectl apply -k k8s/overlays/gpu` (GPU 노드 필요)

---

# 작업 기록: GPU 워커 매니페스트 현실화 + SGLang 스켈레톤 추가

## 작업 목적
- GPU 환경에서 vLLM 워커를 실제 운영에 가까운 형태로 구성하고,
- SGLang 보조 워커를 추가할 수 있는 스켈레톤을 마련했습니다.

## 변경 파일
- `k8s/overlays/gpu/model-worker-deployment.yaml`
  - vLLM 이미지, GPU 리소스, 캐시 볼륨, startupProbe 추가
- `k8s/overlays/gpu/model-worker-secret.yaml`
  - `HF_TOKEN` 준비용 시크릿
- `k8s/overlays/gpu/sglang/`
  - SGLang 보조 워커 템플릿(이미지/엔트리포인트는 실제 환경에 맞게 교체)
- `k8s/README.md`
  - GPU 워커 설정 및 SGLang 적용 방법 안내

## 요약
- vLLM은 기본 엔진으로 운영 가능한 수준의 매니페스트로 보강.
- SGLang은 보조 엔진이므로 별도 overlay로 필요할 때만 적용.

---

# 작업 기록: vLLM + SGLang 라우팅 예시 추가

## 작업 목적
- 두 엔진을 함께 사용할 때 Gateway 라우팅 정책 예시를 제공했습니다.

## 변경 파일
- `k8s/README.md`

## 요약
- `GATEWAY_UPSTREAMS`와 `GATEWAY_ROUTE_POLICIES` 예시를 추가.
- 요청의 `model` 값과 정책 키가 동일해야 함을 명시.

---

# 작업 기록: GPU 노드풀 운영 가이드 추가

## 작업 목적
- GPU 노드풀을 안정적으로 운영하기 위한 기본 규칙을 문서화했습니다.

## 변경 파일
- `k8s/README.md`

## 요약
- GPU 노드풀 분리, `nodeSelector`/`tolerations` 적용 기준 추가.
- 세대별(A100/H100/B300) 노드풀 분리 운영 팁 정리.

---

# 작업 기록: KServe/BentoML 스캐폴딩 추가

## 작업 목적
- 서빙 표준화를 위한 KServe 템플릿과 BentoML 워커 스캐폴딩을 마련했습니다.

## 변경 파일
- `k8s/kserve/inferenceservice.yaml`
- `k8s/kserve/README.md`
- `serving/bentoml/README.md`
- `k8s/README.md`

## 요약
- KServe InferenceService 템플릿 추가
- BentoML은 구조만 잡고 실제 서비스 구현은 추후 진행

---

# 작업 기록: MLOps 스캐폴딩 문서 추가

## 작업 목적
- 4단계(Kubeflow/Argo/MLflow) 진행을 위한 기본 문서 틀을 추가했습니다.

## 변경 파일
- `mlops/README.md`

## 요약
- 데이터 검증 → 양자화 → 모델 등록 → 배포 흐름을 정리
- Kubeflow/Argo CD/Argo Workflows/Airflow/MLflow 역할을 요약

---

# 작업 기록: Kubeflow 파이프라인 템플릿 추가

## 작업 목적
- 4단계 첫 단계로, ML 파이프라인의 최소 템플릿을 추가했습니다.

## 변경 파일
- `mlops/kubeflow/pipeline.yaml`
- `mlops/README.md`

## 요약
- 데이터 검증 → 양자화 → 모델 등록 → 배포 순서의 기본 템플릿 추가

---

# 작업 기록: Argo CD 앱 스캐폴딩 추가

## 작업 목적
- GitOps 기반 배포를 위한 Argo CD Application 템플릿을 추가했습니다.

## 변경 파일
- `mlops/argocd/application.yaml`
- `mlops/argocd/README.md`
- `mlops/README.md`

## 요약
- Argo CD에서 Kustomize overlay를 배포할 수 있는 기본 템플릿 제공

---

# 작업 기록: 모델 워커 HPA 추가

## 작업 목적
- 모델 워커도 트래픽에 따라 자동 확장할 수 있도록 HPA를 추가했습니다.

## 변경 파일
- `k8s/model-worker/hpa.yaml`
- `k8s/kustomization.yaml`
- `k8s/README.md`

## 요약
- CPU 사용률 70% 기준으로 1~3개 Pod 사이에서 자동 확장되도록 설정.

---

# 작업 기록: 서빙 엔진 선택 정리 (vLLM 기본, SGLang 보조)

## 작업 목적
- 서빙 엔진을 통일해 운영 복잡도를 줄이고, 필요한 경우에만 보조 엔진을 사용하는 전략을 확정했습니다.

## 결정 요약
- **기본 엔진: vLLM**
- **보조 엔진: SGLang**
- **Triton: 보류**

## 비교 요약
- **vLLM**: 동시 요청 처리와 메모리 효율이 뛰어나고 OpenAI 호환 API 운영이 쉬움
- **SGLang**: 복잡한 프롬프트/워크플로우 제어에 유리
- **Triton**: 다양한 모델을 통합 서빙할 때 유리하지만 운영 복잡도 높음

## 선택 이유
- vLLM으로 **성능/운영 효율**을 확보하고,
- SGLang은 **특수한 고급 제어**가 필요한 경우에만 사용해 복잡도를 최소화,
- Triton은 **LLM 외 모델 통합 요구가 생길 때** 도입하는 방식으로 단계적 접근.
