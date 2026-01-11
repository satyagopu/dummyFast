# Example: Basic GET Endpoints


from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse


app = FastAPI()

# Simple GET endpoint
@app.get("/")
def read_root():
    """Root endpoint - returns welcome message"""
    return {"message": "Welcome to FastAPI!"}

# GET endpoint returning a list
@app.get("/items")
def list_items():
    """List all items"""
    return {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }

# GET endpoint with type hints
@app.get("/users")
def get_users() -> dict:
    """Get all users with type hint"""
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }
# Path parameter with int type
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    Get item by ID
    
    - **item_id**: The ID of the item (must be an integer)
    """
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "type": type(item_id).__name__  # Shows it's an int
    }


# Path parameter with string type
@app.get("/users/{username}")
def get_user(username: str):
    """Get user by username"""
    return {
        "username": username,
        "message": f"User {username} found"
    }



# Multiple path parameters
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    """Get a specific post by a specific user"""
    return {
        "user_id": user_id,
        "post_id": post_id,
        "content": f"Post {post_id} by user {user_id}"
    }

# Path parameter with type validation
@app.get("/products/{product_id}")
def get_product(product_id: int):
    """
    Get product by ID
    
    FastAPI will:
    - Convert string from URL to int
    - Return 422 error if not a valid integer
    - Validate automatically
    """
    if product_id < 1:
        return {"error": "Product ID must be positive"}
    return {
        "product_id": product_id,
        "name": f"Product {product_id}",
        "price": 99.99
    }



# Required query parameter
@app.get("/search/")
def search(q: str):
    """
    Search endpoint with required query parameter
    
    Access: /search/?q=fastapi
    """
    return {
        "query": q,
        "results": [f"Result for '{q}'"]
    }

# Optional query parameters with defaults
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    """
    List items with pagination
    
    Access: /items/?skip=0&limit=10
    Access: /items/?skip=10&limit=20
    Access: /items/  (uses defaults: skip=0, limit=10)
    """
    return {
        "skip": skip,
        "limit": limit,
        "items": [f"Item {i}" for i in range(skip, skip + limit)]
    }

# Optional query parameter (can be None)
@app.get("/users/")
def list_users(
    active: Optional[bool] = None,
    role: Optional[str] = None
):
    """
    List users with optional filters
    
    Access: /users/
    Access: /users/?active=true
    Access: /users/?active=true&role=admin
    """
    filters = {}
    if active is not None:
        filters["active"] = active
    if role is not None:
        filters["role"] = role
    
    return {
        "filters": filters,
        "users": ["User 1", "User 2"]
    }



# Multiple query parameters
@app.get("/products/")
def list_products(
    category: str = "all",
    min_price: float = 0.0,
    max_price: Optional[float] = None,
    sort_by: str = "name",
    order: str = "asc"
):
    """
    List products with multiple query parameters
    
    Access: /products/?category=electronics&min_price=100&max_price=500&sort_by=price&order=desc
    """
    return {
        "category": category,
        "price_range": {
            "min": min_price,
            "max": max_price or "unlimited"
        },
        "sort": {
            "by": sort_by,
            "order": order
        },
        "products": ["Product 1", "Product 2"]
    }

# Boolean query parameters
@app.get("/posts/")
def list_posts(published: bool = True, featured: bool = False):
    """
    Boolean query parameters
    
    Access: /posts/?published=true&featured=false
    Access: /posts/?published=1&featured=0  (also works)
    """
    return {
        "published": published,
        "featured": featured,
        "posts": ["Post 1", "Post 2"]
    }





# Path parameter + Query parameters
@app.get("/users/{user_id}/posts")
def get_user_posts(
    user_id: int,           # Path parameter (required)
    skip: int = 0,          # Query parameter (optional)
    limit: int = 10         # Query parameter (optional)
):
    """
    Get posts by user with pagination
    
    Access: /users/123/posts
    Access: /users/123/posts?skip=10&limit=20
    """
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit,
        "posts": [f"Post {i} by user {user_id}" for i in range(skip, skip + limit)]
    }

# Multiple path params + query params
@app.get("/users/{user_id}/posts/{post_id}/comments")
def get_post_comments(
    user_id: int,           # Path parameter
    post_id: int,           # Path parameter
    page: int = 1,          # Query parameter
    per_page: int = 10      # Query parameter
):
    """
    Get comments for a specific post
    
    Access: /users/123/posts/456/comments?page=1&per_page=20
    """
    return {
        "user_id": user_id,
        "post_id": post_id,
        "page": page,
        "per_page": per_page,
        "comments": [f"Comment {i} on post {post_id}" for i in range(per_page)]
    }

# Path param with filtering query params
@app.get("/items/{item_id}")
def get_item(
    item_id: int,                    # Path parameter
    include_details: bool = False,   # Query parameter
    format: Optional[str] = None     # Query parameter
):
    """
    Get item with optional details
    
    Access: /items/123
    Access: /items/123?include_details=true
    Access: /items/123?include_details=true&format=json
    """
    item = {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "price": 99.99
    }
    
    if include_details:
        item["details"] = {
            "description": f"Description for item {item_id}",
            "stock": 100
        }
    
    if format:
        item["format"] = format
    
    return item



# Pydantic model for request body
class ItemCreate(BaseModel):
    """Model for creating an item"""
    name: str
    price: float
    description: Optional[str] = None


# Simple POST endpoint
@app.post("/itemss/")
def create_item(item: ItemCreate):
    """
    Create a new item
    
    Request body (JSON):
    {
        "name": "Laptop",
        "price": 999.99,
        "description": "Gaming laptop"
    }
    """
    return {
        "message": "Item created",
        "item": item.dict(),
        "id": 123  # Simulated ID
    }



# POST with validation
class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

@app.post("/userss/")
def create_user(user: UserCreate):
    """
    Create a new user
    
    FastAPI automatically:
    - Validates required fields (name, email)
    - Converts types
    - Returns 422 if validation fails
    """
    return {
        "message": "User created",
        "user": user.dict(),
        "id": 456
    }

# POST with nested models
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserWithAddress(BaseModel):
    name: str
    email: str
    address: Address

@app.post("/users/with-address/")
def create_user_with_address(user: UserWithAddress):
    """Create user with nested address"""
    return {
        "message": "User with address created",
        "user": user.dict()
    }

# POST with list of items
@app.post("/items/bulk/")
def create_items(items: List[ItemCreate]):
    """
    Create multiple items at once
    
    Request body:
    [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0}
    ]
    """
    return {
        "message": f"Created {len(items)} items",
        "items": [item.dict() for item in items]
    }



# Example: Return Types and Responses


# Pydantic models
class Item(BaseModel):
    id: int
    name: str
    price: float

class ItemResponse(BaseModel):
    """Response model"""
    id: int
    name: str
    price: float
    in_stock: bool = True

# Example 1: Simple dict return
@app.get("/simple/")
def simple_response() -> dict:
    """Returns a simple dictionary"""
    return {"message": "Hello", "status": "ok"}

# Example 2: Return Pydantic model
@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int) -> ItemResponse:
    """
    Get item with response model
    
    response_model ensures:
    - Only specified fields are returned
    - Types are validated
    - API docs show correct schema
    """
    return ItemResponse(
        id=item_id,
        name=f"Item {item_id}",
        price=99.99,
        in_stock=True
    )

# Example 3: Return list with response_model
@app.get("/items/", response_model=List[ItemResponse])
def list_items() -> List[ItemResponse]:
    """List all items"""
    return [
        ItemResponse(id=1, name="Item 1", price=10.0),
        ItemResponse(id=2, name="Item 2", price=20.0)
    ]

# Example 4: Custom status code
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> Item:
    """
    Create item with custom status code
    
    Returns 201 Created instead of default 200 OK
    """
    return item

# Example 5: JSONResponse for full control
@app.post("/items/custom/")
def create_item_custom(item: Item):
    """
    Create item with custom response
    
    Full control over status code and headers
    """
    return JSONResponse(
        status_code=201,
        content={
            "message": "Item created successfully",
            "item": item.dict(),
            "location": f"/items/{item.id}"
        },
        headers={"X-Custom-Header": "custom-value"}
    )

# Example 6: Response with headers
@app.get("/items/{item_id}/download")
def download_item(item_id: int):
    """
    Download item (example with custom headers)
    """
    return Response(
        content=f"Item {item_id} data",
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename=item_{item_id}.txt"
        }
    )
