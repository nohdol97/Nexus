# Enterprise AI Platform: Nexus

> [!abstract] 개요
> 토스증권 ML 플랫폼 엔지니어를 목표로 하는 고가용성 LLM 추론 플랫폼 구축 프로젝트입니다. [[FastAPI]], [[vLLM]], [[Kubernetes]], [[Kubeflow]] 등 현대적인 MLOps 스택을 활용하여 실제 엔터프라이즈 환경의 AI 인프라를 설계합니다.

---

## 🏗️ 전체 아키텍처

- **Client/Service → Gateway**: [[FastAPI]] + [[LiteLLM]] 기반 인증/라우팅/Rate Limit/Circuit Breaker/Fallback
- **Gateway → Serving**: [[vLLM]] (기본) + [[SGLang]] (보조) 기반 LLM 서빙 계층
- **Serving → Platform**: [[Kubernetes]]에서 [[HPA]] 및 GPU Scheduling 적용
- **Serving Abstraction**: [[KServe]] / [[BentoML]]로 표준화된 배포/롤백 지원
- **MLOps**: [[Kubeflow]] + [[ArgoCD]] + [[Argo Workflows]] + [[Airflow]] 파이프라인
- **Observability/Logging**: [[Prometheus]] + [[Grafana]] + [[Kafka]] → [[Elasticsearch]] / [[Kibana]]

## ✅ 엔진 선택 요약

- **기본 엔진: vLLM**
  - 대규모 동시 요청 처리와 OpenAI 호환 API 운영에 유리
  - 운영 복잡도를 낮추면서도 성능 효율이 높음
- **보조 엔진: SGLang**
  - 복잡한 프롬프트/워크플로우 제어가 필요한 경우에만 선택
- **Triton: 보류**
  - LLM 외 다양한 모델을 통합 서빙해야 할 때 고려

## ⚖️ vLLM / SGLang / Triton 비교 요약

- **vLLM**: 고속 처리, 동시성/메모리 효율 강점, OpenAI 호환 API 제공이 쉬움 → 운영 기본 엔진에 적합
- **SGLang**: 복잡한 프롬프트/워크플로우 제어 강점 → 특정 고급 시나리오 보조 엔진에 적합
- **Triton**: LLM 외 다양한 모델 통합 서빙에 강점, 운영 복잡도 높음 → 멀티모달/다모델 통합 시 고려

## ✅ 선택 이유 정리

- **운영 단순화 + 성능 효율**을 위해 vLLM을 기본 엔진으로 채택
- **복잡한 오케스트레이션이 필요한 일부 요청**만 SGLang으로 처리해 유연성 확보
- Triton은 **LLM 외 대규모 모델 통합 필요성이 생길 때**로 보류하여 현재 복잡도를 낮춤

## 🎯 JD 매칭 포인트

- **Gateway 역량**: FastAPI 기반 인증/라우팅/트래픽 제어, Circuit Breaker/Fallback 설계
- **서빙 운영**: vLLM/SGLang/Triton 기반 LLM 서빙 및 K8s 운영, GPU 자원 최적화
- **플랫폼 운영**: Kubeflow/ArgoCD 중심 ML 파이프라인 구축 및 배포 자동화
- **관측/로그**: Prometheus/Grafana 지표와 Kafka/ELK 로그 파이프라인 연동
- **운영 개선**: 장애 분석 및 근본 원인 개선을 위한 SLO/Runbook 기반 운영

## 🚀 5단계 상세 로드맵

### 1단계: 모델 서빙 엔진 구축 (Core Engine)
가장 먼저 AI 모델이 실제로 구동되는 '엔진' 부분을 구축합니다.
- **기술 스택**: [[Python]], [[vLLM]](기본), [[SGLang]](보조), [[Triton]](보류) <- GPU 환경 필요
- **주요 구현**:
	- [[Llama 3]] 또는 Mistral 오픈소스 모델을 vLLM 엔진으로 실행
	- 분산 서빙(Distributed Serving) 환경 구성을 통한 확장성 확보
	- SGLang을 활용한 vLLM과의 Throughput/Latency 비교 분석 및 최적화

