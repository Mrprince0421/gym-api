import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("gym_api")

def format_error(code: str, message: str, status_code: int, details=None):
    payload = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "status": status_code,
        }
    }
    if details:
        payload["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=payload)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return format_error(
        code="HTTP_ERROR",
        message=str(exc.detail),
        status_code=exc.status_code
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    clean_errors = [
        {"field": ".".join(str(loc) for loc in err["loc"]), "issue": err["msg"]}
        for err in exc.errors()
    ]
    return format_error(
        code="VALIDATION_ERROR",
        message="Dados de entrada inválidos.",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details=clean_errors
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Erro interno não tratado em {request.method} {request.url.path}")
    return format_error(
        code="INTERNAL_SERVER_ERROR",
        message="Ocorreu um erro interno inesperado no servidor.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )