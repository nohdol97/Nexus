# GitOps Integration Notes

This document describes how the pipeline output connects to Argo CD.

## Recommended flow

1) Kubeflow pipeline produces a deployment manifest:
   - Output: `/workspace/kserve_manifest.yaml`
2) A follow-up step commits the manifest into Git:
   - Example path: `deployments/kserve/llm-vllm.yaml`
3) Argo CD watches the repo path and syncs changes to the cluster.

## Why this matters

- The **pipeline creates artifacts** (what to deploy).
- **Git becomes the source of truth** (what is actually deployed).
- Argo CD **keeps the cluster in sync** with Git.

## Next step (optional)

Create a lightweight job that:
- Copies `kserve_manifest.yaml` to the Git repo path
- Commits & pushes
- Lets Argo CD reconcile automatically
