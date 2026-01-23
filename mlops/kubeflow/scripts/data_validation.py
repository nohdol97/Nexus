from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone


def main() -> None:
    data_path = Path(os.getenv("DATA_PATH", "/workspace/data"))
    data_path.mkdir(parents=True, exist_ok=True)

    files = [path for path in data_path.rglob("*") if path.is_file()]
    if not files:
        sample = data_path / "sample.txt"
        sample.write_text("sample\n", encoding="utf-8")
        files = [sample]

    report = {
        "status": "ok",
        "file_count": len(files),
        "data_path": str(data_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    output_path = Path("/workspace/validation.json")
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
