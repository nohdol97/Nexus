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

- **SDK(Software Development Kit)**: 특정 API를 쉽게 쓰도록 도와주는 라이브러리 묶음.
  - **왜 필요?** 외부 Agent가 Gateway를 쉽게 호출하도록 하기 위해.
  - **어디에?** `plan.md` Agent 통합 항목.

- **CLI(Command Line Interface)**: 터미널에서 명령으로 실행하는 방식.
  - **왜 필요?** 간단한 테스트/운영 작업을 빠르게 하기 위해.
  - **어디에?** `docs/cli_commands_guide.md`, `plan.md` Agent 통합 항목.

- **SDK(샘플 클라이언트)**: 외부 Agent가 쉽게 호출하도록 제공하는 예제 클라이언트/스크립트.
  - **왜 필요?** 빠른 연동과 테스트를 위해.
  - **어디에?** `docs/agent_client_guide.md`, `gateway/scripts/agent_client_smoke.sh`.

- **MSA(Microservices Architecture, 마이크로서비스 아키텍처)**: 큰 서비스를 여러 개의 작은 서비스로 분리해 운영하는 방식.
  - **왜 필요?** 서비스별 독립 배포/확장/장애 격리가 쉬워짐.
  - **어디에?** `docs/msa_communication.md`의 통신 원칙.

- **REST**: HTTP 기반의 서비스 통신 규칙(JSON 요청/응답).
  - **왜 필요?** 내부/외부 서비스가 가장 보편적으로 통신할 수 있음.
  - **어디에?** `docs/msa_communication.md` REST 가이드.

- **gRPC**: 바이너리(Protocol Buffers) 기반의 고성능 RPC 통신.
  - **왜 필요?** 내부 서비스 간 고TPS/저지연 통신에 유리.
  - **어디에?** `contracts/nexus_inference.proto`, `docs/msa_communication.md`.

- **gRPC Channel(채널)**: gRPC 서버와 연결을 유지하는 통신 통로.
  - **왜 필요?** 클라이언트가 서버에 요청을 보내기 위해.
  - **어디에?** `gateway/scripts/grpc_agent_smoke.py`.

- **gRPC Stub(스텁)**: gRPC 서버의 메서드를 호출하기 위한 클라이언트 객체.
  - **왜 필요?** 메서드 호출을 함수처럼 사용하기 위해.
  - **어디에?** `gateway/scripts/grpc_agent_smoke.py`.

- **gRPC Upstream**: Gateway가 `grpc://` 스킴으로 내부 워커를 호출하는 방식.
  - **왜 필요?** 내부 통신을 저지연으로 처리하기 위해.
  - **어디에?** `gateway/app/services/proxy.py`, `docs/grpc_agent_guide.md`.

- **Protocol Adapter(프로토콜 어댑터)**: REST 요청을 gRPC 등 다른 프로토콜로 변환하는 역할.
  - **왜 필요?** 외부 호출과 내부 통신 방식을 분리해 유연성을 확보하기 위해.
  - **어디에?** `gateway/app/services/proxy.py`의 `_grpc_response`.

- **Codegen(코드 생성)**: proto 계약을 실제 코드로 자동 변환하는 작업.
  - **왜 필요?** 요청/응답 구조와 서비스 인터페이스를 일관되게 맞추기 위해.
  - **어디에?** `scripts/gen_grpc.sh`.

- **PB2 / PB2_GRPC**: proto에서 자동 생성되는 Python 파일 이름 규칙.
  - **왜 필요?** 메시지 구조(`*_pb2.py`)와 서비스 연결(`*_pb2_grpc.py`)을 구분하기 위해.
  - **어디에?** `docs/grpc_gen_guide.md`.

- **Generated Code(자동 생성 코드)**: 스크립트로 생성되는 파일(직접 수정하지 않음).
  - **왜 필요?** proto 변경 시 일관된 코드 생성과 호환성 유지.
  - **어디에?** `scripts/gen_grpc.sh`, `docs/grpc_gen_guide.md`.

- **RPC(Remote Procedure Call, 원격 프로시저 호출)**: 네트워크 너머의 함수를 로컬 호출처럼 실행하는 방식.
  - **왜 필요?** 서비스 간 호출을 단순한 함수 호출처럼 만들기 위해.
  - **어디에?** `contracts/nexus_inference.proto`의 `service`/`rpc` 정의.

- **Protobuf(Protocol Buffers)**: gRPC 메시지 스키마를 정의하는 직렬화 형식.
  - **왜 필요?** 서비스 간 계약을 엄격하게 맞추고 성능을 확보하기 위해.
  - **어디에?** `contracts/nexus_inference.proto`.

- **Field Number(필드 번호)**: Protobuf 필드에 붙는 고유 번호(예: `= 1`, `= 2`).
  - **왜 필요?** 호환성을 유지하기 위한 식별자(변경 금지).
  - **어디에?** `contracts/nexus_inference.proto`.

- **Idempotency(멱등성)**: 같은 요청을 여러 번 보내도 결과가 동일하게 유지되는 성질.
  - **왜 필요?** 재시도 시 중복 처리/중복 과금/중복 생성 방지.
  - **어디에?** `Idempotency-Key` 헤더, `docs/msa_communication.md`.

- **Timeout/Deadline(타임아웃/데드라인)**: 요청 처리에 허용되는 최대 시간.
  - **왜 필요?** 지연이 길어지는 요청을 빠르게 차단하고 장애 전파를 방지.
  - **어디에?** `docs/msa_communication.md` 타임아웃 가이드.

- **Saga(사가 패턴)**: 분산 트랜잭션을 단계별 보상 작업으로 관리하는 방식.
  - **왜 필요?** 여러 서비스가 얽힌 작업을 안정적으로 완료/복구하기 위해.
  - **어디에?** `docs/msa_communication.md` 트랜잭션 패턴.

- **Outbox 패턴**: DB 변경과 이벤트 발행을 분리하지 않고 함께 기록하는 방식.
  - **왜 필요?** 데이터 변경과 이벤트 전파의 일관성을 확보하기 위해.
  - **어디에?** `docs/msa_communication.md` 트랜잭션 패턴.

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

- **Kafka**: 로그/이벤트를 안전하게 모아두는 메시지 스트림.
  - **왜 필요?** 대량 로그를 한 번에 받고 다른 시스템으로 전달하기 위해.
  - **어디에?** `docker-compose.logging.yml`의 `kafka` 서비스.

- **Elasticsearch**: 로그를 저장·검색하는 데이터베이스.
  - **왜 필요?** 로그를 빠르게 검색하고 필터링하기 위해.
  - **어디에?** `docker-compose.logging.yml`의 `elasticsearch` 서비스.

- **Kibana**: Elasticsearch에 저장된 로그를 화면으로 보는 도구.
  - **왜 필요?** 로그를 시각적으로 탐색/분석하기 위해.
  - **어디에?** `docker-compose.logging.yml`의 `kibana` 서비스. (Elasticsearch 로그를 웹에서 검색/필터링)

- **Vector**: 로그 수집/전달 에이전트.
  - **왜 필요?** 로그를 Kafka로 보내거나 Elasticsearch로 적재하기 위해.
  - **어디에?** `ops/logging/vector-to-kafka.toml`, `ops/logging/kafka-to-es.toml`.

