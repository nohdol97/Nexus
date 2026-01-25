# Mock Model Worker

CPU-only, OpenAI-compatible mock worker used for local/K8s validation.

## Local run

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001
```

## Docker run

```bash
docker build -t nexus-model-worker:latest -f serving/mock-worker/Dockerfile serving/mock-worker
docker run --rm -p 8001:8001 -e WORKER_MODEL_NAME=mock-worker nexus-model-worker:latest
```

## Quick test

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"mock-worker","messages":[{"role":"user","content":"hello"}]}'
```

## gRPC server (optional)

```bash
python3 serving/mock-worker/grpc_server.py
```

- Default port: `50051`
