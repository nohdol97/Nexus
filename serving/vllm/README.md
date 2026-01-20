# vLLM Serving

This folder contains a minimal setup to run vLLM with the OpenAI-compatible API.

## Local run (Python)

```bash
export MODEL_ID="meta-llama/Meta-Llama-3-8B-Instruct"
export HOST="0.0.0.0"
export PORT="8001"

python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_ID" \
  --host "$HOST" \
  --port "$PORT"
```

## Docker run (GPU host)

```bash
docker run --rm --gpus all -p 8001:8001 \
  vllm/vllm-openai:latest \
  --model "$MODEL_ID" \
  --host 0.0.0.0 \
  --port 8001
```

## Gateway integration

```bash
export GATEWAY_UPSTREAMS="llama=http://localhost:8001"
export GATEWAY_DEFAULT_UPSTREAM="llama"
```
