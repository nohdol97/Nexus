# MSA 통신 가이드 (REST + gRPC)

이 문서는 Nexus 플랫폼의 서비스 간 통신 규칙을 정의합니다.
Gateway, Worker, MLOps 구성 요소 간 동작이 **일관되게** 유지되도록
버전 관리, 신뢰성, 추적 가능성을 기준으로 정리했습니다.

---

## 1) 범위

- 내부 서비스 간(S2S) 통신
- REST(HTTP/JSON) 및 gRPC(Protobuf)
- 요청/응답 계약, 에러 포맷, 타임아웃, 멱등성 규칙

---

## 2) 핵심 원칙

- API 버전 고정(경로 또는 패키지 버전)
- 기본값은 **하위 호환 유지**
- 멱등성 키로 안전한 재시도 보장
- 데드라인/타임아웃은 **필수 설정**
- Correlation/Trace 헤더는 **필수 전파**

---

## 3) REST 가이드

### 3.1 필수 헤더

- `X-Request-Id`: 고유 요청 ID
- `X-Trace-Id`: 추적 ID (request ID와 동일 가능)
- `Idempotency-Key`: 쓰기 작업 시 필수
- `Content-Type: application/json`

### 3.2 에러 포맷 (JSON)

```json
{
  "error": {
    "code": "UPSTREAM_TIMEOUT",
    "message": "upstream did not respond in time",
    "request_id": "<uuid>",
    "retryable": true
  }
}
```

### 3.3 상태 코드

- `200/201/202`: 성공
- `400`: 입력 오류(재시도 불가)
- `401/403`: 인증/권한 오류
- `404`: 리소스 없음
- `409`: 충돌(멱등성 충돌 포함)
- `429`: 호출 제한 또는 Load Shedding
- `5xx`: 서버 장애(대부분 재시도 가능)

### 3.4 타임아웃/재시도

- 구간별 타임아웃 설정 (gateway -> worker, worker -> storage)
- 재시도 가능한 오류는 **지수 백오프** 적용
- `Retry-After` 헤더가 있으면 준수

---

## 4) gRPC 가이드

### 4.1 gRPC를 쓰는 경우

- 내부 호출 TPS가 높을 때
- 저지연이 중요하고 스키마 엄격성이 필요할 때
- 스트리밍 응답이 필요할 때(선택)

### 4.2 데드라인 전파

- 호출 측에서 반드시 데드라인 설정
- 남은 데드라인을 하위 호출에 전파

### 4.3 상태 매핑

- `OK`: 성공
- `INVALID_ARGUMENT`: 입력 검증 오류
- `UNAUTHENTICATED/ PERMISSION_DENIED`: 인증 문제
- `RESOURCE_EXHAUSTED`: Rate Limit/Load Shedding
- `UNAVAILABLE/DEADLINE_EXCEEDED`: 재시도 가능

### 4.4 Proto 위치

- `contracts/nexus_inference.proto`

### 4.5 Proto 읽는 법

- `syntax = "proto3"`: Protobuf 문법 버전
- `package nexus.inference.v1`: 네임스페이스 + 버전
- `service InferenceService`: 호출 가능한 API 묶음
- `rpc ChatCompletion(...) returns (...)`: 메서드 이름과 요청/응답 타입
- `message ChatCompletionRequest`: 요청 데이터 형태
- `repeated`: 배열(리스트)
- `map<string, string>`: 키-값 딕셔너리
- 필드 번호(`= 1`, `= 2`, ...): 호환성 식별자(변경 금지)

---

## 5) 분산 트랜잭션 패턴

- 다단계 작업은 **Saga** 패턴 선호
- 이중 기록 방지를 위해 **Outbox** 패턴 사용
- 재시도 가능한 작업에는 멱등성 키 필수

---

## 6) 예시: Gateway -> Worker

### REST 예시

`POST /v1/inference/chat`

Headers:
- `X-Request-Id`
- `X-Trace-Id`
- `Idempotency-Key`

Body:
```json
{
  "model": "mock",
  "messages": [
    {"role": "user", "content": "hello"}
  ]
}
```

### gRPC 예시

`contracts/nexus_inference.proto`의 `InferenceService.ChatCompletion` 사용.

---

## 7) 체크리스트

- [ ] Request/Trace ID가 End-to-End로 전파되는가?
- [ ] 각 구간에 타임아웃이 설정되어 있는가?
- [ ] 재시도는 멱등성을 보장하는가?
- [ ] 에러 포맷이 일관된가?
- [ ] 계약 변경이 버전화되어 있는가?
