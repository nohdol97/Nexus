# vLLM 서빙

이 폴더는 OpenAI 호환 API로 vLLM을 실행하기 위한 최소 예제를 제공합니다. 로컬 테스트나 게이트웨이 연동 확인에 사용하세요.

## 로컬 실행 (Python)

```bash
export MODEL_ID="meta-llama/Meta-Llama-3-8B-Instruct"
export HOST="0.0.0.0"
export PORT="8001"

python -m vllm.entrypoints.openai.api_server \
  --model "$MODEL_ID" \
  --host "$HOST" \
  --port "$PORT"
```

`MODEL_ID`는 Hugging Face 모델 식별자이며, 필요 시 토큰/HF 캐시 설정을 함께 구성하세요.

## Docker 실행 (GPU 호스트)

```bash
docker run --rm --gpus all -p 8001:8001 \
  vllm/vllm-openai:latest \
  --model "$MODEL_ID" \
  --host 0.0.0.0 \
  --port 8001
```

GPU가 없는 환경에서는 실행되지 않으므로, CPU 테스트는 mock 워커를 사용하세요.

## 게이트웨이 연동

```bash
export GATEWAY_UPSTREAMS="llama=http://localhost:8001"
export GATEWAY_DEFAULT_UPSTREAM="llama"
```
