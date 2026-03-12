from typing import Optional, Any, Dict
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback
import uuid
import time


class ErrorResponse:
    def __init__(
        self,
        error: str,
        message: str,
        status_code: int = 500,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[float] = None,
    ):
        self.error = error
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        self.details = details
        self.timestamp = timestamp or time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "error": self.error,
            "message": self.message,
            "timestamp": self.timestamp,
        }
        if self.request_id:
            result["request_id"] = self.request_id
        if self.details:
            result["details"] = self.details
        return result


class BaseAPIException(Exception):
    def __init__(
        self,
        message: str,
        error: str = "internal_error",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error = error
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ResourceNotFoundError(BaseAPIException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} not found: {resource_id}",
            error="resource_not_found",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "resource_id": resource_id},
        )


class ValidationError(BaseAPIException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error="validation_error",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class AuthenticationError(BaseAPIException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error="authentication_error",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AuthorizationError(BaseAPIException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            error="authorization_error",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class RateLimitError(BaseAPIException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            error="rate_limit_exceeded",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


class ExternalServiceError(BaseAPIException):
    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} error: {message}",
            error="external_service_error",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details={"service": service},
        )


class DatabaseError(BaseAPIException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            error="database_error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    
    error_response = ErrorResponse(
        error="http_exception",
        message=exc.detail,
        status_code=exc.status_code,
        request_id=request_id,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", ""),
        })
    
    error_response = ErrorResponse(
        error="validation_error",
        message="Request validation failed",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        request_id=request_id,
        details={"errors": errors},
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.to_dict(),
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    
    error_message = "Database operation failed"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, IntegrityError):
        error_message = "Data integrity constraint violated"
        status_code = status.HTTP_409_CONFLICT
    
    error_response = ErrorResponse(
        error="database_error",
        message=error_message,
        status_code=status_code,
        request_id=request_id,
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.to_dict(),
    )


async def base_api_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    
    error_response = ErrorResponse(
        error=exc.error,
        message=exc.message,
        status_code=exc.status_code,
        request_id=request_id,
        details=exc.details,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.to_dict(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    
    error_response = ErrorResponse(
        error="internal_server_error",
        message="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        request_id=request_id,
        details={"exception_type": type(exc).__name__},
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.to_dict(),
    )