- **Zookeeper(주키퍼)**: Kafka 같은 분산 시스템의 상태/구성을 관리하는 코디네이터.
  - **왜 필요?** Kafka 클러스터가 안정적으로 동작하도록 보조하기 위해.
  - **어디에?** `docker-compose.logging.yml`의 `zookeeper` 서비스.

- **Confluent**: Kafka를 운영/배포하기 쉽게 만든 배포판(이미지 제공).
  - **왜 필요?** 로컬에서 Kafka를 빠르게 띄우기 위해.
  - **어디에?** `docker-compose.logging.yml`의 Kafka 이미지.

- **Topic(토픽)**: Kafka에서 메시지를 모아두는 “채널”.
  - **왜 필요?** 로그/이벤트를 종류별로 분리해 전달하기 위해.
  - **어디에?** `gateway-logs` 토픽.

- **Index(인덱스)**: Elasticsearch에 저장되는 로그 묶음(테이블 같은 개념).
  - **왜 필요?** 날짜/종류별로 로그를 빠르게 조회하기 위해.
  - **어디에?** `gateway-logs-YYYY.MM.DD` 형태로 생성.

- **Data View(데이터 뷰)**: Kibana에서 인덱스를 쉽게 탐색하기 위한 보기 설정.
  - **왜 필요?** Kibana에서 필드/시간 기준으로 로그를 조회하기 위해.
  - **어디에?** `gateway-logs-*` 데이터 뷰.

- **Saved Object(저장 객체)**: Kibana 설정(데이터 뷰, 대시보드 등)을 저장하는 내부 단위.
  - **왜 필요?** Kibana 설정을 API로 생성/관리하기 위해.
  - **어디에?** `ops/logging/bootstrap_kibana.sh`에서 조회 API 사용.

- **KQL(Kibana Query Language)**: Kibana에서 로그를 검색하기 위한 쿼리 문법.
  - **왜 필요?** 에러/지연/업스트림 등 원하는 로그를 빠르게 찾기 위해.
  - **어디에?** `ops/logging/kibana_queries.md`.

- **Correlation(상관 분석)**: 지표와 로그를 함께 보고 원인을 좁히는 방법.
  - **왜 필요?** 지표 이상 원인을 로그에서 빠르게 찾기 위해.
  - **어디에?** `ops/logging/correlation_guide.md`.

- **Dashboard(대시보드)**: 여러 지표/로그 패널을 한 화면에 모아 보는 화면.
  - **왜 필요?** 장애 상황을 빠르게 한눈에 파악하기 위해.
  - **어디에?** `ops/logging/kibana_dashboard.md`.

- **Saved Query(저장 쿼리)**: Kibana에서 재사용할 수 있는 검색 쿼리.
  - **왜 필요?** 자주 쓰는 로그 필터를 반복 입력하지 않기 위해.
  - **어디에?** `ops/logging/bootstrap_kibana_saved_objects.sh`.

- **Saved Search(저장 검색)**: Discover 화면에서 저장하는 검색/테이블 설정.
  - **왜 필요?** 자주 쓰는 검색 결과를 빠르게 재사용하기 위해.
  - **어디에?** `ops/logging/kibana_saved_objects.ndjson`.

- **NDJSON(Newline Delimited JSON)**: JSON 객체를 한 줄씩 이어붙인 형식.
  - **왜 필요?** 여러 Kibana Saved Objects를 한 번에 가져오기/내보내기 위해.
  - **어디에?** `ops/logging/kibana_saved_objects.ndjson`.

- **Observability Status(관측 상태)**: 현재 모니터링 스택 상태를 빠르게 확인하는 체크리스트.
  - **왜 필요?** 장애 시 어디가 문제인지 즉시 파악하기 위해.
  - **어디에?** `ops/observability_status.md`.

- **Log Schema(로그 스키마)**: 로그에 포함되는 필드와 의미를 정리한 문서.
  - **왜 필요?** Kibana에서 필드 기반 탐색을 쉽게 하기 위해.
  - **어디에?** `ops/logging/log_schema.md`.

- **Observability Summary(관측 요약)**: 관측 스택 구성과 링크를 한눈에 보는 문서.
  - **왜 필요?** 현재 구성/접근 경로를 빠르게 파악하기 위해.
  - **어디에?** `ops/observability_summary.md`.

- **Dashboard Link(대시보드 링크)**: Grafana 대시보드에서 외부 시스템으로 이동하는 링크.
  - **왜 필요?** 지표에서 바로 로그 화면으로 이동하기 위해.
  - **어디에?** `ops/grafana/provisioning/dashboards/nexus-gateway.json`.

- **Bootstrap Script(부트스트랩 스크립트)**: 초기 설정을 자동으로 구성하는 스크립트.
  - **왜 필요?** 데이터 뷰/저장 객체 등을 반복 없이 생성하기 위해.
  - **어디에?** `ops/observability_bootstrap.sh`.

- **mTLS(상호 TLS)**: 서비스 간에 서로를 인증하는 TLS 방식.
  - **왜 필요?** 내부 통신 신뢰성을 높이기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **PII(개인정보)**: 개인을 식별할 수 있는 정보.
  - **왜 필요?** 로그/데이터에서 민감정보를 마스킹하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **PII 마스킹(PII Masking)**: 로그에 민감 정보를 원문 대신 가공 형태로 저장하는 것.
  - **왜 필요?** 개인정보 유출 위험을 줄이기 위해.
  - **어디에?** `gateway/app/core/redaction.py`, `docs/security_baseline.md`.

- **Audit Log(감사 로그)**: 누가 어떤 요청을 했는지 기록하는 보안 로그.
  - **왜 필요?** 보안 감사/추적 가능성을 확보하기 위해.
  - **어디에?** `gateway/app/core/security.py`, `docs/security_baseline.md`.

- **Principal Hash(주체 해시)**: 호출 주체 식별자를 해시로 저장한 값.
  - **왜 필요?** 감사 로그에 원문 노출 없이 추적성을 확보하기 위해.
  - **어디에?** `gateway/app/core/redaction.py`.

- **Shadow Traffic(미러링 트래픽)**: 실제 요청을 복제해 별도 경로로 보내는 방식.
  - **왜 필요?** 운영에 영향 없이 새 기능을 검증하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **Shadow Policy(미러링 정책)**: 어떤 요청을 어느 비율로 복제할지 정하는 규칙.
  - **왜 필요?** 성능 검증 범위를 안전하게 조절하기 위해.
  - **어디에?** `docs/shadow_traffic.md`, `gateway/app/core/shadow.py`.

- **Shadow Target(미러링 대상)**: 복제된 요청을 보내는 별도 업스트림.
  - **왜 필요?** 신규 모델/버전을 운영 트래픽과 분리해 검증하기 위해.
  - **어디에?** `docs/shadow_traffic.md`.

- **Disaggregated Serving(분리 서빙)**: 프리필/디코딩 등 서빙 단계를 분리해 처리하는 방식.
  - **왜 필요?** GPU 자원을 효율적으로 쓰고 병목을 줄이기 위해.
  - **어디에?** `plan.md` 단계 B 강화 항목.

- **Prefix-aware Routing(프리픽스 기반 라우팅)**: 요청 프롬프트의 앞부분을 기준으로 라우팅하는 방식.
  - **왜 필요?** 캐시 히트율/성능을 높이기 위해.
  - **어디에?** `plan.md` 단계 B 강화 항목.

- **Context Caching(컨텍스트 캐싱)**: 긴 프롬프트의 일부를 캐시해 재사용하는 최적화.
  - **왜 필요?** 지연 시간과 비용을 줄이기 위해.
  - **어디에?** `plan.md` 단계 B 강화 항목.

