# Example 1: Simple Function Dependency

from fastapi import FastAPI, Depends, Query
from typing import Optional

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