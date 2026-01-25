# Agent Client Guide (REST)

이 문서는 외부 Agent가 Nexus Gateway를 호출하기 위한 **최소 사용 방법**을 설명합니다.

---

## 1) 기본 호출 흐름

1. API Key 또는 JWT 발급
2. Gateway 엔드포인트 호출
3. 응답(JSON) 수신

---

## 2) 엔드포인트

- `POST /v1/chat/completions`
- Base URL 예시: `http://localhost:8000`

---

## 3) 필수 헤더

- `Content-Type: application/json`
- `X-API-Key: <your-key>` 또는
- `Authorization: Bearer <jwt>`

권장 헤더:
- `X-Request-Id`: 요청 고유 ID
- `X-Trace-Id`: 추적 ID

---

## 4) 요청 예시 (curl)

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key" \
  -d '{"model":"mock","messages":[{"role":"user","content":"hello"}]}'
```

---

## 5) 요청 예시 (Python)

```python
import requests

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "dev-key",
    "X-Request-Id": "req-123",
    "X-Trace-Id": "trace-123",
}
payload = {
    "model": "mock",
    "messages": [{"role": "user", "content": "hello"}],
}

res = requests.post(url, json=payload, headers=headers, timeout=10)
print(res.status_code, res.json())
```

---

## 6) 응답 예시

```json
{
  "id": "cmpl-123",
  "object": "chat.completion",
  "created": 1730000000,
  "model": "mock",
  "choices": [{"index": 0, "message": {"role": "assistant", "content": "hi"}}]
}
```

---

## 7) 실패 시 체크리스트

- 인증 헤더가 있는지 확인
- `GATEWAY_API_KEYS`에 키가 등록되었는지 확인
- `/health` 정상 여부 확인
- `X-Request-Id`로 로그에서 요청 추적