- **Service Mesh(서비스 메시)**: 서비스 간 통신을 프록시 레이어로 관리하는 인프라.
  - **왜 필요?** mTLS, 정책, 관측을 코드 변경 없이 적용하기 위해.
  - **어디에?** `plan.md` 단계 A/B 강화 항목.

- **Istio**: 대표적인 Service Mesh 구현체.
  - **왜 필요?** mTLS, 트래픽 정책, 관측 기능을 제공.
  - **어디에?** `plan.md` 실 구현 체크리스트.

- **Linkerd**: 경량 Service Mesh 구현체.
  - **왜 필요?** 비교적 단순한 운영으로 mTLS/관측 적용.
  - **어디에?** `plan.md` 실 구현 체크리스트.

- **Argo Rollouts**: Canary/Blue-Green 배포를 지원하는 Argo 확장 컴포넌트.
  - **왜 필요?** 배포 전략을 자동화하고 롤백을 쉽게 하기 위해.
  - **어디에?** `plan.md` 단계 B 강화 항목.

- **PoC(Proof of Concept, 개념 검증)**: 실제 적용 전에 가능성을 확인하는 작은 실험.
  - **왜 필요?** 큰 투자 전에 리스크를 줄이기 위해.
  - **어디에?** `plan.md` 실 구현 체크리스트.

- **Chaos(혼돈 테스트)**: 일부 장애를 의도적으로 발생시켜 복원력을 검증하는 테스트.
  - **왜 필요?** 장애 대응 체계를 검증하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **Blue/Green 배포**: 두 환경을 번갈아 운영해 무중단 전환하는 배포 방식.
  - **왜 필요?** 롤백과 안전 배포를 쉽게 하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **FinOps(클라우드 비용 최적화)**: 클라우드 비용을 가시화/최적화하는 운영 방식.
  - **왜 필요?** GPU 비용을 효율적으로 관리하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **DR(재해 복구)**: 장애 시 서비스를 복구하기 위한 전략.
  - **왜 필요?** 대규모 장애에도 서비스 지속성을 확보하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **데이터 거버넌스**: 데이터 품질/버전/접근 제어를 관리하는 체계.
  - **왜 필요?** 데이터 신뢰성과 컴플라이언스를 확보하기 위해.
  - **어디에?** `plan.md` 강화 항목.

- **Throughput(TPS, 처리량)**: 초당 처리 가능한 요청 수.
  - **왜 필요?** 시스템이 얼마나 많은 요청을 감당하는지 판단하기 위해.
  - **어디에?** `ops/perf_tuning_report.md` 지표 항목.

- **LLM Serving(서빙)**: 모델을 API로 제공해 요청을 처리하는 시스템.
  - **왜 필요?** 실제 서비스에서 모델을 호출할 수 있게 하기 위해.
  - **어디에?** `docs/llm_serving_agent_guide.md`, `plan.md`.

- **OpenAI 호환 API**: `/v1/chat/completions` 형식의 공통 API 스펙.
  - **왜 필요?** 다양한 모델 엔진을 동일한 호출 방식으로 통합하기 위해.
  - **어디에?** `docs/llm_serving_agent_guide.md`, `gateway/README.md`.

- **Healthcheck(헬스체크)**: 서비스가 정상 동작하는지 확인하는 간단한 상태 점검.
  - **왜 필요?** 배포 후 빠르게 정상 여부를 확인하기 위해.
  - **어디에?** `docs/llm_serving_agent_guide.md`, `scripts/run_sglang.sh`.

- **Load Test(부하 테스트)**: 일정 트래픽을 지속적으로 주어 성능을 측정하는 테스트.
  - **왜 필요?** 안정적인 처리량/지연 시간을 확인하기 위해.
  - **어디에?** `ops/testing/load_test.md`.

- **Spike Test(급증 테스트)**: 짧은 시간에 트래픽을 급격히 올려 보는 테스트.
  - **왜 필요?** 갑작스러운 트래픽 폭증 대응 능력을 확인하기 위해.
  - **어디에?** `ops/testing/load_test.md`.

- **RPS(Requests Per Second)**: 초당 요청 수.
  - **왜 필요?** 부하 테스트 강도를 수치로 관리하기 위해.
  - **어디에?** `ops/testing/load_test.md`.

- **k6**: 부하 테스트를 수행하는 CLI 도구.
  - **왜 필요?** HTTP 부하 테스트를 손쉽게 실행하기 위해.
  - **어디에?** `ops/testing/k6_smoke.js`.

- **Latency Percentile(p50/p95/p99)**: 지연시간 분포의 분위수.
  - **왜 필요?** 평균이 아닌 “느린 요청” 구간을 파악하기 위해.
  - **어디에?** `ops/perf_tuning_report.md` 지표 항목.

- **Batch Size(배치 크기)**: 한 번에 처리하는 요청 묶음 크기.
  - **왜 필요?** 처리량과 지연시간의 균형을 조절하기 위해.
  - **어디에?** `ops/perf_tuning_report.md` 파라미터 항목.

- **Concurrency(동시성)**: 동시에 처리하는 요청 수.
  - **왜 필요?** 부하 상황에서 성능을 재현하기 위해.
  - **어디에?** `ops/perf_tuning_report.md` 워크로드 항목.

- **GPU Utilization(자원 사용률)**: GPU가 사용되는 비율.
  - **왜 필요?** 성능 최적화와 병목 원인을 확인하기 위해.
  - **어디에?** `ops/perf_tuning_report.md` 지표 항목.

- **Source/Sink(소스/싱크)**: Vector 파이프라인의 입력/출력 지점.
  - **왜 필요?** 어디서 로그를 읽고 어디로 보낼지 분리해 설정하기 위해.
  - **어디에?** `vector-to-kafka.toml`, `kafka-to-es.toml`에서 정의.

- **VRL(Vector Remap Language)**: Vector에서 로그를 변환하는 스크립트 언어.
  - **왜 필요?** 로그 형식을 정규화하거나 필드를 추가/변형하기 위해.
  - **어디에?** `vector-to-kafka.toml`의 `remap` 블록.

- **Log Pipeline(로그 파이프라인)**: 로그가 이동하는 전체 흐름.
  - **왜 필요?** 수집 → 전달 → 저장 → 조회 흐름을 표준화하기 위해.
  - **어디에?** `ops/logging/README.md` 문서.

- **SLI(Service Level Indicator)**: 서비스 품질을 수치로 측정하는 지표.
  - **왜 필요?** 신뢰성/성능을 숫자로 판단하기 위해.
  - **어디에?** Prometheus 메트릭으로 계산.

- **SLO(Service Level Objective)**: SLI에 대한 목표값.
  - **왜 필요?** 운영 기준선을 명확히 하기 위해.
  - **어디에?** `ops/slo_runbook.md`에 정의.

- **SLA(Service Level Agreement)**: 외부 고객과 합의한 보장 수준.
  - **왜 필요?** 사업/계약 기준으로 품질을 약속하기 위해.
  - **어디에?** 실제 계약/정책 문서(현재는 내부 기준만).

- **Error Budget(에러 예산)**: SLO에서 허용하는 실패 범위.
  - **왜 필요?** 장애 허용치 안에서 실험/변경을 관리하기 위해.
  - **어디에?** SLO 계산 결과로 산출.

