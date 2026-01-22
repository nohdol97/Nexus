# Argo CD Scaffolding

This folder provides a minimal Argo CD Application template.

## Apply (after Argo CD is installed)

```bash
kubectl apply -f mlops/argocd/application.yaml
```

## Notes
- Update `repoURL` to your Git repository.
- Use `path` to point at the desired Kustomize overlay.
- `namespace: argocd` assumes the default Argo CD install namespace.
