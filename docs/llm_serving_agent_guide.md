# LLM 서빙 연동 가이드 (vLLM 기본 + SGLang 보조)

이 문서는 내부 Agent가 **LLM 서빙 계층(vLLM/SGLang)** 을 사용하는 기본 흐름을 정리합니다.
GPU 환경이 필요하므로 로컬에서는 구조/흐름 확인 위주로 봅니다.

---

## 1) 기본 원칙

- vLLM을 기본 엔진으로 사용
- SGLang은 고급 프롬프트/워크플로우 제어가 필요한 경우 보조 엔진으로 사용
- 공통 규격은 Gateway의 OpenAI 호환 API 형태로 통일

---

## 2) 요청 흐름 (요약)

1. Agent → Gateway (REST)
2. Gateway → vLLM/SGLang (업스트림 선택)
3. 응답 수신 및 반환

---

## 3) 업스트림 등록 예시

```bash
GATEWAY_UPSTREAMS="vllm=http://vllm:8001;sglang=http://sglang:8002"
GATEWAY_FALLBACKS="vllm=sglang"
```

---

## 4) 헬스체크 기준

- vLLM: `/v1/models` (OpenAI 호환 상태 확인)
- SGLang: `/health` 또는 `/v1/models` (구성에 따라 변경 가능)

---

## 5) 라우팅 예시

```bash
GATEWAY_ROUTE_POLICIES='{
  "chat": {"strategy":"weighted","targets":[{"name":"vllm","weight":90},{"name":"sglang","weight":10}]}
}'
```

---

## 6) 운영 체크리스트

- [ ] GPU 환경에서 vLLM 정상 기동
- [ ] SGLang 보조 엔진 정상 기동
- [ ] Fallback 경로 동작 확인
- [ ] Throughput/Latency 측정 및 리포트 기록

---

## 7) vLLM 로컬 실행 예시 (GPU 필요)

```bash
MODEL_ID=meta-llama/Meta-Llama-3-8B-Instruct \\
  docker compose -f docker-compose.yml -f docker-compose.vllm.yml up --build
```

> GPU가 없는 환경에서는 vLLM 구동이 불가능합니다.

---

## 8) GPU가 없을 때 대안 (외부 API)

GPU가 없는 로컬 환경에서는 **LiteLLM 외부 모델**을 업스트림으로 등록해\n기능 흐름만 검증할 수 있습니다.

```bash
GATEWAY_UPSTREAMS="gpt-4o-mini=litellm://gpt-4o-mini"
```

---

## 9) 로그/지표 확인 포인트

- `/metrics`에서 업스트림 지연 시간 확인
- Kibana에서 `upstream`, `fallback_model` 필드 확인

---

## 10) SGLang Compose 스캐폴딩 (GPU 필요)

SGLang은 엔트리포인트/옵션이 환경마다 다르므로 **템플릿 형태**로 제공합니다.

```bash
SGLANG_IMAGE=<your-sglang-image> \\
SGLANG_COMMAND="<your-sglang-command>" \\
  docker compose -f docker-compose.yml -f docker-compose.sglang.yml up --build
```

> `docker-compose.sglang.yml`는 템플릿입니다. 이미지/커맨드는 실제 환경에 맞게 설정하세요.

---

## 11) SGLang 실행 스크립트 + 헬스체크

템플릿 설정을 손쉽게 실행하고, 기본 헬스체크까지 확인하려면 아래 스크립트를 사용합니다.

```bash
SGLANG_IMAGE=<your-sglang-image> \\
SGLANG_COMMAND="<your-sglang-command>" \\
  ./scripts/run_sglang.sh
```

헬스체크 경로가 다를 경우 환경 변수를 변경할 수 있습니다.

```bash
SGLANG_HEALTH_URL=http://localhost:8002/health \\
SGLANG_HEALTH_FALLBACK_URL=http://localhost:8002/v1/models \\
  ./scripts/run_sglang.sh
```
