# E-Commerce Database Design for FastAPI Learning

> Comprehensive database schema covering SQLAlchemy ORM, Database Patterns, NoSQL, Authentication, Authorization, and Redis Caching

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [SQL Schema (SQLite)](#sql-schema-sqlite)
4. [MongoDB Schema](#mongodb-schema)
5. [Redis Caching Strategy](#redis-caching-strategy)
6. [Learning Coverage](#learning-coverage)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Overview

This database design supports learning:
- **Section 6.1**: SQLAlchemy ORM (models, relationships, CRUD, migrations, connection pooling)
- **Section 6.2**: Database Patterns (Repository, Unit of Work, session management, transactions)
- **Section 6.3**: NoSQL Databases (MongoDB with Motor, Redis caching)
- **Section 7**: Authentication & Authorization (JWT, OAuth2, RBAC)
- **Section 15**: Caching Strategies (Redis)

**Use Case**: E-Commerce Platform
- **SQL Database**: SQLite (for development)
- **NoSQL Database**: MongoDB Atlas (for production scenarios)
- **Cache**: Redis

---

## Design Principles

1. **Simplicity First**: Minimal tables that cover all learning objectives
2. **Extensibility**: Easy to add features later (reviews, addresses, etc.)
3. **Real-World**: Practical e-commerce scenarios
4. **Learning-Focused**: Each entity teaches specific concepts
5. **Dual Support**: Works for both SQL and NoSQL approaches

---

## SQL Schema (SQLite)

### Core Tables

#### 1. Users Table
**Purpose**: User management, authentication, and authorization base

```sql
users
├── id (PK, Integer, Auto-increment)
├── email (String, Unique, Indexed, Not Null)
├── username (String, Unique, Indexed, Not Null)
├── password_hash (String, Not Null)
├── full_name (String, Nullable)
├── role (String, Default: 'customer') -- 'customer', 'admin', 'vendor'
├── is_active (Boolean, Default: True)
├── is_verified (Boolean, Default: False) -- Email verification
├── verification_token (String, Nullable)
├── verification_token_expires (DateTime, Nullable)
├── password_reset_token (String, Nullable)
├── password_reset_expires (DateTime, Nullable)
├── last_login (DateTime, Nullable)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Default: Now)
```

**Learning Points**:
- Authentication fields (password_hash, tokens)
- Authorization base (role field)
- Email verification workflow
- Password reset workflow

---

#### 2. Refresh Tokens Table
**Purpose**: JWT refresh token management for authentication

```sql
refresh_tokens
├── id (PK, Integer, Auto-increment)
├── user_id (FK → users.id, Not Null, Indexed)
├── token (String, Unique, Indexed, Not Null)
├── expires_at (DateTime, Not Null)
├── is_revoked (Boolean, Default: False)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Default: Now)
```

**Learning Points**:
- Token storage and management
- Token expiration handling
- Token revocation
- One-to-many relationship (User → Tokens)

---

#### 3. Roles Table
**Purpose**: Role definitions for authorization

```sql
roles
├── id (PK, Integer, Auto-increment)
├── name (String, Unique, Not Null) -- 'admin', 'customer', 'vendor', 'moderator'
├── description (String, Nullable)
└── created_at (DateTime, Default: Now)
```

**Learning Points**:
- Role-based access control (RBAC)
- Flexible role system

---

#### 4. Permissions Table
**Purpose**: Permission definitions for fine-grained authorization

```sql
permissions
├── id (PK, Integer, Auto-increment)
├── name (String, Unique, Not Null) -- 'create_product', 'delete_order', 'view_analytics'
├── resource (String, Not Null) -- 'product', 'order', 'user', 'category'
├── action (String, Not Null) -- 'create', 'read', 'update', 'delete'
└── created_at (DateTime, Default: Now)
```

**Learning Points**:
- Permission-based access control
- Resource-action mapping

---

#### 5. Role Permissions Table
**Purpose**: Many-to-many relationship between roles and permissions

```sql
role_permissions
├── id (PK, Integer, Auto-increment)
├── role_id (FK → roles.id, Not Null, Indexed)
├── permission_id (FK → permissions.id, Not Null, Indexed)
└── created_at (DateTime, Default: Now)
```

**Learning Points**:
- Many-to-many relationships
- RBAC implementation
- Composite primary key consideration

---

#### 6. Categories Table
**Purpose**: Product categorization with hierarchy support

```sql
categories
├── id (PK, Integer, Auto-increment)
├── name (String, Not Null)
├── slug (String, Unique, Indexed, Not Null)
├── description (String, Nullable)
├── parent_id (FK → categories.id, Nullable) -- For hierarchy
├── is_active (Boolean, Default: True)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Default: Now)
```

**Learning Points**:
- Self-referential relationships (hierarchy)
- Slug for SEO-friendly URLs
- One-to-many relationship (Category → Products)

---

#### 7. Products Table
**Purpose**: Product catalog management

```sql
products
├── id (PK, Integer, Auto-increment)
├── name (String, Not Null)
├── slug (String, Unique, Indexed, Not Null)
├── description (Text, Nullable)
├── category_id (FK → categories.id, Not Null, Indexed)
├── price (Decimal(10, 2), Not Null)
├── stock_quantity (Integer, Default: 0)
├── is_active (Boolean, Default: True)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Default: Now)
```

**Learning Points**:
- Foreign key relationships
- Decimal for currency
- Indexing for performance
- Many-to-one relationship (Products → Category)

---

#### 8. Orders Table
**Purpose**: Order management and transaction handling

```sql
orders
├── id (PK, Integer, Auto-increment)
├── order_number (String, Unique, Indexed, Not Null) -- Human-readable: ORD-2024-001
├── user_id (FK → users.id, Nullable, Indexed) -- Nullable for guest orders
├── status (String, Default: 'pending') -- 'pending', 'processing', 'shipped', 'delivered', 'cancelled'
├── total_amount (Decimal(10, 2), Not Null)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Default: Now)
```

**Learning Points**:
- Transaction management
- Status workflow
- Nullable foreign keys (guest orders)
- One-to-many relationship (Order → Order Items)

---

#### 9. Order Items Table
**Purpose**: Order line items with price snapshots

```sql
order_items
├── id (PK, Integer, Auto-increment)
├── order_id (FK → orders.id, Not Null, Indexed)
├── product_id (FK → products.id, Not Null, Indexed)
├── quantity (Integer, Not Null)
├── price (Decimal(10, 2), Not Null) -- Snapshot of price at order time
├── created_at (DateTime, Default: Now)
└── UNIQUE(order_id, product_id) -- Prevent duplicate products in same order
```

**Learning Points**:
- Price snapshot (immutable order data)
- Composite unique constraint
- Many-to-one relationships (Order Items → Order, Order Items → Product)

---

#### 10. Cart Items Table
**Purpose**: Shopping cart management

```sql
cart_items
├── id (PK, Integer, Auto-increment)
├── user_id (FK → users.id, Nullable, Indexed) -- Nullable for guest carts
├── session_id (String, Nullable, Indexed) -- For guest users
├── product_id (FK → products.id, Not Null, Indexed)
├── quantity (Integer, Not Null, Default: 1)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Default: Now)
```

**Learning Points**:
- Session management
- Guest vs authenticated users
- Many-to-one relationship (Cart Items → User, Cart Items → Product)

---

### Database Relationships Diagram

```
users (1) ──→ (M) refresh_tokens
users (1) ──→ (M) orders
users (1) ──→ (M) cart_items

categories (1) ──→ (M) products
categories (1) ──→ (M) categories (self-referential: parent_id)

products (1) ──→ (M) order_items
products (1) ──→ (M) cart_items

orders (1) ──→ (M) order_items

roles (1) ──→ (M) role_permissions
permissions (1) ──→ (M) role_permissions
```

---

## MongoDB Schema

### Document Structure Approach

#### 1. Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique, indexed),
  username: String (unique, indexed),
  password_hash: String,
  full_name: String,
  role: String, // "customer" | "admin" | "vendor"
  is_active: Boolean,
  is_verified: Boolean,
  verification_token: String (nullable),
  verification_token_expires: ISODate (nullable),
  password_reset_token: String (nullable),
  password_reset_expires: ISODate (nullable),
  last_login: ISODate (nullable),
  created_at: ISODate,
  updated_at: ISODate
}
```

#### 2. Refresh Tokens Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (indexed), // Reference to users
  token: String (unique, indexed),
  expires_at: ISODate,
  is_revoked: Boolean,
  created_at: ISODate,
  updated_at: ISODate
}
```

#### 3. Roles Collection
```javascript
{
  _id: ObjectId,
  name: String (unique), // "admin", "customer", "vendor"
  description: String,
  permissions: [ObjectId], // Array of permission references
  created_at: ISODate
}
```

#### 4. Permissions Collection
```javascript
{
  _id: ObjectId,
  name: String (unique), // "create_product", "delete_order"
  resource: String, // "product", "order", "user"
  action: String, // "create", "read", "update", "delete"
  created_at: ISODate
}
```

#### 5. Categories Collection
```javascript
{
  _id: ObjectId,
  name: String,
  slug: String (unique, indexed),
  description: String,
  parent_id: ObjectId (nullable), // Self-reference for hierarchy
  is_active: Boolean,
  created_at: ISODate,
  updated_at: ISODate
}
```

#### 6. Products Collection
```javascript
{
  _id: ObjectId,
  name: String,
  slug: String (unique, indexed),
  description: String,
  category: {
    _id: ObjectId, // Reference to categories
    name: String, // Denormalized for quick access
    slug: String
  },
  price: Decimal,
  stock_quantity: Integer,
  is_active: Boolean,
  created_at: ISODate,
  updated_at: ISODate
}
```

#### 7. Orders Collection (with embedded items)
```javascript
{
  _id: ObjectId,
  order_number: String (unique, indexed),
  user_id: ObjectId (nullable), // Reference to users
  status: String, // "pending" | "processing" | "shipped" | "delivered" | "cancelled"
  items: [ // Embedded documents
    {
      product_id: ObjectId,
      product_name: String, // Snapshot
      quantity: Integer,
      price: Decimal // Snapshot
    }
  ],
  total_amount: Decimal,
  created_at: ISODate,
  updated_at: ISODate
}
```

#### 8. Cart Collection (with embedded items)
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (nullable), // Reference to users
  session_id: String (indexed), // For guest users
  items: [ // Embedded documents
    {
      product_id: ObjectId,
      quantity: Integer,
      added_at: ISODate
    }
  ],
  updated_at: ISODate,
  expires_at: ISODate // For cleanup
}
```

---

## Redis Caching Strategy

### Cache Keys Structure

#### 1. Product Catalog Caching
```
Key Pattern: product:{id}
Example: product:123
TTL: 1 hour
Invalidation: On product update/delete

Key Pattern: products:category:{category_id}
Example: products:category:5
TTL: 30 minutes
Invalidation: On product create/update/delete in category

Key Pattern: products:all
Example: products:all
TTL: 15 minutes
Invalidation: On any product change
```

#### 2. Category Caching
```
Key Pattern: category:{id}
Example: category:5
TTL: 24 hours (rarely changes)
Invalidation: On category update/delete

Key Pattern: categories:tree
Example: categories:tree
TTL: 24 hours
Invalidation: On category hierarchy change
```

#### 3. User Session Caching
```
Key Pattern: session:{session_id}
Example: session:abc123xyz
TTL: 30 minutes (extend on activity)
Invalidation: On logout or expiration

Key Pattern: user:{user_id}:session
Example: user:42:session
TTL: 30 minutes
Invalidation: On logout
```

#### 4. Shopping Cart Caching (Guest Users)
```
Key Pattern: cart:session:{session_id}
Example: cart:session:abc123xyz
TTL: 7 days
Invalidation: On cart clear or expiration
```

#### 5. Authentication Data Caching
```
Key Pattern: user:{user_id}:auth
Example: user:42:auth
TTL: 15 minutes
Invalidation: On user update, role change, or logout

Key Pattern: token:{refresh_token}
Example: token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
TTL: 7 days (matches refresh token expiration)
Invalidation: On token revocation or expiration
```

#### 6. Product Stock Caching
```
Key Pattern: product:{id}:stock
Example: product:123:stock
TTL: 5 minutes (frequently updated)
Invalidation: On order creation, stock update
```

#### 7. Order Status Caching
```
Key Pattern: order:{order_id}:status
Example: order:456:status
TTL: 10 minutes
Invalidation: On order status update
```

### Cache Invalidation Strategy

1. **Product Updates**: Invalidate `product:{id}`, `products:category:{category_id}`, `products:all`
2. **Order Creation**: Invalidate `product:{id}:stock` for all products in order
3. **User Updates**: Invalidate `user:{user_id}:auth`
4. **Category Changes**: Invalidate `category:{id}`, `categories:tree`, related `products:category:{category_id}`
5. **Token Revocation**: Delete `token:{refresh_token}`

---

## Learning Coverage

### Section 6.1: SQLAlchemy ORM

✅ **Setting up SQLAlchemy**
- Database connection setup
- Engine configuration
- Session management

✅ **Database Models**
- All 10 tables as SQLAlchemy models
- Type definitions
- Column constraints

✅ **Relationships**
- One-to-many: User → Orders, Category → Products, Order → Order Items
- Many-to-one: Products → Category, Order Items → Product/Order
- Many-to-many: Roles ↔ Permissions
- Self-referential: Categories hierarchy

✅ **CRUD Operations**
- Create: Users, Products, Orders
- Read: Querying with filters, joins
- Update: Product updates, order status changes
- Delete: Soft deletes with is_active flag

✅ **Database Migrations**
- Alembic setup
- Migration creation
- Schema versioning

✅ **Connection Pooling**
- SQLite connection management
- Pool configuration

---

### Section 6.2: Database Patterns

✅ **Repository Pattern**
- Repository interface for each entity
- Implementation for Users, Products, Orders, Categories
- Abstract base repository

✅ **Unit of Work Pattern**
- Order creation with multiple items
- Transaction management
- Rollback on errors

✅ **Database Session Management**
- Dependency injection for sessions
- Context managers
- Session lifecycle

✅ **Transaction Handling**
- Order creation (Order + Order Items)
- Stock deduction on order
- Atomic operations

---

### Section 6.3: NoSQL Databases

✅ **MongoDB with Motor (async)**
- Async database operations
- Document structure design
- Embedded vs referenced documents

✅ **Redis for Caching**
- Product catalog caching
- Session management
- Cache invalidation strategies

✅ **Choosing between SQL and NoSQL**
- When to use SQL (structured data, transactions)
- When to use NoSQL (flexible schema, read-heavy)
- Hybrid approach

---

### Section 7: Authentication & Authorization

✅ **JWT (JSON Web Tokens)**
- User data from `users` table
- Token creation and validation
- Refresh token management in `refresh_tokens` table
- Token expiration handling

✅ **OAuth2**
- User authentication flow
- Token storage
- Scope-based permissions

✅ **Security Best Practices**
- Password hashing (stored in `password_hash`)
- Token security
- Email verification workflow

✅ **Authorization**
- Role-based: `users.role` field
- Permission-based: `roles`, `permissions`, `role_permissions` tables
- Resource-level access control

---

### Section 15: Caching

✅ **Redis Caching**
- Product catalog caching
- User session caching
- Shopping cart caching
- Authentication data caching

✅ **Cache Invalidation**
- Strategies for different entities
- Event-driven invalidation
- TTL management

---

## Implementation Roadmap

### Phase 1: SQLAlchemy Basics (Week 1)
1. Setup SQLAlchemy with SQLite
2. Create core models: Users, Categories, Products
3. Implement basic CRUD operations
4. Add relationships (Product → Category)

**Deliverables**:
- Database connection setup
- 3 core models
- Basic CRUD endpoints

---

### Phase 2: Advanced SQLAlchemy (Week 2)
1. Create Orders and OrderItems models
2. Implement complex relationships
3. Setup Alembic for migrations
4. Add connection pooling

**Deliverables**:
- All 10 models
- Relationships configured
- Migration system working

---

### Phase 3: Database Patterns (Week 3)
1. Implement Repository pattern
2. Implement Unit of Work pattern
3. Dependency injection for sessions
4. Transaction handling

**Deliverables**:
- Repository classes for all entities
- Unit of Work implementation
- Transaction-safe operations

---

### Phase 4: Authentication (Week 4)
1. Add authentication fields to Users
2. Create RefreshTokens model
3. Implement JWT creation/validation
4. Password hashing and verification

**Deliverables**:
- Authentication endpoints
- Token management
- Password reset flow

---

### Phase 5: Authorization (Week 5)
1. Create Roles and Permissions models
2. Implement RBAC system
3. Permission checking middleware
4. Role-based route protection

**Deliverables**:
- RBAC system
- Permission-based access control
- Protected endpoints

---

### Phase 6: NoSQL & Caching (Week 6)
1. Setup MongoDB with Motor
2. Convert SQL models to MongoDB documents
3. Setup Redis
4. Implement caching strategies

**Deliverables**:
- MongoDB collections
- Redis caching implementation
- Cache invalidation logic

---

## Summary

### Tables/Collections Count
- **SQL Tables**: 10
- **MongoDB Collections**: 8
- **Redis Cache Keys**: 7 patterns

### Learning Topics Covered
- ✅ SQLAlchemy ORM (models, relationships, CRUD, migrations)
- ✅ Database Patterns (Repository, Unit of Work, transactions)
- ✅ NoSQL Databases (MongoDB, Redis)
- ✅ Authentication (JWT, tokens, password management)
- ✅ Authorization (RBAC, permissions)
- ✅ Caching Strategies (Redis, invalidation)

### Complexity Level
- **Simple**: Core structure is straightforward
- **Complete**: Covers all learning objectives
- **Extensible**: Easy to add features (reviews, addresses, etc.)

---

## Next Steps

1. Review and approve this design
2. Create SQLAlchemy models
3. Setup database connections
4. Implement CRUD operations
5. Add relationships
6. Setup migrations
7. Implement patterns
8. Add authentication
9. Add authorization
10. Implement caching

---

*Last Updated: 2024*
*This design supports the complete FastAPI learning roadmap*
