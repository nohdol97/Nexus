# MLOps Scaffolding

This folder documents the planned ML pipeline and GitOps flow.

## 목표 파이프라인 (요약)

1) 데이터 검증 (Data Validation)
2) 양자화/최적화 (Quantization)
3) 모델 등록 (Model Registry / MLflow)
4) 배포 (KServe/BentoML)

## 구성 요소 역할

- **Kubeflow**: ML 파이프라인 실행/오케스트레이션
- **Argo CD**: GitOps 기반 배포 자동화
- **Argo Workflows / Airflow**: 배치/스케줄링 작업 관리
- **MLflow**: 모델 버전/메타데이터 관리

## 다음 단계

- Kubeflow 파이프라인 템플릿 추가
- Argo CD 앱 정의 예시 추가
- 모델 레지스트리/배포 연동 방식 정리

## Kubeflow 파이프라인 템플릿

```bash
kubectl apply -f mlops/kubeflow/pipeline.yaml
```