- **Runbook(런북)**: 장애 대응 절차를 정리한 문서.
  - **왜 필요?** 누구나 동일한 절차로 빠르게 복구하기 위해.
  - **어디에?** `ops/slo_runbook.md`.

- **Quickstart(빠른 시작)**: 핵심 절차만 요약한 짧은 가이드.
  - **왜 필요?** 긴 문서를 읽지 않고도 빠르게 테스트하기 위해.
  - **어디에?** `ops/runbook_quickstart.md`.

- **Flag/Option(옵션)**: 명령어의 동작을 바꾸는 스위치.
  - **왜 필요?** 명령어를 상황에 맞게 조정하기 위해.
  - **어디에?** `docs/cli_commands_guide.md`.

- **Pipe(파이프)**: 한 명령의 출력을 다음 명령의 입력으로 전달하는 기능.
  - **왜 필요?** 결과를 필터링/가공해서 바로 다음 명령으로 넘기기 위해.
  - **어디에?** `docs/cli_commands_guide.md`.

- **Redirection(리다이렉션)**: 출력 결과를 파일로 저장하는 기능.
  - **왜 필요?** 결과를 파일로 남기거나 로그를 보존하기 위해.
  - **어디에?** `docs/cli_commands_guide.md`.

- **Alert Rule(알림 규칙)**: 지표가 기준을 넘으면 알림을 발생시키는 조건.
  - **왜 필요?** 장애 징후를 빠르게 감지하기 위해.
  - **어디에?** `ops/prometheus_alerts.yml`.

- **PromQL**: Prometheus 지표를 조회/계산하는 쿼리 언어.
  - **왜 필요?** 에러율/지연시간 같은 지표를 계산하기 위해.
  - **어디에?** `ops/prometheus_alerts.yml`의 alert 조건.

- **Alertmanager**: Prometheus 알림을 받아 전달/라우팅하는 서비스.
  - **왜 필요?** 알림을 Slack/Email/Webhook 등으로 보낼 수 있게 하기 위해.
  - **어디에?** `ops/alertmanager.yml`, `docker-compose.yml`.

- **Receiver(수신자)**: Alertmanager가 알림을 전달하는 대상.
  - **왜 필요?** 알림을 어디로 보낼지 설정하기 위해.
  - **어디에?** `ops/alertmanager.yml`.

- **Webhook(웹훅)**: HTTP로 알림을 전달하는 방식.
  - **왜 필요?** 외부 시스템으로 알림을 전달하기 위해.
  - **어디에?** `ops/alertmanager.yml`의 예시 설정.

- **Test Alert(테스트 알림)**: 실제 장애 없이 알림 경로를 검증하는 테스트 이벤트.
  - **왜 필요?** 알림이 정상적으로 도착하는지 확인하기 위해.
  - **어디에?** `ops/alerts/test_alert.sh`.

- **Slack Webhook(슬랙 웹훅)**: Slack으로 알림을 보내는 URL 기반 방식.
  - **왜 필요?** 팀 채널로 즉시 알림을 전달하기 위해.
  - **어디에?** `ops/alerts/receiver_templates.md`.

- **SMTP**: 이메일 발송 서버 프로토콜.
  - **왜 필요?** 이메일로 알림을 전송하기 위해.
  - **어디에?** `ops/alerts/receiver_templates.md`.

- **Contact Point(연락처)**: Grafana 알림이 전달될 대상 설정.
  - **왜 필요?** 알림을 외부 시스템으로 보내기 위해.
  - **어디에?** `ops/grafana/provisioning/alerting/contact-points.yml`.

- **Notification Policy(알림 정책)**: 알림을 어떤 규칙으로 묶어 전달할지 결정.
  - **왜 필요?** 알림 빈도/그룹화를 조절하기 위해.
  - **어디에?** `ops/grafana/provisioning/alerting/notification-policies.yml`.

- **Port Forward(포트 포워딩)**: 클러스터 내부 서비스를 로컬에서 여는 방법.
  - **왜 필요?** 로컬에서 UI나 API에 접속하기 위해.
  - **어디에?** `kubectl port-forward` 명령으로 사용.

- **KFP(Kubeflow Pipelines)**: Kubeflow 내 파이프라인 실행 엔진.
  - **왜 필요?** 모델 학습/검증/배포 단계를 자동화하기 위해.
  - **어디에?** Kubeflow 설치 시 동작하는 핵심 컴포넌트.

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

- **CI(Continuous Integration)**: 코드를 자주 병합하고 자동 테스트/빌드를 수행하는 과정.
  - **왜 필요?** 버그를 빠르게 발견하고 안정적으로 통합하기 위해.
  - **어디에?** 향후 CI 파이프라인에서 사용 (예: GitHub Actions).

- **CD(Continuous Delivery/Deployment)**: 빌드된 결과를 자동으로 배포까지 연결하는 과정.
  - **왜 필요?** 배포 속도를 높이고 수동 오류를 줄이기 위해.
  - **어디에?** Argo CD 같은 배포 도구/파이프라인에서 수행.

- **Model Registry(모델 레지스트리)**: 모델 버전과 상태(예: Production)를 관리하는 저장소.
  - **왜 필요?** 배포 대상을 명확히 하고 추적하기 위해.
  - **어디에?** `mlops/mlflow/README.md`.

- **Model URI**: 배포에 사용할 모델 버전을 가리키는 식별자.
  - **왜 필요?** “어떤 모델을 배포할지”를 명확히 지정하기 위해.
  - **어디에?** `mlops/mlflow/README.md`.

- **Argo Workflows**: 쿠버네티스 기반 배치 워크플로우 엔진.
  - **왜 필요?** 데이터 전처리/평가 같은 배치 작업을 단계별로 실행하기 위해.
  - **어디에?** `mlops/argo-workflows/`.

- **Airflow**: 정기 배치 작업을 스케줄링하는 워크플로우 도구.
  - **왜 필요?** 재학습/정기 리포트 같은 반복 작업을 관리하기 위해.
  - **어디에?** `mlops/airflow/`.

- **Scaffolding(스캐폴딩)**: 실제 구현 전에 구조/틀을 먼저 만들어 두는 작업.
  - **왜 필요?** 팀/프로젝트가 같은 구조를 공유하고, 이후 구현 리스크를 줄이기 위해.
  - **어디에?** `mlops/`, `k8s/overlays/`, `serving/` 내 템플릿.

- **PVC(PersistentVolumeClaim)**: Pod가 사용할 영속 스토리지를 요청하는 리소스.
  - **왜 필요?** 단계 간 결과 파일을 공유하고 재사용하기 위해.
  - **어디에?** `mlops/kubeflow/pipeline.yaml`.

- **Artifact(아티팩트)**: 파이프라인 단계에서 만들어지는 결과 파일.
  - **왜 필요?** 다음 단계가 이전 결과를 참고하기 위해.
  - **어디에?** `mlops/README.md`의 결과물 목록.

- **RBAC(Role-Based Access Control)**: 역할(Role) 기반으로 권한을 제어하는 방식.
  - **왜 필요?** 누구/어떤 서비스가 어떤 리소스를 조작할 수 있는지 제한하기 위해.
  - **어디에?** `mlops/argo-workflows/rbac.yaml`.

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

# 작업 기록: MLflow 모델 URI → 배포 연결 예시 추가

## 작업 목적
- MLflow 레지스트리의 모델 URI를 KServe 배포 설정에 연결하는 예시를 추가했습니다.

## 변경 파일
- `k8s/kserve/inferenceservice.yaml`
- `k8s/kserve/README.md`

