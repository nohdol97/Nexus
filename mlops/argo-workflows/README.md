# Argo Workflows 스캐폴딩

이 폴더는 배치 작업을 위한 최소 Argo Workflow 템플릿을 제공합니다. 실제 배치 작업으로 교체하기 위한 출발점입니다.

## 적용 (Argo Workflows 설치 후)

```bash
kubectl apply -f mlops/argo-workflows/rbac.yaml
kubectl apply -f mlops/argo-workflows/workflow.yaml
```

## 참고
- 컨테이너 이미지/명령을 실제 배치 작업으로 변경하세요.
