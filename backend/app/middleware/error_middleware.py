"""
Global error handling middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.exceptions import BaseAPIException
from app.utils.responses import error_response


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled exceptions
    
    Args:
        request: FastAPI request object
        exc: Exception that was raised
    
    Returns:
        JSONResponse with error details
    """
    return error_response(
        message="Internal server error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handler for HTTP exceptions
    
    Args:
        request: FastAPI request object
        exc: HTTPException that was raised
    
    Returns:
        JSONResponse with error details
    """
    return error_response(
        message=exc.detail,
        status_code=exc.status_code
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler for validation exceptions (Pydantic validation errors)
    
    Args:
        request: FastAPI request object
        exc: RequestValidationError that was raised
    
    Returns:
        JSONResponse with validation error details
    """
    errors = {}
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors[field] = error["msg"]
    
    return error_response(
        message="Validation error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        errors=errors
    )


async def base_api_exception_handler(request: Request, exc: BaseAPIException) -> JSONResponse:
    """
    Handler for custom API exceptions
    
    Args:
        request: FastAPI request object
        exc: BaseAPIException that was raised
    
    Returns:
        JSONResponse with error details
    """
    return error_response(
        message=exc.detail,
        status_code=exc.status_code
    )