## 요약
- `MODEL_URI=models:/<name>/<stage>` 형태를 문서화

---

# 작업 기록: KServe 설치/적용 흐름 문서화

## 작업 목적
- KServe 적용에 필요한 전제(설치)와 적용 순서를 문서화했습니다.

## 변경 파일
- `k8s/kserve/README.md`
- `mlops/README.md`

## 요약
- KServe CRD 확인 및 InferenceService 적용 흐름 추가

---

# 작업 기록: KServe 배포 체크리스트 추가

## 작업 목적
- 배포 전/후 확인할 체크리스트를 추가했습니다.

## 변경 파일
- `k8s/kserve/checklist.md`
- `k8s/kserve/README.md`

## 요약
- 설치/적용/검증 단계 체크리스트 제공

---

# 작업 기록: 검증 실패 시 파이프라인 중단 처리

## 작업 목적
- 데이터 검증 실패 시 파이프라인이 중단되도록 로직을 강화했습니다.

## 변경 파일
- `mlops/kubeflow/scripts/data_validation.py`
- `mlops/kubeflow/scripts-configmap.yaml`
- `mlops/README.md`

## 요약
- 데이터 파일이 없으면 `RuntimeError`로 실패 처리

---

# 작업 기록: 파이프라인 요약 리포트 추가

## 작업 목적
- 각 단계 결과를 하나의 요약 파일로 묶어 확인하기 쉽게 했습니다.

## 변경 파일
- `mlops/kubeflow/scripts/summary_report.py`
- `mlops/kubeflow/scripts-configmap.yaml`
- `mlops/kubeflow/pipeline.yaml`
- `mlops/README.md`

## 요약
- `summary.json`으로 결과 요약을 생성

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

# 작업 기록: Kubeflow 파이프라인 단계 스크립트 연결

## 작업 목적
- 파이프라인 단계별로 실제 실행되는 스크립트를 연결했습니다.

## 변경 파일
- `mlops/kubeflow/pipeline.yaml`
- `mlops/kubeflow/scripts-configmap.yaml`
- `mlops/kubeflow/scripts/`
- `mlops/README.md`

## 요약
- ConfigMap으로 스크립트를 마운트하고 각 단계에서 실행
- `workspace` PVC를 통해 단계 간 결과 파일 공유

---

# 작업 기록: 파이프라인 단계 로직 구체화

## 작업 목적
- 파이프라인 단계가 실제 결과물을 생성하도록 로직을 보강했습니다.

## 변경 파일
- `mlops/kubeflow/scripts/`
- `mlops/kubeflow/scripts-configmap.yaml`
- `mlops/kubeflow/pipeline.yaml`
- `mlops/README.md`

## 요약
- 각 단계가 JSON/텍스트 아티팩트를 생성하도록 구성
- 배포 단계에서 KServe 템플릿을 파일로 생성

---

# 작업 기록: GitOps 연계 설명 추가

## 작업 목적
- 파이프라인 결과가 Argo CD 배포로 이어지는 흐름을 문서화했습니다.

## 변경 파일
- `mlops/gitops/README.md`
- `mlops/README.md`

## 요약
- 파이프라인 출력물을 Git에 커밋하면 Argo CD가 동기화하는 흐름 정리

---

# 작업 기록: GitOps 커밋 예시 추가

## 작업 목적
- 파이프라인 결과를 Git에 반영하는 수동 커밋 예시를 추가했습니다.

## 변경 파일
- `mlops/gitops/commit_example.md`
- `mlops/gitops/README.md`
- `mlops/README.md`

## 요약
- GitOps 커밋 예시 명령 추가

---

# 작업 기록: Kubeflow GitOps 커밋 단계(옵션) 추가

## 작업 목적
- 파이프라인 결과물을 GitOps 경로로 복사하는 단계를 추가했습니다.

## 변경 파일
- `mlops/kubeflow/pipeline.yaml`
- `mlops/kubeflow/scripts-configmap.yaml`
- `mlops/gitops/gitops_commit_step.py`
- `mlops/README.md`

## 요약
- `kserve_manifest.yaml`을 GitOps 대상 경로로 복사하는 예시 단계 추가

---

# 작업 기록: BentoML 워커 예시 추가

## 작업 목적
- BentoML 기반 워커의 최소 동작 예시를 추가했습니다.

## 변경 파일
- `serving/bentoml/service.py`
- `serving/bentoml/README.md`

## 요약
- 간단한 JSON 입력/출력 형태로 응답하는 mock 서비스 제공

---

# 작업 기록: BentoML 빌드 파일 추가

## 작업 목적
- BentoML 서비스 패키징을 위한 기본 파일을 추가했습니다.

## 변경 파일
- `serving/bentoml/requirements.txt`
- `serving/bentoml/bentofile.yaml`
- `serving/bentoml/README.md`

## 요약
- 최소 의존성과 빌드 설정 스캐폴딩 마련

---

# 작업 기록: BentoML K8s 워커 오버레이 추가

## 작업 목적
- BentoML 워커를 선택적으로 배포할 수 있도록 K8s 오버레이를 추가했습니다.

## 변경 파일
- `k8s/overlays/bentoml/`
- `k8s/README.md`
- `serving/bentoml/README.md`

## 요약
- CPU 환경에서 BentoML 워커를 띄우는 선택형 오버레이 제공

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

# 작업 기록: Argo CD 로컬 설치 및 Application 생성

## 작업 목적
- kind 환경에서 Argo CD를 설치하고 Application을 생성했습니다.

## 결과
- `argocd` 네임스페이스에 Argo CD 구성 요소가 올라옴
- `nexus-gateway` Application 생성 확인

---

# 작업 기록: MLflow 레지스트리 연동 문서 추가

## 작업 목적
- 모델 버전과 배포를 연결하는 기준(모델 URI)을 정리했습니다.

## 변경 파일
- `mlops/mlflow/README.md`
- `mlops/README.md`

## 요약
- `models:/name/version` 형태의 모델 URI를 배포 기준으로 사용

---

# 작업 기록: Argo Workflows/Airflow 스캐폴딩 추가

## 작업 목적
- 배치 워크플로우(Argo)와 스케줄링(Airflow) 구조를 문서화했습니다.

## 변경 파일
- `mlops/argo-workflows/workflow.yaml`
- `mlops/argo-workflows/README.md`
- `mlops/airflow/README.md`
- `mlops/README.md`

## 요약
- Argo Workflows 기본 템플릿 추가
- Airflow는 구조만 먼저 마련

---

# 작업 기록: Argo Workflows RBAC 추가

## 작업 목적
- Nexus 네임스페이스에서 Workflow 실행 권한을 부여했습니다.

## 변경 파일
- `mlops/argo-workflows/rbac.yaml`
- `mlops/argo-workflows/workflow.yaml`
- `mlops/argo-workflows/README.md`

## 요약
- `argo-workflow` ServiceAccount와 RoleBinding 추가

---

# 작업 기록: Argo Workflows 로컬 실행 검증

## 작업 목적
- kind 클러스터에서 Argo Workflows를 설치하고 샘플 워크플로우를 실행했습니다.

## 결과
- `nexus-batch` 워크플로우가 정상 완료됨

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

---

# 작업 기록: Kubeflow 로컬 검증 후 종료

## 작업 목적
- KFP 스모크 테스트 완료 후 로컬 리소스를 정리해 시스템 부담을 줄였습니다.

