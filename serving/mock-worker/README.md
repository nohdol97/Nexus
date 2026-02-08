# Mock 모델 워커

로컬/K8s 검증용으로 사용하는 CPU 전용 OpenAI 호환 모의 워커입니다. 실제 모델 대신 빠른 연동 테스트에 적합합니다.

## 로컬 실행

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001
```

## Docker 실행

```bash
docker build -t nexus-model-worker:latest -f serving/mock-worker/Dockerfile serving/mock-worker
docker run --rm -p 8001:8001 -e WORKER_MODEL_NAME=mock-worker nexus-model-worker:latest
```

## 지연/실패 시뮬레이션 (선택)

```bash
WORKER_DELAY_MS=500
WORKER_FAIL_RATE=0.1
```

> 지연은 밀리초(ms), 실패율은 0.0 ~ 1.0 범위입니다.

## 빠른 테스트

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"mock-worker","messages":[{"role":"user","content":"hello"}]}'
```

## gRPC 서버 (선택)

```bash
python3 serving/mock-worker/grpc_server.py
```

- 기본 포트: `50051`
