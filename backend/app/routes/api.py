"""
Main API router - aggregates all route modules
"""
from fastapi import APIRouter

from app.routes import health

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include route modules
api_router.include_router(health.router, tags=["Health"])
