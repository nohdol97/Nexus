# Kibana Dashboard Template (Gateway Logs)

> 이 문서는 Kibana에서 대시보드를 구성할 때 참고할 템플릿입니다.

## 1) 필수 패널

### 1-1. 에러율 추이
- KQL: `status >= 500`
- 시각화: Line chart
- 목적: 5xx 급증 구간 확인

### 1-2. 지연시간 분포
- 필드: `duration_ms`
- 시각화: Histogram
- 목적: 느린 요청 분포 파악

### 1-3. 엔드포인트별 요청 수
- 필드: `path`
- 시각화: Bar chart
- 목적: 트래픽 집중 구간 확인

### 1-4. 업스트림별 요청 비율
- 필드: `upstream`
- 시각화: Pie chart
- 목적: 라우팅 비율 확인

### 1-5. 최근 에러 로그 테이블
- KQL: `status >= 500`
- 시각화: Table
- 필드: `timestamp`, `path`, `status`, `request_id`, `trace_id`, `upstream`

---

## 2) 추천 패널

### 2-1. 레이트 리밋 응답
- KQL: `status = 429`
- 시각화: Line chart

### 2-2. Circuit Breaker 로그
- KQL: `message : "circuit"`
- 시각화: Table

### 2-3. 클라이언트 IP Top N
- 필드: `client_ip`
- 시각화: Bar chart

---

## 3) 대시보드 운영 팁
- 시간 범위를 15분/1시간 단위로 먼저 줄여서 탐색
- 에러율 패널에서 급증 구간을 찾고 → 로그 테이블로 drill-down
- 업스트림 비율과 지연시간 분포를 함께 보며 병목 원인 확인
