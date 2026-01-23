from __future__ import annotations

import os
from pathlib import Path
import subprocess


def main() -> None:
    manifest_path = Path(os.getenv("MANIFEST_PATH", "/workspace/kserve_manifest.yaml"))
    output_dir = Path(os.getenv("GITOPS_OUTPUT_DIR", "/workspace/gitops"))
    repo_url = os.getenv("GITOPS_REPO_URL", "")
    git_ref = os.getenv("GITOPS_GIT_REF", "main")
    target_path = os.getenv("GITOPS_TARGET_PATH", "deployments/kserve/llm-vllm.yaml")

    output_dir.mkdir(parents=True, exist_ok=True)

    if repo_url:
        subprocess.run(["git", "clone", "--depth", "1", "--branch", git_ref, repo_url, str(output_dir)], check=True)

    target_file = output_dir / target_path
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(manifest_path.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"gitops_target_written={target_file}")


if __name__ == "__main__":
    main()
