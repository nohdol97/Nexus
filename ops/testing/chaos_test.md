# 장애 주입(Chaos) 테스트 가이드

이 문서는 최소한의 장애 주입 시나리오를 정의합니다.
운영 안정성을 확인하기 위해 **짧고 제한된 범위**로 수행합니다.

---

## 1) 목표

- 장애 발생 시 서비스 연속성 확인
- Circuit Breaker / Fallback 동작 검증
- 장애 시 로그/알림이 정상 발생하는지 확인

---

## 2) 최소 시나리오 (단기)

### 2.1 업스트림 강제 중단
- 대상: mock worker 또는 vLLM 컨테이너
- 방법: 컨테이너 중지
- 기대 결과:
  - Circuit Breaker OPEN
  - Fallback 동작
  - 에러 로그/알림 발생

### 2.2 지연 시간 강제 증가
- 대상: 업스트림 응답 지연
- 방법: mock worker에 인위적 sleep 추가(테스트 전용)
- 기대 결과:
  - timeout 발생
  - 재시도/에러율 증가 감지

### 2.3 Redis 비활성화
- 대상: Redis rate limiter
- 방법: Redis 컨테이너 중지
- 기대 결과:
  - Rate limit backend error 로그
  - 기본 처리 계속 수행

---

## 3) 체크리스트

- [ ] 장애 상황에서도 Gateway는 살아있는가?
- [ ] Circuit Breaker가 열리는가?
- [ ] Fallback이 활성화되는가?
- [ ] 로그/알림이 남는가?
