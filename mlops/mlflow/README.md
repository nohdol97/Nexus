# MLflow Registry Scaffolding

This document outlines how model versions map to deployment.

## 기본 흐름

1) 학습 결과를 MLflow에 기록 (log_model)
2) 모델을 Registry에 등록 (register_model)
3) 버전/스테이지 관리 (Staging/Production)
4) 배포 단계에서 **모델 URI**를 사용해 서빙

## 모델 URI 예시

- `models:/nexus-llm/1`
- `models:/nexus-llm/Production`

## 배포와 연결하는 방법(예시)

- KServe/BentoML 배포 시 아래 값을 참조:
  - `MODEL_NAME`: `nexus-llm`
  - `MODEL_VERSION`: `Production`
  - `MODEL_URI`: `models:/nexus-llm/Production`

## 운영 팁

- 모델 버전마다 **학습 데이터 버전**과 **코드 커밋**을 태그로 남기기
- Production 승격은 리뷰/검증 후에만 수행
