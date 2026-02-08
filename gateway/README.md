# Nexus Gateway

인증, 라우팅, 속도 제한(Rate Limiting), 서킷 브레이커(Circuit Breaker) 기능을 갖춘 최소한의 FastAPI 게이트웨이 스켈레톤입니다.

## 빠른 시작

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## Docker 빠른 시작

```bash
docker compose up --build
```

- 게이트웨이: http://localhost:8000
- 지표 (Metrics): http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (기본값: admin / admin)
  - 대시보드: Nexus Gateway (자동 프로비저닝됨)

## vLLM 업스트림을 포함한 Docker 실행

NVIDIA 컨테이너 런타임이 설치된 GPU 호스트가 필요합니다.

```bash
MODEL_ID=meta-llama/Meta-Llama-3-8B-Instruct \
  docker compose -f docker-compose.yml -f docker-compose.vllm.yml up --build
```

## 설정

모든 설정은 `GATEWAY_` 접두사를 사용합니다.

- `GATEWAY_API_KEYS` (콤마로 구분, 기본값: `dev-key`)
- `GATEWAY_RATE_LIMIT_PER_MINUTE` (기본값: `60`)
- `GATEWAY_CIRCUIT_BREAKER_MAX_FAILURES` (기본값: `5`)
- `GATEWAY_CIRCUIT_BREAKER_RESET_SECONDS` (기본값: `30`)
- `GATEWAY_REQUEST_TIMEOUT_SECONDS` (기본값: `10`)
- `GATEWAY_UPSTREAMS` (예: `llama=http://localhost:8001;mock=mock://local;gpt-4o-mini=litellm://gpt-4o-mini`)
- `GATEWAY_DEFAULT_UPSTREAM` (선택 사항: 기본 업스트림 이름)
- `GATEWAY_FALLBACKS` (예: `llama=gpt-4o-mini,mock`)
- `GATEWAY_REDIS_URL` (선택 사항: Redis 기반 속도 제한 활성화)
- `GATEWAY_API_KEY_POLICIES` (선택 사항: 키별 규칙을 위한 JSON)
- `GATEWAY_ROUTE_POLICIES` (선택 사항: 가중치/카나리아 라우팅을 위한 JSON)
- `GATEWAY_JWT_SECRET` / `GATEWAY_JWT_PUBLIC_KEY` (선택 사항: JWT 유효성 검사 활성화)
- `GATEWAY_JWT_ALGORITHMS` (기본값: `HS256`)
- `GATEWAY_JWT_ISSUER` / `GATEWAY_JWT_AUDIENCE` (선택 사항)
- `GATEWAY_PII_MASKING_ENABLED` (기본값: `true`)
- `GATEWAY_PII_HASH_SALT` (선택 사항: 리액션(redaction)을 위한 해시 솔트)
- `GATEWAY_AUDIT_LOGGING_ENABLED` (기본값: `true`)
- `GATEWAY_SHADOW_ENABLED` (기본값: `false`)
- `GATEWAY_SHADOW_PERCENT` (기본값: `0`)
- `GATEWAY_SHADOW_TARGET` (선택 사항: 섀도우 트래픽 업스트림 이름)

## 관측성 (Observability)

- 지표 (Metrics): `GET /metrics` (Prometheus 형식)
- 로그: 표준 출력(stdout)으로 출력되는 JSON 구조화 로그

## LiteLLM 업스트림

`litellm://`을 사용하여 LiteLLM을 통해 외부 제공업체로 라우팅합니다. 모델 이름은 URL의 일부가 될 수 있습니다:

```
GATEWAY_UPSTREAMS="gpt-4o-mini=litellm://gpt-4o-mini"
```

폴백(Fallback) 예시:

```
GATEWAY_UPSTREAMS="llama=http://localhost:8001;gpt-4o-mini=litellm://gpt-4o-mini"
GATEWAY_FALLBACKS="llama=gpt-4o-mini"
```

## 라우팅 정책 (가중치/카나리아)

라우트 정책은 요청된 모델을 업스트림 타겟에 매핑하는 JSON입니다.
타겟은 `GATEWAY_UPSTREAMS`에 정의된 업스트림 이름과 일치해야 합니다.

```bash
GATEWAY_ROUTE_POLICIES='{
  "chat": {
    "strategy": "weighted",
    "targets": [{"name":"primary","weight":90},{"name":"canary","weight":10}]
  }
}'
```

카나리아 정책 예시:

```bash
GATEWAY_ROUTE_POLICIES='{
  "chat": {"strategy":"canary","primary":"primary","canary":"canary","percent":5}
}'
```

## API 키 정책

```bash
GATEWAY_API_KEY_POLICIES='{
  "dev-key": {"allowed_models":["chat"], "rate_limit_per_minute": 30}
}'
```

## JWT

```bash
GATEWAY_JWT_SECRET="my-secret"
GATEWAY_JWT_ALGORITHMS="HS256"
```

## gRPC 업스트림 예시

```bash
GATEWAY_UPSTREAMS="worker=grpc://localhost:50051"
GATEWAY_DEFAULT_UPSTREAM="worker"
```

## 예시 요청

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "X-API-Key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```

## 에이전트 클라이언트 스모크 테스트

```bash
./gateway/scripts/agent_client_smoke.sh
```

## gRPC 에이전트 스모크 테스트

```bash
python3 gateway/scripts/grpc_agent_smoke.py
```
