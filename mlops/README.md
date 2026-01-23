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
kubectl apply -f mlops/kubeflow/scripts-configmap.yaml
kubectl apply -f mlops/kubeflow/pipeline.yaml
```

## 파이프라인 결과물(예시)

- `validation.json`: 데이터 검증 결과
- `quantization_report.json`: 양자화 요약
- `registry.json`: 모델 등록 정보
- `model_uri.txt`: 배포 기준 모델 URI
- `kserve_manifest.yaml`: 배포 템플릿(예시)
- `gitops/`: GitOps 대상 경로에 복사된 배포 파일 (옵션)

## GitOps 연계 흐름

- 파이프라인이 `kserve_manifest.yaml`을 생성
- 해당 파일을 Git에 커밋하면 Argo CD가 자동 동기화
- 상세 문서: `mlops/gitops/README.md`
- 파이프라인에서 사용하는 GitOps 스크립트: `mlops/gitops/gitops_commit_step.py`

## Argo CD 앱 템플릿

```bash
kubectl apply -f mlops/argocd/application.yaml
```

## MLflow 레지스트리 연동 정리

- 문서 위치: `mlops/mlflow/README.md`
- 모델 URI 기준으로 배포 단계와 연결

## Argo Workflows 템플릿

```bash
kubectl apply -f mlops/argo-workflows/workflow.yaml
```

## Airflow 스캐폴딩

- 위치: `mlops/airflow/README.md`
