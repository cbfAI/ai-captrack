import logging
import sys
import json
import uuid
import time
from typing import Any, Dict, Optional
from datetime import datetime
from contextvars import ContextVar
from functools import wraps

request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        request_id = request_id_var.get()
        if request_id:
            log_data["request_id"] = request_id
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        if record.levelno >= logging.ERROR:
            log_data["stack_trace"] = self.formatException(record.exc_info) if record.exc_info else None
        
        return json.dumps(log_data, ensure_ascii=False)


class FormattedStructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        request_id = request_id_var.get()
        rid = f"[{request_id[:8]}] " if request_id else ""
        
        message = f"{timestamp} {rid}{record.levelname:8} {record.name}: {record.getMessage()}"
        
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"
        
        return message


class ColoredFormatter(FormattedStructuredFormatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        reset = self.RESET if color else ""
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        request_id = request_id_var.get()
        rid = f"[{request_id[:8]}] " if request_id else ""
        
        message = f"{color}{timestamp} {rid}{record.levelname:8} {record.name}: {record.getMessage()}{reset}"
        
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"
        
        return message


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_json: bool = False,
) -> logging.Logger:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    root_logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    if enable_json:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(FormattedStructuredFormatter())
    
    root_logger.addHandler(console_handler)
    
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StructuredFormatter())
        root_logger.addHandler(file_handler)
    
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


class LoggerAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        extra_fields = kwargs.get("extra", {})
        if "extra_fields" not in kwargs:
            kwargs["extra"] = {"extra_fields": extra_fields}
        elif "extra_fields" in kwargs["extra"]:
            kwargs["extra"]["extra_fields"].update(extra_fields)
        return msg, kwargs


def log_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration: float,
    request_id: str,
    extra: Optional[Dict[str, Any]] = None,
):
    log_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration * 1000, 2),
        "request_id": request_id,
    }
    if extra:
        log_data.update(extra)
    
    if status_code >= 500:
        logger.error(f"HTTP {method} {path} {status_code} - {duration*1000:.2f}ms", extra=log_data)
    elif status_code >= 400:
        logger.warning(f"HTTP {method} {path} {status_code} - {duration*1000:.2f}ms", extra=log_data)
    else:
        logger.info(f"HTTP {method} {path} {status_code} - {duration*1000:.2f}ms", extra=log_data)


def log_function_call(
    logger: logging.Logger,
    func_name: str,
    duration: float,
    success: bool = True,
    error: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
):
    log_data = {
        "function": func_name,
        "duration_ms": round(duration * 1000, 2),
        "success": success,
    }
    if error:
        log_data["error"] = error
    if extra:
        log_data.update(extra)
    
    if success:
        logger.debug(f"Function {func_name} completed in {duration*1000:.2f}ms", extra=log_data)
    else:
        logger.error(f"Function {func_name} failed: {error}", extra=log_data)


def generate_request_id() -> str:
    return str(uuid.uuid4())


logger = get_logger(__name__)
