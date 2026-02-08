# KServe 스캐폴딩

이 폴더는 KServe InferenceService 최소 템플릿을 제공합니다. KServe가 설치된 클러스터에서만 적용할 수 있습니다.

## 적용 (KServe 설치 후)

```bash
kubectl apply -f k8s/kserve/inferenceservice.yaml
```

## 참고
- 모델 ID, 이미지, 리소스 요청/제한을 GPU 환경에 맞게 변경하세요.
- 게이티드 모델이면 `model-worker-secrets`에 `HF_TOKEN`이 필요합니다.
- `MODEL_URI`는 배포하려는 MLflow 레지스트리 버전을 가리켜야 합니다.

## 설치 (참고)

InferenceService를 적용하기 전에 KServe가 설치되어 있어야 합니다.

```bash
# KServe CRD 확인
kubectl get crd | grep kserve
```

KServe가 없다면 클러스터에 맞는 공식 설치 가이드를 사용하세요.
이 리포지토리에는 KServe 설치 매니페스트가 포함되어 있지 않습니다.

## 체크리스트

- `k8s/kserve/checklist.md`
