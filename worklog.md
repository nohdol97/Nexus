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