### 2단계: 지능형 API Gateway 개발 (The Brain)
다양한 요청을 처리하고 장애에 대응하는 지능형 인터페이스를 만듭니다.
- **기술 스택**: [[FastAPI]], [[LiteLLM]], [[Redis]]
- **주요 구현**:
	- **Unified Interface**: LiteLLM 내장으로 자체 모델과 외부 API(OpenAI, Claude)를 단일 엔드포인트로 통합
	- **Fallback & Retry**: 자체 서버 장애 시 외부 API로 자동 전환되는 Failover 로직
	- **Rate Limiting**: Redis 연동을 통한 사용자별/Key별 호출 제어
	- **Auth & Routing**: API Key/JWT 기반 인증 및 정책 기반 라우팅(AB/Canary)
	- **Circuit Breaker & Load Shedding**: 장애 격리와 과부하 제어

### 3단계: 쿠버네티스 인프라 이식 (Foundation)
시스템을 개별 서버가 아닌 클라우드 네이티브 환경으로 전환합니다.
- **기술 스택**: [[Kubernetes]], [[Docker]], [[KServe]], [[BentoML]]
- **주요 구현**:
	- Gateway 및 Model Worker의 컨테이너화 및 [[K8s]] 배포
	- **Auto Scaling**: [[HPA]] 설정을 통한 트래픽 기반 Pod 자동 확장
	- **GPU Scheduling**: 효율적인 리소스 할당을 위한 K8s 스케줄링 전략 학습
	- **GPU Node Pool**: A100/H100/B300 등 노드 풀 운영 전략 수립

### 4단계: Kubeflow 기반 MLOps 자동화 (Workflow)
모델 배포의 전 과정을 자동화 파이프라인으로 연결합니다.
- **기술 스택**: [[Kubeflow]], [[ArgoCD]], [[Argo Workflows]], [[Airflow]], [[MLflow]]
- **주요 구현**:
	- **ML Pipeline**: [데이터 검증 → 양자화(Quantization) → 모델 등록(MLflow) → K8s 배포(KServe/BentoML)] 구축
	- **Workflow Orchestration**: Argo Workflows/Airflow 기반 배치 및 스케줄링
	- **Canary Deployment**: 점진적 트래픽 전환 시나리오 구현 및 검증

### 5단계: 가시성 확보 및 최적화 (Observability)
시스템 상태를 데이터로 파악하고 성능을 극대화합니다.
- **기술 스택**: [[Prometheus]], [[Grafana]], [[Kafka]], [[Elasticsearch]], [[Kibana]]
- **주요 구현**:
	- Latency, TPS, GPU 사용량 등 핵심 지표(Golden Signals) 수집
	- [[Grafana]] 대시보드 시각화 및 장애 알림 체계 구축
	- **Logging Pipeline**: Kafka → Elasticsearch/Kibana 로그 수집 및 상관 분석
	- **SLO/Runbook**: 운영 기준(SLO)과 장애 대응 Runbook 정립
	- 수집 데이터를 바탕으로 vLLM Batch size 등 파라미터 튜닝 리포트 작성

---

## 🔧 추가로 강화하면 좋은 항목 (단계별)

### 단계 A (단기 · 운영 안정화)
- **MSA 통신**: REST/gRPC 기반 서비스 간 통신 및 트랜잭션 처리 설계
- **보안 강화**: mTLS/서비스 간 인증, PII 마스킹, 감사 로그 표준화
- **트래픽 안전장치**: Shadow Traffic(미러링) + 안정성 검증 흐름 추가
- **부하/장애 테스트**: 부하 테스트 시나리오와 장애 주입(Chaos) 최소 세트

### 단계 B (중기 · 서빙/인프라 고도화)
- **고급 라우팅**: disaggregated serving, prefix-aware routing, context caching 적용
- **K8s 확장**: Operator/Scheduler 커스터마이징으로 GPU 효율 최적화
- **배포 전략**: Blue/Green + Canary 운영 시나리오 표준화
- **비용 최적화(FinOps)**: GPU 사용량 기반 비용 리포트 및 정책 수립

### 단계 C (장기 · 플랫폼 확장)
- **Public Cloud**: AWS SageMaker/Bedrock 또는 Azure AI 환경 비교 검토
- **학습 파이프라인**: 금융 도메인 대규모 학습/재학습 환경 구축
- **DR(재해 복구)**: 멀티 리전/백업 복구 전략 수립
- **데이터 거버넌스**: 데이터 품질/버전/접근 제어 체계 수립

