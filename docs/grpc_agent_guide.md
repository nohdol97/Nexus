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
