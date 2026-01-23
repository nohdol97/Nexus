# KServe Deployment Checklist

Use this list before/after applying an InferenceService.

## Before apply

- KServe CRDs installed (`kubectl get crd | grep kserve`)
- GPU node available (if required)
- `model-worker-secrets` includes `HF_TOKEN` for gated models
- Image and model settings updated in `k8s/kserve/inferenceservice.yaml`

## Apply

```bash
kubectl apply -f k8s/kserve/inferenceservice.yaml
kubectl get inferenceservice -n nexus
```

## After apply

- InferenceService shows `READY=True`
- Pods are running without `CrashLoopBackOff`
- `/v1/chat/completions` works via Gateway route
