from __future__ import annotations

import os
from pathlib import Path
from textwrap import dedent


def main() -> None:
    model_uri_file = Path(os.getenv("MODEL_URI_FILE", "/workspace/model_uri.txt"))
    if model_uri_file.exists():
        model_uri = model_uri_file.read_text(encoding="utf-8").strip()
    else:
        model_uri = os.getenv("MODEL_URI", "models:/nexus-llm/1")

    manifest = dedent(
        f"""
        apiVersion: serving.kserve.io/v1beta1
        kind: InferenceService
        metadata:
          name: llm-vllm
          namespace: nexus
        spec:
          predictor:
            container:
              image: vllm/vllm-openai:latest
              env:
                - name: MODEL_URI
                  value: "{model_uri}"
        """
    ).strip()

    output_path = Path("/workspace/kserve_manifest.yaml")
    output_path.write_text(manifest + "\n", encoding="utf-8")
    print(f"deployment_manifest_written={output_path}")


if __name__ == "__main__":
    main()
