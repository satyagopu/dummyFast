# Example 1: Simple Function Dependency

from fastapi import FastAPI, Depends, Query ,APIRouter, Header, HTTPException
from typing import Optional
import asyncio  
from fastapi.exceptions import HTTPException
import time
from functools import lru_cache


app = FastAPI()

def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return")
):
    """Dependency that extracts and validates pagination parameters"""
    return {"skip": skip, "limit": limit}

@app.get("/products/")
def list_products(pagination: dict = Depends(get_pagination_params)):
    """List products with pagination"""
    return {
        "pagination": pagination,
        "products": [f"Product {i}" for i in range(pagination["skip"], pagination["skip"] + pagination["limit"])]
    }

print("✅ Pagination dependency created!")


async def get_async_data():
    """Async dependency - useful for async database operations"""
    print("⏳ Fetching data asynchronously...")
    await asyncio.sleep(0.1)  # Simulate async operation
    return {"data": "async_data", "timestamp": "2024-01-01"}

@app.get("/async-data/")
async def get_data(data: dict = Depends(get_async_data)):
    """Route using async dependency"""
    return {"result": data}

print("✅ Async dependency example created!")


# Example 3: Dependency with Parameters


def get_user_agent(user_agent: Optional[str] = Header(None)):
    """Dependency that extracts User-Agent header"""
    return user_agent or "Unknown"

@app.get("/user-info/")
def get_user_info(ua: str = Depends(get_user_agent)):
    """Route that uses User-Agent from header"""
    return {
        "user_agent": ua,
        "message": f"Request from: {ua}"
    }

print("✅ Dependency with header parameter created!")



# Using Dependencies in Routes

# There are multiple ways to use dependencies:

# 1. **As function parameters** (most common)
# 2. **As route decorator** (applies to all routes)
# 3. **As router dependencies** (applies to all routes in a router)


# Method 1: Dependency as Function Parameter (Most Common)

def get_settings():
    return {"app_name": "MyApp", "version": "1.0.0"}

@app.get("/info/")
def get_info(settings: dict = Depends(get_settings)):
    """Dependency injected as function parameter"""
    return {"info": settings}

print("✅ Method 1: Parameter injection")

# Method 2: Route-level Dependencies (Applies to all methods)

def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    """Verify API key from header"""
    if api_key != "secret-key-123":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return {"api_key": api_key, "verified": True}

# Apply dependency to all HTTP methods for this route
@app.api_route("/protected/", methods=["GET", "POST"], dependencies=[Depends(verify_api_key)])
def protected_route():
    """This route requires API key verification"""
    return {"message": "Access granted", "data": "sensitive information"}

print("✅ Method 2: Route-level dependencies")



# Method 3: Router-level Dependencies

def check_admin(role: str = Header(..., alias="X-User-Role")):
    """Check if user is admin"""
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"role": role, "access": "admin"}

# Create router with dependencies
admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(check_admin)]  # Applied to ALL routes in this router
)

@admin_router.get("/users/")
def list_users():
    """All routes in admin_router require admin role"""
    return {"users": ["user1", "user2"]}

@admin_router.get("/settings/")
def get_settings():
    """This route also requires admin role"""
    return {"settings": "admin_settings"}

app.include_router(admin_router)

print("✅ Method 3: Router-level dependencies")



# Example: Request Scope (Default Behavior)

# Counter to track how many times dependency is called
call_count = 0

def get_request_id():
    """This dependency is called ONCE per request"""
    global call_count
    call_count += 1
    request_id = f"req-{call_count}-{int(time.time() * 1000)}"
    print(f"🆔 Creating request ID: {request_id}")
    return request_id

@app.get("/request-scope/")
def get_data(request_id: str = Depends(get_request_id)):
    """Each request gets a new request_id"""
    return {
        "request_id": request_id,
        "message": "This dependency is created fresh for each request"
    }

print("✅ Request scope example (default behavior)")
print("💡 Each request will get a new request_id")





# Example: Caching Dependencies (Singleton-like behavior)


@lru_cache()  # Cache the result - only called once
def get_app_config():
    """This dependency is cached - only called once"""
    print("⚙️ Loading application configuration (only once!)")
    return {
        "app_name": "MyApp",
        "version": "1.0.0",
        "environment": "production",
        "database_url": "postgresql://localhost/db"
    }

@app.get("/config/")
def get_config(config: dict = Depends(get_app_config)):
    """Config is loaded once and cached"""
    return {"config": config}

@app.get("/config/check/")
def check_config(config: dict = Depends(get_app_config)):
    """Same cached config is reused"""
    return {"config": config, "cached": True}

print("✅ Cached dependency example")
print("💡 get_app_config() is only called once, then cached")