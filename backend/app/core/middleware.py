from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import HTTPMiddleware
import time
import uuid
import logging
from app.core.logging import request_id_var, get_logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request_id_var.set(request_id)
        request.state.request_id = request_id
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception as exc:
            raise exc
        finally:
            duration = time.time() - start_time
            response.headers["X-Request-ID"] = request_id
            
            if not request.url.path.startswith("/docs") and not request.url.path.startswith("/openapi"):
                from app.core.logging import log_request
                logger = get_logger("access")
                log_request(
                    logger=logger,
                    method=request.method,
                    path=str(request.url.path),
                    status_code=response.status_code,
                    duration=duration,
                    request_id=request_id,
                )
        
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        logger = get_logger("request")
        
        request_id = getattr(request.state, "request_id", None)
        
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={"extra_fields": {"request_id": request_id}}
        )
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            logger.info(
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "extra_fields": {
                        "request_id": request_id,
                        "duration_ms": round(duration * 1000, 2),
                        "status_code": response.status_code,
                    }
                }
            )
            
            return response
        except Exception as exc:
            duration = time.time() - start_time
            
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "extra_fields": {
                        "request_id": request_id,
                        "duration_ms": round(duration * 1000, 2),
                        "error": str(exc),
                    }
                }
            )
            raise


def setup_middleware(app):
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(LoggingMiddleware)
