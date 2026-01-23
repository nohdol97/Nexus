from __future__ import annotations

import json
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    workspace = Path("/workspace")
    summary = {
        "validation": read_json(workspace / "validation.json"),
        "quantization": read_json(workspace / "quantization_report.json"),
        "registry": read_json(workspace / "registry.json"),
    }

    output = workspace / "summary.json"
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
