from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        extra_fields = (
            "event",
            "request_id",
            "trace_id",
            "method",
            "path",
            "status",
            "duration_ms",
            "upstream",
            "fallback_model",
            "client_ip",
            "shadow",
            "auth_method",
            "principal_hash",
            "audit_outcome",
            "audit_reason",
            "error",
            "rate_limited",
        )
        for field in extra_fields:
            if hasattr(record, field):
                value = getattr(record, field)
                if value is not None:
                    log[field] = value
        if record.exc_info:
            log["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log, ensure_ascii=True, separators=(",", ":"))


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("gateway")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger
