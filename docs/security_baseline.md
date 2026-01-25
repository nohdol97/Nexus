# 보안 강화 가이드 (단기)

이 문서는 Nexus 플랫폼의 **서비스 간 보안**과 **로그 보호**를 위한 기본 규칙을 정리합니다.
단기 운영 안정화 단계에서 바로 적용 가능한 수준으로 정리했습니다.

---

## 1) 목표

- 서비스 간 통신의 신뢰성 확보 (mTLS / 서비스 인증)
- 로그에서 개인정보(PII) 노출 최소화
- 감사 로그(audit log) 기준 통일

---

## 2) 서비스 간 인증 (S2S Auth)

- **API Key/JWT**: 내부 서비스 호출에도 인증 수단을 적용
- **권한 최소화**: 호출 서비스별로 접근 가능한 모델/엔드포인트 제한
- **정책 관리**: 중앙 정책(JSON)으로 관리해 운영 변경을 단순화

권장 정책 흐름:
1. 호출 서비스가 인증 정보(API Key 또는 JWT)를 보냄
2. Gateway가 인증/권한 검증
3. 요청 ID/Trace ID와 함께 업스트림으로 전달

---

## 3) mTLS (상호 TLS)

- **목적**: 서비스끼리 서로의 신원을 검증
- **적용 지점**: Gateway ↔ Worker, Worker ↔ 내부 서비스
- **운영 방식**:
  - Kubernetes 환경에서 Service Mesh(Istio/Linkerd) 활용
  - 또는 Ingress/Service 사이에서 mTLS 종단 구성

mTLS 적용 시 확인할 항목:
- 인증서 발급/회전 주기
- 인증서 폐기 시 즉시 차단 가능 여부
- 인증 실패 시 대응 정책

---

## 4) PII 마스킹

- **대상**: IP, 사용자 식별자, API 키, 계정 번호 등
- **기본 규칙**:
  - 로그에 **원문** 저장 금지
  - 해시 또는 마스킹 형태로 저장

Gateway에서는 기본적으로 **클라이언트 IP를 마스킹**하도록 설정합니다.

관련 설정:
- `GATEWAY_PII_MASKING_ENABLED` (기본: `true`)
- `GATEWAY_PII_HASH_SALT` (선택: 해시 난독화용)

---

## 5) 감사 로그(audit log) 표준

감사 로그는 **누가 어떤 요청을 했는지**를 추적하기 위한 로그입니다.

필수 필드 권장:
- `event`: `audit_auth`
- `request_id` / `trace_id`
- `method` / `path`
- `auth_method`: `api_key` or `jwt`
- `principal_hash`: 식별자 해시값
- `audit_outcome`: `allow` / `deny`
- `audit_reason`: 실패 사유(선택)

관련 설정:
- `GATEWAY_AUDIT_LOGGING_ENABLED` (기본: `true`)

---

## 6) 운영 체크리스트

- [ ] 서비스 간 호출에 인증 정보가 포함되는가?
- [ ] mTLS 인증 실패 시 차단되는가?
- [ ] 로그에 원문 PII가 남지 않는가?
- [ ] 감사 로그에 인증 결과가 남는가?