## 🧩 실 구현 체크리스트 (계획 → 실행)

### Agent 통합 사용 시나리오 (1 + 2 + 3 포함)
- **외부 Agent 클라이언트(1)**
  - Gateway 호출용 샘플 SDK/CLI 제공 (REST)
  - API Key/JWT 발급 및 테스트 흐름 문서화
  - Request/Trace ID 전달 규칙과 재시도 정책 명시
- **내부 서비스 간 gRPC Agent(2)**
  - gRPC 서버/클라이언트 실제 연결 (proto codegen 포함)
  - 계약 테스트(요청/응답/에러/타임아웃)
  - 서비스 간 인증(내부 JWT 또는 mTLS) 적용
- **LLM 서빙 연동 Agent(3)**
  - vLLM 기본 엔진 연동 (GPU 환경)
  - SGLang 보조 엔진 연동 + 라우팅 정책
  - 서빙 엔진 헬스체크 및 장애 시 Fallback 경로 확정
  - 서빙 성능/비용 리포트(Throughput, Latency, GPU Util)

### 단계 A (단기 · 운영 안정화)
- **MSA 통신**
  - gRPC 서버/클라이언트 실제 연결 (proto codegen 포함)
  - REST 계약 테스트(에러 포맷, idempotency, timeout)
  - Request/Trace ID 전파 검증 테스트
- **보안 강화**
  - mTLS 도입 경로 결정(Istio/Linkerd 또는 Ingress 종단)
  - 인증서 발급/회전/폐기 정책 문서화 + 테스트
  - PII 마스킹 단위 테스트 + 감사 로그 필드 검증
  - 감사 로그를 Kafka/Elasticsearch 파이프라인으로 적재
- **Shadow Traffic**
  - Shadow 정책(비율/타겟) 설정값 추가
  - 비동기 미러링 전송 구현 및 실패 메트릭 추가
  - Shadow 결과 저장/비교 경로 정의
- **부하/Chaos 테스트**
  - k6 Baseline/Spike 스크립트 추가
  - Chaos 주입 토글(업스트림 지연/다운) 테스트 플래그
  - 기준 SLO/성공 기준 정의 및 리포트 자동화

### 단계 B (중기 · 서빙/인프라 고도화)
- **고급 라우팅**
  - prefix-aware routing 정책 스펙 확정 + 구현
  - context caching 설계(캐시 키/만료/용량) + PoC
  - disaggregated serving 경로 설계 + 성능 비교
- **K8s 확장**
  - GPU 스케줄러/오퍼레이터 PoC
  - 노드풀/taints/affinity 최적화 가이드 + 검증
- **배포 전략**
  - Blue/Green + Canary 표준 흐름(Argo Rollouts/KServe) 적용
  - 롤백/장애 시나리오 리허설
- **비용 최적화(FinOps)**
  - GPU 사용량/요금 추정 리포트 템플릿
  - 비용 알림 기준/정책 정의

### 단계 C (장기 · 플랫폼 확장)
- **Public Cloud**
  - AWS/Azure POC 환경 구축 및 비교 리포트
  - 보안/네트워크/비용 구조 비교표 작성
- **학습 파이프라인**
  - 데이터 버전 관리 + 학습 파이프라인 자동화
  - 재학습 트리거/검증/배포 흐름 확정
- **DR(재해 복구)**
  - 멀티 리전 백업/복구 절차 문서화
  - 복구 리허설(테스트) 시나리오 실행
- **데이터 거버넌스**
  - 데이터 품질/스키마 검증 룰 정의
  - 접근 제어/감사 정책 확정

## 📝 이력서 하이라이트 (Key Achievements)

> [!tip] 성과 중심 요약
> - **고가용성 플랫폼**: Kubeflow 및 K8s 기반 LLM 추론 플랫폼 구축으로 운영 공수 50% 절감
> - **장애 복구**: FastAPI & LiteLLM 기반 Fallback 시스템 설계로 서비스 연속성 확보
> - **성능 최적화**: vLLM 서빙 최적화를 통한 추론 속도 2배 향상 및 GPU 활용률 극대화
> - **모니터링**: Prometheus 기반 실시간 관측 체계를 통한 MTTD(장애 인지 시간) 단축