## 변경 파일
- 없음 (클러스터 리소스만 정리)

## 요약
- `kubectl port-forward` 중지
- KFP 매니페스트 삭제로 `kubeflow` 네임스페이스 제거

---

# 작업 기록: 로그 파이프라인 스캐폴딩 추가 (Kafka → Elasticsearch → Kibana)

## 작업 목적
- 게이트웨이 구조화 로그를 Kafka로 수집하고 Elasticsearch/Kibana로 조회하는 흐름을 준비했습니다.

## 변경 파일
- `docker-compose.logging.yml`
- `ops/logging/README.md`
- `ops/logging/vector-to-kafka.toml`
- `ops/logging/kafka-to-es.toml`

## 요약
- Vector가 Docker 로그를 읽어 Kafka `gateway-logs` 토픽으로 전달
- 다른 Vector 인스턴스가 Kafka 로그를 Elasticsearch로 적재
- Kibana에서 `gateway-logs-*` 인덱스로 조회 가능

---

# 작업 기록: 로그 파이프라인 로컬 실행 검증 및 설정 보완

## 작업 목적
- Kafka → Elasticsearch → Kibana 경로가 실제로 동작하는지 로컬에서 검증했습니다.

## 변경 파일
- `docker-compose.logging.yml`
- `ops/logging/vector-to-kafka.toml`
- `ops/logging/kafka-to-es.toml`

## 요약
- Kafka 이미지를 Confluent 기반으로 교체하고 Zookeeper를 추가
- Vector 설정 오류 수정(필터/VRL/Elasticsearch sink)
- 게이트웨이 로그가 Kafka 토픽에 적재되고 Elasticsearch 인덱스가 생성되는 것 확인
- Kibana 데이터 뷰(`gateway-logs-*`) 생성 완료

---

# 작업 기록: SLO/Runbook 문서 초안 추가

## 작업 목적
- 게이트웨이 및 로그 파이프라인 운영 기준(SLO)과 장애 대응 절차(Runbook)를 문서화했습니다.

## 변경 파일
- `ops/slo_runbook.md`

## 요약
- 초기 SLO/SLI 기준과 알람 예시 정리
- 장애 유형별 확인 절차/복구 방법 정리

---

# 작업 기록: Runbook 용어 설명 보강

## 작업 목적
- Runbook 내 용어(Symptoms/Checks/Mitigation)를 한글로 이해하기 쉽게 설명했습니다.

## 변경 파일
- `ops/slo_runbook.md`

## 요약
- Runbook 항목 설명(증상/확인/완화)을 추가

---

# 작업 기록: Prometheus 알림 규칙 추가

## 작업 목적
- SLO 초안을 기반으로 Prometheus 알림 규칙을 추가했습니다.

## 변경 파일
- `ops/prometheus_alerts.yml`
- `ops/prometheus.yml`
- `docker-compose.yml`

## 요약
- Gateway 다운, 에러율/지연시간/레이트리밋/업스트림 오류 알림 추가
- Prometheus가 알림 규칙 파일을 읽도록 설정

---

# 작업 기록: PromQL 알림 식 설명 주석 추가

## 작업 목적
- Prometheus 알림 규칙의 expr를 한글 주석으로 이해하기 쉽게 보강했습니다.

## 변경 파일
- `ops/prometheus_alerts.yml`

## 요약
- 각 알림의 expr 바로 아래에 의미 설명 주석 추가

---

# 작업 기록: Kibana 데이터 뷰 자동 생성 스크립트 추가

## 작업 목적
- Kibana 데이터 뷰를 수동 설정 없이 생성할 수 있도록 스크립트를 추가했습니다.

## 변경 파일
- `ops/logging/bootstrap_kibana.sh`
- `ops/logging/README.md`

## 요약
- Kibana Saved Objects API로 데이터 뷰 존재 여부 확인
- 없으면 `gateway-logs-*` 데이터 뷰 생성

---

# 작업 기록: Kibana 설명 보강

## 작업 목적
- Kibana가 무엇인지와 어디에 쓰는지 설명을 보강했습니다.

## 변경 파일
- `ops/slo_runbook.md`
- `worklog.md`

## 요약
- Kibana 설명에 “Elasticsearch 로그를 웹에서 검색/필터링” 의미 추가

---

# 작업 기록: Kibana KQL 쿼리 템플릿 추가

## 작업 목적
- Kibana에서 바로 사용할 수 있는 검색 템플릿(KQL)을 정리했습니다.

## 변경 파일
- `ops/logging/kibana_queries.md`
- `ops/logging/README.md`

## 요약
- 에러/지연/업스트림/요청 추적용 기본 쿼리 예시 제공

---

# 작업 기록: 메트릭-로그 상관 분석 가이드 추가

## 작업 목적
- Prometheus 지표와 Kibana 로그를 함께 보는 방법을 정리했습니다.

## 변경 파일
- `ops/logging/correlation_guide.md`
- `ops/logging/README.md`

## 요약
- 에러율/지연/업스트림 오류/레이트리밋/회로차단 상황별 점검 흐름 정리

---

# 작업 기록: 성능 튜닝 리포트 템플릿 추가

## 작업 목적
- vLLM 성능 튜닝 결과를 기록할 수 있는 템플릿을 추가했습니다.

## 변경 파일
- `ops/perf_tuning_report.md`

## 요약
- 워크로드/지표/파라미터/결과 요약 형식 제공

---

# 작업 기록: Alertmanager 스캐폴딩 추가

## 작업 목적
- Prometheus 알림을 수신/라우팅할 Alertmanager를 로컬에 연결했습니다.

## 변경 파일
- `ops/alertmanager.yml`
- `ops/alerts/README.md`
- `ops/prometheus.yml`
- `docker-compose.yml`

## 요약
- Alertmanager 기본 설정 파일 추가
- Prometheus가 Alertmanager로 알림을 전달하도록 연결

---

# 작업 기록: Alertmanager 로컬 구동

## 작업 목적
- 로컬에서 Alertmanager를 실행하고 Prometheus 재시작으로 연동을 반영했습니다.

## 변경 파일
- 없음 (컨테이너 실행만 수행)

## 요약
- `alertmanager` 컨테이너 시작
- Prometheus 재시작으로 alerting 설정 반영

---

# 작업 기록: Grafana 알림 설정 스캐폴딩

## 작업 목적
- Grafana에서 알림을 외부로 전송할 수 있도록 기본 설정을 추가했습니다.

## 변경 파일
- `ops/grafana/provisioning/alerting/contact-points.yml`
- `ops/grafana/provisioning/alerting/notification-policies.yml`
- `ops/grafana/provisioning/alerting/alert-rules.yml`
- `ops/grafana/provisioning/alerting/README.md`

## 요약
- Alertmanager로 전송하는 기본 Webhook Contact Point 추가
- 기본 Notification Policy 추가

---

# 작업 기록: Alertmanager 수신자 템플릿 추가

## 작업 목적
- Slack/Email/Webhook 수신자 템플릿을 정리했습니다.

## 변경 파일
- `ops/alerts/receiver_templates.md`
- `ops/alerts/README.md`

## 요약
- Slack Webhook, SMTP 예시 추가

---

# 작업 기록: Alertmanager 테스트 알림 스크립트 추가

## 작업 목적
- 로컬에서 알림 경로를 검증할 수 있도록 테스트 스크립트를 추가했습니다.

## 변경 파일
- `ops/alerts/test_alert.sh`
- `ops/alerts/README.md`

