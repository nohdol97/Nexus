# KServe Scaffolding

This folder provides a minimal InferenceService template for KServe.

## Apply (after KServe is installed)

```bash
kubectl apply -f k8s/kserve/inferenceservice.yaml
```

## Notes
- Replace the model ID, image, and resources for your GPU environment.
- `model-worker-secrets` must include `HF_TOKEN` if the model is gated.
- `MODEL_URI` should point to the MLflow registry version you want to deploy.

## Installation (reference)

KServe must be installed before applying the InferenceService.

```bash
# Check KServe CRDs
kubectl get crd | grep kserve
```

If KServe is not installed, follow the official installation guide for your cluster.
This repo does not include KServe install manifests.

## Checklist

- `k8s/kserve/checklist.md`
