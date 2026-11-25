from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.middlewares.request_logging import RequestLoggingMiddleware
from app.middlewares.sanitization import InputSanitizationMiddleware
from app.api.routes import auth, members, workouts, checkins

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# 1. Tratamento global padronizado de erros
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# 2. Middlewares (executam de fora para dentro: Logging -> Sanitização -> Rotas/Validação/Auth)
app.add_middleware(InputSanitizationMiddleware)
app.add_middleware(RequestLoggingMiddleware)

@app.get("/health", tags=["Saúde"])
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(members.router)
app.include_router(workouts.router)
app.include_router(checkins.router)