## 요약
- Alertmanager로 테스트 알림 전송 스크립트 추가

---

# 작업 기록: 알림 테스트 절차 문서 보강

## 작업 목적
- 관측 체크리스트와 Runbook Quickstart에 알림 테스트 절차를 추가했습니다.

## 변경 파일
- `ops/observability_status.md`
- `ops/runbook_quickstart.md`

## 요약
- Alertmanager 테스트 알림 실행 단계 추가

---

# 작업 기록: Kibana 대시보드 템플릿 추가

## 작업 목적
- Kibana에서 사용할 기본 대시보드 구성을 문서로 정리했습니다.

## 변경 파일
- `ops/logging/kibana_dashboard.md`
- `ops/logging/README.md`

## 요약
- 에러율/지연시간/업스트림/최근 에러 로그 등 핵심 패널 구성 정리

---

# 작업 기록: Kibana Saved Objects 자동 생성 스크립트 추가

## 작업 목적
- Kibana의 Saved Query/Dashboard를 스크립트로 생성할 수 있도록 추가했습니다.

## 변경 파일
- `ops/logging/bootstrap_kibana_saved_objects.sh`
- `ops/logging/kibana_saved_objects.md`
- `ops/logging/README.md`

## 요약
- 자주 쓰는 KQL 쿼리 저장 자동화
- Saved Search + 기본 대시보드 템플릿 자동 생성

---

# 작업 기록: Kibana Saved Objects 프로비저닝 검증

## 작업 목적
- 저장 객체 생성 스크립트를 실행해 실제 생성 여부를 확인했습니다.

## 변경 파일
- `ops/logging/bootstrap_kibana_saved_objects.sh`
- `worklog.md`

## 요약
- 데이터 뷰 조회 로직 개선(DATA_VIEW_ID 옵션 유지)
- Saved Query + Dashboard 생성 확인

---

# 작업 기록: Kibana 대시보드 패널 확장

## 작업 목적
- 로그 대시보드에 기본 패널을 4개로 확장했습니다.

## 변경 파일
- `ops/logging/kibana_saved_objects.ndjson`
- `ops/logging/kibana_saved_objects.md`

## 요약
- Errors/Slow/RateLimit/Chat 패널 구성 추가

---

# 작업 기록: NDJSON 용어 설명 추가

## 작업 목적
- Kibana Saved Objects 포맷(NDJSON)을 쉽게 이해할 수 있도록 용어 설명을 추가했습니다.

## 변경 파일
- `worklog.md`

## 요약
- NDJSON 정의 및 사용 이유 추가

---

# 작업 기록: Gateway 로그 스키마 문서 추가

## 작업 목적
- Gateway 로그 필드 정의를 문서로 정리했습니다.

## 변경 파일
- `ops/logging/log_schema.md`
- `ops/logging/README.md`

## 요약
- 로그 필드/설명/예시 표 추가

---

# 작업 기록: 관측 스택 요약 문서 추가

## 작업 목적
- 로컬 관측 스택 구성과 접근 URL을 한눈에 볼 수 있도록 요약했습니다.

## 변경 파일
- `ops/observability_summary.md`

## 요약
- Metrics/Logs/Alerts 구성과 접근 링크 정리

---

# 작업 기록: 관측 스택 부트스트랩 스크립트 추가

## 작업 목적
- Kibana 데이터 뷰와 저장 객체 생성을 한 번에 실행하도록 스크립트를 추가했습니다.

## 변경 파일
- `ops/observability_bootstrap.sh`
- `ops/observability_summary.md`

## 요약
- `bootstrap_kibana.sh` + `bootstrap_kibana_saved_objects.sh` 연계 실행

---

# 작업 기록: Grafana → Kibana 링크 추가

## 작업 목적
- Grafana 대시보드에서 Kibana Dashboard/Discover로 바로 이동할 수 있도록 링크를 추가했습니다.

## 변경 파일
- `ops/grafana/provisioning/dashboards/nexus-gateway.json`
- `ops/observability_summary.md`

## 요약
- Kibana 대시보드 및 Discover 링크 추가

---

# 작업 기록: 강화 항목 단계화 정리

## 작업 목적
- plan의 “추가로 강화하면 좋은 항목”을 단계별로 정리했습니다.

## 변경 파일
- `plan.md`

## 요약
- 단기/중기/장기 단계로 강화 항목 분리
- 보안/비용/DR/거버넌스 등 추가 항목 보강

---

# 작업 기록: 관측 스택 상태 체크리스트 추가

## 작업 목적
- 로컬에서 Prometheus/Grafana/Kibana/Alertmanager 상태를 빠르게 확인할 수 있도록 체크리스트를 추가했습니다.

## 변경 파일
- `ops/observability_status.md`

## 요약
- 서비스 상태, 접근 URL, 로그 플로우 테스트 절차 정리

---

# 작업 기록: Runbook Quickstart 추가

## 작업 목적
- 로컬에서 빠르게 장애 상황을 재현/확인할 수 있는 최소 절차를 정리했습니다.

## 변경 파일
- `ops/runbook_quickstart.md`
- `ops/slo_runbook.md`

## 요약
- Gateway down, 로그 플로우 테스트 등 최소 재현 시나리오 정리

---

# 작업 기록: 터미널 명령어/옵션 가이드 추가

## 작업 목적
- curl/docker/kubectl 등 명령어의 옵션과 기호를 쉽게 이해할 수 있도록 정리했습니다.

## 변경 파일
- `docs/cli_commands_guide.md`

## 요약
- 자주 쓰는 옵션(단축어)과 파이프/리다이렉션 등 셸 문법 설명 추가

---

# 작업 기록: MSA 통신 가이드 및 gRPC 계약 초안 추가

## 작업 목적
- 단계 A의 "MSA 통신" 항목을 문서화하고, 서비스 간 계약을 표준화하기 위한 gRPC proto 초안을 추가했습니다.

## 변경 파일
- `docs/msa_communication.md`
- `contracts/nexus_inference.proto`

## 요약
- REST/gRPC 통신 원칙, 헤더, 에러 포맷, 타임아웃/재시도 기준 정리
- gRPC 기본 서비스/메시지 스키마 초안 추가

---

# 작업 기록: proto 이해 가이드 추가

## 작업 목적
- gRPC proto 파일을 읽는 방법을 문서에 추가해 비개발자도 구조를 이해할 수 있도록 했습니다.

## 변경 파일
- `docs/msa_communication.md`
- `worklog.md`

## 요약
- proto 핵심 구성요소(service/rpc/message/field number) 설명 추가
- RPC/필드 번호 용어 설명 추가

---

# 작업 기록: MSA 통신 가이드 한글화

## 작업 목적
- MSA 통신 가이드를 한글로 정리해 이해도를 높였습니다.

## 변경 파일
- `docs/msa_communication.md`

## 요약
- REST/gRPC 통신 원칙과 proto 읽는 법을 한국어로 정리

---

# 작업 기록: 보안 강화(PII 마스킹 + 감사 로그 + mTLS 가이드)

## 작업 목적
- 단계 A의 "보안 강화" 항목을 문서화하고, 게이트웨이에 PII 마스킹과 감사 로그 스키마를 추가했습니다.

## 변경 파일
- `docs/security_baseline.md`
- `gateway/app/core/config.py`
- `gateway/app/core/redaction.py`
- `gateway/app/core/security.py`
- `gateway/app/core/logging.py`
- `gateway/app/main.py`
- `gateway/README.md`
- `ops/logging/log_schema.md`
- `worklog.md`

