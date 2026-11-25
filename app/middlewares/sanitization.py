import json
import re
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

def _sanitize_value(value):
    if isinstance(value, str):
        cleaned = CONTROL_CHARS_RE.sub("", value).strip()
        return cleaned
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {k: _sanitize_value(v) for k, v in value.items()}
    return value

class InputSanitizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH") and "application/json" in request.headers.get("content-type", ""):
            raw_body = await request.body()
            if raw_body:
                try:
                    parsed = json.loads(raw_body)
                    sanitized = _sanitize_value(parsed)
                    new_body = json.dumps(sanitized).encode("utf-8")

                    async def receive():
                        return {"type": "http.request", "body": new_body, "more_body": False}

                    request._receive = receive
                except json.JSONDecodeError:
                    pass
        return await call_next(request)