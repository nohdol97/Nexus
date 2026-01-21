# SGLang GPU Worker (Skeleton)

This is a template for adding a SGLang-based worker.

- Replace `REPLACE_WITH_SGLANG_IMAGE` with your actual image.
- Update the container command/args to the SGLang server entrypoint you use.
- Apply after the GPU overlay:

```bash
kubectl apply -k k8s/overlays/gpu
kubectl apply -k k8s/overlays/gpu/sglang
```

If you enable this worker, add it to the gateway upstreams and route policies.
