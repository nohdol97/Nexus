# vLLM Performance Tuning Report (Template)

> 이 문서는 **실측 데이터 기반**으로 튜닝 결과를 기록하기 위한 템플릿입니다.
> GPU 환경 확보 후 실제 수치로 채워 주세요.

## 1) 목적
- 처리량(Throughput)과 지연시간(Latency)을 개선하기 위한 파라미터 튜닝 결과 기록

## 2) 환경
- 엔진: vLLM
- 모델: (예: Llama 3 / Mistral)
- 하드웨어: (예: A100 80GB / H100 80GB)
- 설정 버전: (Git commit 또는 config 버전)

## 3) 워크로드
- 요청 유형: (예: /v1/chat/completions)
- 입력 길이: (예: 평균 1,000 tokens)
- 출력 길이: (예: 평균 200 tokens)
- 동시성(Concurrency): (예: 32)
- 측정 구간: (예: 10분)

## 4) 측정 지표
- Throughput (TPS)
- Latency p50 / p95 / p99
- GPU Utilization (%)
- Error Rate (% 5xx)

## 5) 변경 파라미터
- batch size
- max_num_seqs
- max_model_len
- tensor_parallel_size
- kv_cache_dtype
- 기타: (예: scheduling policy)

## 6) 결과 요약 (Before/After)

| 항목 | Before | After | 변화 |
| --- | --- | --- | --- |
| TPS |  |  |  |
| p95 latency |  |  |  |
| p99 latency |  |  |  |
| GPU utilization |  |  |  |
| Error rate |  |  |  |

## 7) 결론
- (예: batch size 증가로 TPS 개선, p95 약간 상승)

## 8) 다음 액션
- (예: 다른 max_model_len 조합 실험)
- (예: SGLang 비교 테스트)
