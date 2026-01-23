# Argo Workflows Scaffolding

This folder provides a minimal Argo Workflow template for batch jobs.

## Apply (after Argo Workflows is installed)

```bash
kubectl apply -f mlops/argo-workflows/rbac.yaml
kubectl apply -f mlops/argo-workflows/workflow.yaml
```

## Notes
- Replace the container images/commands with real batch jobs.
