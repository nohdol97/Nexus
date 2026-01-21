# KServe Scaffolding

This folder provides a minimal InferenceService template for KServe.

## Apply (after KServe is installed)

```bash
kubectl apply -f k8s/kserve/inferenceservice.yaml
```

## Notes
- Replace the model ID, image, and resources for your GPU environment.
- `model-worker-secrets` must include `HF_TOKEN` if the model is gated.
