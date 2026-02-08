# Argo CD 스캐폴딩

이 폴더는 최소 Argo CD Application 템플릿을 제공합니다. GitOps 방식의 배포 동기화를 테스트하는 데 사용하세요.

## 설치 (kind/local)

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 애플리케이션 적용

```bash
kubectl apply -f mlops/argocd/application.yaml
kubectl get applications -n argocd
```

## 참고
- `repoURL`은 대상 Git 저장소로 변경하세요.
- `path`는 원하는 Kustomize 오버레이 경로를 가리켜야 합니다.
- `namespace: argocd`는 기본 Argo CD 설치 네임스페이스를 가정합니다.
