"""
Standardized API response utilities
"""
from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse
from fastapi import status


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
    
    Returns:
        JSONResponse with standardized format
    """
    response_data: Dict[str, Any] = {
        "success": True,
        "message": message,
        "status_code": status_code
    }
    
    if data is not None:
        response_data["data"] = data
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )


def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    errors: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        errors: Optional dictionary of field-specific errors
    
    Returns:
        JSONResponse with standardized format
    """
    response_data: Dict[str, Any] = {
        "success": False,
        "message": message,
        "status_code": status_code
    }
    
    if errors:
        response_data["errors"] = errors
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )


def paginated_response(
    data: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Success"
) -> JSONResponse:
    """
    Create a standardized paginated response
    
    Args:
        data: List of items for current page
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        message: Success message
    
    Returns:
        JSONResponse with pagination metadata
    """
    total_pages = (total + page_size - 1) // page_size  # Ceiling division
    
    response_data = {
        "success": True,
        "message": message,
        "status_code": status.HTTP_200_OK,
        "data": data,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response_data
    )
