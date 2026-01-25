from __future__ import annotations

import os
import sys
import time
import uuid
from concurrent import futures

import grpc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEN_DIR = os.path.join(BASE_DIR, "grpc_gen")
if GEN_DIR not in sys.path:
    sys.path.insert(0, GEN_DIR)

import nexus_inference_pb2 as pb2  # noqa: E402
import nexus_inference_pb2_grpc as pb2_grpc  # noqa: E402

MODEL_NAME = os.getenv("WORKER_MODEL_NAME", "mock-worker")
GRPC_HOST = os.getenv("GRPC_HOST", "0.0.0.0")
GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))


class InferenceService(pb2_grpc.InferenceServiceServicer):
    def ChatCompletion(
        self, request: pb2.ChatCompletionRequest, context: grpc.ServicerContext
    ) -> pb2.ChatCompletionResponse:
        user_text = ""
        for message in reversed(request.messages):
            if message.role == "user":
                user_text = message.content
                break

        content = f"mock response: {user_text}" if user_text else "mock response"
        now = int(time.time())
        request_id = request.request_id or str(uuid.uuid4())
        trace_id = request.trace_id or request_id
        model_name = request.model or MODEL_NAME
        return pb2.ChatCompletionResponse(
            request_id=request_id,
            trace_id=trace_id,
            model=model_name,
            output=content,
            latency_ms=0.0,
        )

    def Health(
        self, request: pb2.HealthRequest, context: grpc.ServicerContext
    ) -> pb2.HealthResponse:
        return pb2.HealthResponse(status="ok")


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_InferenceServiceServicer_to_server(InferenceService(), server)
    server.add_insecure_port(f"{GRPC_HOST}:{GRPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
