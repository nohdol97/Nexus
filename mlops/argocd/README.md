# Argo CD Scaffolding

This folder provides a minimal Argo CD Application template.

## Install (kind/local)

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Apply application

```bash
kubectl apply -f mlops/argocd/application.yaml
kubectl get applications -n argocd
```

## Notes
- `repoURL` should point at your Git repository.
- Use `path` to point at the desired Kustomize overlay.
- `namespace: argocd` assumes the default Argo CD install namespace.
