import logging
import socket
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("gym_api.access")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        instance_id = socket.gethostname()

        response = await call_next(request)

        process_time_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Instance-ID"] = instance_id
        response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"

        logger.info(
            f"instance={instance_id} method={request.method} path={request.url.path} "
            f"status={response.status_code} client={request.client.host if request.client else 'unknown'} "
            f"duration={process_time_ms:.2f}ms"
        )
        return response