## 요약
- mTLS/S2S 인증/PII 마스킹/감사 로그 기준 정리
- 클라이언트 IP 마스킹 및 감사 로그 이벤트 추가
- 설정값(GATEWAY_PII_MASKING_ENABLED, GATEWAY_PII_HASH_SALT, GATEWAY_AUDIT_LOGGING_ENABLED) 추가

---

# 작업 기록: Shadow Traffic 가이드 및 스캐폴딩 추가

## 작업 목적
- 단계 A의 "Shadow Traffic" 항목을 문서화하고, 최소 스캐폴딩을 추가했습니다.

## 변경 파일
- `docs/shadow_traffic.md`
- `gateway/app/core/shadow.py`

## 요약
- 미러링 트래픽 동작 방식, 안전장치, 관측 포인트 정리
- Shadow 정책 구조 스캐폴딩 추가

---

# 작업 기록: 부하/Chaos 테스트 최소 세트 추가

## 작업 목적
- 단계 A의 "부하/장애 테스트" 항목을 문서화하고, 최소 실행 예시를 추가했습니다.

## 변경 파일
- `ops/testing/load_test.md`
- `ops/testing/chaos_test.md`
- `ops/testing/k6_smoke.js`
- `worklog.md`

## 요약
- Smoke/Baseline/Spike 시나리오와 관측 지표 정리
- 최소 장애 주입 시나리오 정의
- k6 기본 스모크 테스트 스크립트 추가

---

# 작업 기록: 계획 항목 실 구현 체크리스트 추가

## 작업 목적
- plan에 있는 계획 항목을 실제 구현 작업으로 전환할 수 있도록 체크리스트를 보강했습니다.

## 변경 파일
- `plan.md`
- `worklog.md`

## 요약
- 단계 A/B/C에 대한 실 구현 작업 목록 추가
- mTLS, shadow traffic, 고급 라우팅 등 후속 구현 기준 정리

---

# 작업 기록: Agent 통합 사용 시나리오 체크리스트 추가

## 작업 목적
- 외부 Agent 클라이언트, 내부 gRPC Agent, LLM 서빙 연동까지 포함하는 통합 사용 시나리오를 plan에 추가했습니다.

## 변경 파일
- `plan.md`

## 요약
- Agent 사용 수준을 1/2/3 범주로 분리해 실 구현 항목을 명시

---

# 작업 기록: 외부 Agent 클라이언트 가이드/스크립트 추가

## 작업 목적
- 통합 사용 시나리오(1)인 외부 Agent REST 호출을 쉽게 시작할 수 있도록 가이드와 스모크 스크립트를 추가했습니다.

## 변경 파일
- `docs/agent_client_guide.md`
- `gateway/scripts/agent_client_smoke.sh`
- `gateway/README.md`
- `docs/cli_commands_guide.md`
- `worklog.md`

## 요약
- REST 호출 가이드/예시 추가
- 스모크 테스트 스크립트 제공

---

# 작업 기록: 내부 gRPC Agent 연결 스캐폴딩/실행 경로 추가

## 작업 목적
- 통합 사용 시나리오(2)인 내부 gRPC 통신을 실제로 실행 가능한 수준으로 구성했습니다.

## 변경 파일
- `scripts/gen_grpc.sh`
- `gateway/scripts/grpc_agent_smoke.py`
- `serving/mock-worker/grpc_server.py`
- `docs/grpc_agent_guide.md`
- `gateway/pyproject.toml`
- `serving/mock-worker/requirements.txt`
- `gateway/README.md`
- `serving/mock-worker/README.md`
- `worklog.md`
- `gateway/app/grpc/gen/*`
- `serving/mock-worker/grpc_gen/*`

## 요약
- proto → Python 코드 생성 스크립트 추가
- gRPC 서버(모크 워커)와 gRPC 클라이언트 스모크 추가
- 실행 가이드 문서화

---

# 작업 기록: gRPC gen 코드 이해 가이드 추가

## 작업 목적
- 자동 생성된 gRPC Python 코드(pb2/pb2_grpc)를 이해하기 위한 설명 문서를 추가했습니다.

## 변경 파일
- `docs/grpc_gen_guide.md`
- `worklog.md`

## 요약
- pb2/pb2_grpc 역할과 읽는 법 정리

---

# 작업 기록: gRPC gen 생성 경로 명시

## 작업 목적
- gen 코드가 `scripts/gen_grpc.sh`로 생성된다는 점을 문서에 명확히 표시했습니다.

## 변경 파일
- `docs/grpc_gen_guide.md`
- `docs/grpc_agent_guide.md`
- `worklog.md`

## 요약
- 자동 생성 코드의 생성 방식/주의사항 추가

---

# 작업 기록: LLM 서빙 연동 가이드 추가

## 작업 목적
- 통합 사용 시나리오(3)인 vLLM/SGLang 연동의 기본 흐름을 문서화했습니다.

## 변경 파일
- `docs/llm_serving_agent_guide.md`
- `worklog.md`

## 요약
- vLLM 기본 + SGLang 보조 사용 원칙과 라우팅/헬스체크 기준 정리

---

# 작업 기록: LLM 서빙 가이드 상세 보강

## 작업 목적
- vLLM/SGLang 연동 문서에 실행 예시와 대안 경로를 추가했습니다.

## 변경 파일
- `docs/llm_serving_agent_guide.md`
- `worklog.md`

## 요약
- vLLM Compose 실행 예시 추가
- GPU 없는 환경의 대안(LiteLLM) 정리
- 헬스체크/관측 포인트 보강

---

# 작업 기록: SGLang Compose 스캐폴딩 추가

## 작업 목적
- vLLM/SGLang 연동을 위해 SGLang용 docker compose 템플릿을 추가했습니다.

## 변경 파일
- `docker-compose.sglang.yml`
- `docs/llm_serving_agent_guide.md`
- `worklog.md`

## 요약
- SGLang 템플릿 compose와 실행 예시 추가

---

# 작업 기록: SGLang 실행 스크립트/헬스체크 추가

## 작업 목적
- SGLang 템플릿을 실제 실행 가능한 스크립트와 헬스체크로 보강했습니다.

## 변경 파일
- `scripts/run_sglang.sh`
- `docs/llm_serving_agent_guide.md`
- `worklog.md`

## 요약
- SGLang 실행 스크립트 제공
- 헬스체크 URL 환경 변수 지원

---

# 작업 기록: Gateway gRPC 업스트림 연동

## 작업 목적
- MSA 통신 실 구현으로 Gateway가 gRPC 워커를 직접 호출할 수 있게 했습니다.

## 변경 파일
- `gateway/app/services/proxy.py`
- `gateway/app/grpc/__init__.py`
- `docs/grpc_agent_guide.md`
- `gateway/README.md`
- `worklog.md`

## 요약
- `grpc://` 업스트림 지원 추가
- gRPC 생성 코드 로딩 방식 정리
- 문서에 gRPC 업스트림 사용 예시 추가

---

# 작업 기록: gRPC 응답 변환 흐름 정리

## 작업 목적
- Gateway의 `_grpc_response` 동작을 문서로 정리해 이해하기 쉽게 했습니다.

## 변경 파일
- `docs/grpc_agent_guide.md`
- `worklog.md`

## 요약
- REST → gRPC 변환 흐름과 관련 코드 경로 설명 추가
