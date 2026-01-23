from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone


def main() -> None:
    quant_method = os.getenv("QUANT_METHOD", "none")
    report = {
        "status": "ok",
        "quant_method": quant_method,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    output_path = Path("/workspace/quantization_report.json")
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
