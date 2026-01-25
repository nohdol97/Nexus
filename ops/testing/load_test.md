# 부하 테스트 가이드 (Load Test)

이 문서는 Nexus Gateway의 기본 부하 테스트 시나리오를 정의합니다.
단기 단계에서는 **최소 세트**만 수행합니다.

---

## 1) 목표

- 정상 트래픽 구간에서 안정성 확인
- 급증(Spike) 상황에서 오류율/지연 변화 확인
- Rate Limit, Circuit Breaker 동작 확인

---

## 2) 최소 시나리오 (단기)

### 2.1 Smoke (기본 기능 확인)
- RPS: 1 ~ 5
- 지속 시간: 1~3분
- 목적: 기능/인증 오류 확인

### 2.2 Baseline (기본 부하)
- RPS: 10 ~ 50 (환경에 맞게 조절)
- 지속 시간: 5~10분
- 목적: 평균 지연 시간/에러율 측정

### 2.3 Spike (급증)
- RPS: 50 -> 200 (짧게 상승)
- 지속 시간: 1~2분
- 목적: 급증 대응 능력, Rate Limit 동작 확인

---

## 3) 측정 지표

- `p50/p95/p99` 지연 시간
- HTTP 5xx 비율
- Rate Limit 발생 횟수
- Circuit Breaker OPEN 횟수

---

## 4) k6 예시

```bash
k6 run ops/testing/k6_smoke.js
```

환경 변수 예시:

```bash
K6_BASE_URL=http://localhost:8000 \
K6_API_KEY=dev-key \
k6 run ops/testing/k6_smoke.js
```

---

## 5) 결과 기록

- 결과는 `ops/perf_tuning_report.md`에 요약
- 실패 원인(응답 코드, 에러 로그)도 함께 기록
