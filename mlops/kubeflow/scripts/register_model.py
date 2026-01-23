from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone


def main() -> None:
    model_name = os.getenv("MODEL_NAME", "nexus-llm")
    model_version = os.getenv("MODEL_VERSION", "1")
    model_uri = f"models:/{model_name}/{model_version}"

    registry = {
        "model_name": model_name,
        "model_version": model_version,
        "model_uri": model_uri,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    model_uri_file = Path(os.getenv("MODEL_URI_FILE", "/workspace/model_uri.txt"))
    model_uri_file.write_text(model_uri, encoding="utf-8")

    registry_file = Path("/workspace/registry.json")
    registry_file.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(json.dumps(registry))


if __name__ == "__main__":
    main()
