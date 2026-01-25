from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def load_grpc_modules() -> tuple[Any, Any]:
    gen_dir = Path(__file__).parent / "gen"
    if gen_dir.exists():
        gen_path = str(gen_dir)
        if gen_path not in sys.path:
            sys.path.insert(0, gen_path)
    try:
        import nexus_inference_pb2 as pb2  # type: ignore
        import nexus_inference_pb2_grpc as pb2_grpc  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "gRPC generated code is missing. Run ./scripts/gen_grpc.sh first."
        ) from exc
    return pb2, pb2_grpc
