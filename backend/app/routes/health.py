"""
Health check and system status endpoints
"""
from fastapi import APIRouter
from datetime import datetime

from app import __version__
from app.config import settings
from app.utils.responses import success_response

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status of the API
    """
    return success_response(
        data={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": settings.APP_NAME,
            "version": __version__,
            "environment": settings.ENVIRONMENT
        },
        message="Service is healthy"
    )


@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check endpoint with system information
    
    Returns:
        Detailed health status including configuration
    """
    return success_response(
        data={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": {
                "name": settings.APP_NAME,
                "version": __version__,
                "environment": settings.ENVIRONMENT,
                "debug": settings.DEBUG
            },
            "server": {
                "host": settings.HOST,
                "port": settings.PORT
            },
            "database": {
                "url": settings.DATABASE_URL.split("://")[0] + "://***"  # Hide credentials
            }
        },
        message="Service is healthy"
    )
