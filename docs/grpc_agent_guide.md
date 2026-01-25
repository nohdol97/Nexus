# 내부 gRPC Agent 가이드

이 문서는 내부 서비스(Agent)가 gRPC로 Model Worker에 접근하는 기본 흐름을 설명합니다.

---

## 1) 구성 요소

- `contracts/nexus_inference.proto`: gRPC 계약
- `serving/mock-worker/grpc_server.py`: gRPC 서버 (Mock Worker)
- `gateway/scripts/grpc_agent_smoke.py`: gRPC 클라이언트 스모크

---

## 2) 코드 생성 (proto → Python)

```bash
./scripts/gen_grpc.sh
```

> `grpcio-tools`가 필요합니다. (예: `python3 -m pip install --user grpcio-tools`)
> 위 스크립트가 `gen` 폴더의 자동 생성 코드를 만듭니다.

---

## 3) gRPC 서버 실행 (Mock Worker)

```bash
python3 serving/mock-worker/grpc_server.py
```

- 기본 포트: `50051`
- 환경 변수:
  - `GRPC_HOST` (기본: `0.0.0.0`)
  - `GRPC_PORT` (기본: `50051`)
  - `WORKER_MODEL_NAME` (기본: `mock-worker`)

---

## 4) gRPC 클라이언트 실행 (Agent)

```bash
python3 gateway/scripts/grpc_agent_smoke.py
```

환경 변수 예시:

```bash
GRPC_TARGET=localhost:50051 MODEL=mock-worker TEXT=hello \
python3 gateway/scripts/grpc_agent_smoke.py
```

---

## 5) 체크리스트

- [ ] `scripts/gen_grpc.sh` 실행 완료
- [ ] gRPC 서버가 `50051`에서 대기 중
- [ ] 클라이언트 호출 시 응답 수신

---

## 6) Gateway에서 gRPC 업스트림 사용

Gateway가 gRPC 워커를 호출하도록 업스트림을 등록할 수 있습니다.

```bash
GATEWAY_UPSTREAMS="worker=grpc://localhost:50051"
GATEWAY_DEFAULT_UPSTREAM="worker"
```

---

## 7) Gateway 내부 동작 (_grpc_response)

Gateway는 REST 요청을 gRPC 요청으로 변환해 워커로 전달합니다.

동작 흐름:
1. 업스트림 주소에서 `host:port` 추출 (`grpc://host:port`)
2. gRPC 채널/Stub 생성 또는 재사용
3. proto 메시지(`ChatCompletionRequest`) 구성
4. `ChatCompletion` 호출
5. gRPC 응답을 OpenAI 호환 JSON으로 변환해 반환

관련 코드:
- `gateway/app/services/proxy.py`의 `_grpc_response`
