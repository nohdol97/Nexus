from __future__ import annotations

import os
import sys
import uuid

import grpc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GATEWAY_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
GEN_DIR = os.path.join(GATEWAY_DIR, "app", "grpc", "gen")
for path in (GATEWAY_DIR, GEN_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

import nexus_inference_pb2 as pb2  # noqa: E402
import nexus_inference_pb2_grpc as pb2_grpc  # noqa: E402

TARGET = os.getenv("GRPC_TARGET", "localhost:50051")
MODEL = os.getenv("MODEL", "mock-worker")
TEXT = os.getenv("TEXT", "hello")
REQUEST_ID = os.getenv("REQUEST_ID", str(uuid.uuid4()))
TRACE_ID = os.getenv("TRACE_ID", REQUEST_ID)


def main() -> None:
    channel = grpc.insecure_channel(TARGET)
    stub = pb2_grpc.InferenceServiceStub(channel)
    request = pb2.ChatCompletionRequest(
        request_id=REQUEST_ID,
        trace_id=TRACE_ID,
        idempotency_key="",
        model=MODEL,
        messages=[pb2.Message(role="user", content=TEXT)],
        metadata={},
    )
    response = stub.ChatCompletion(request, timeout=10)
    print(response)


if __name__ == "__main__":
    main()
