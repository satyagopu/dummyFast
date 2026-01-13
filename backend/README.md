# FastAPI E-Commerce Backend

A production-ready FastAPI backend for an e-commerce platform built with SQLite.

## 🚀 Features

- **FastAPI** - Modern, fast web framework
- **SQLite** - Lightweight database for development
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and settings management
- **JWT Authentication** - Secure token-based authentication
- **RBAC Authorization** - Role-based access control
- **Repository Pattern** - Clean architecture
- **Service Layer** - Business logic separation
- **Error Handling** - Global exception handling
- **API Documentation** - Auto-generated Swagger/ReDoc docs

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository** (if applicable)
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🏃 Running the Application

### Development Mode
```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection (Phase 2)
│   ├── models/              # SQLAlchemy models (Phase 3)
│   ├── schemas/             # Pydantic schemas (Phase 4)
│   ├── repositories/        # Repository pattern (Phase 4)
│   ├── services/            # Business logic (Phase 4)
│   ├── controllers/         # Route handlers (Phase 4)
│   ├── routes/              # Route definitions
│   ├── middleware/          # Custom middleware
│   ├── dependencies/        # FastAPI dependencies
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🔌 API Endpoints

### Health Check
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health check

### Authentication (Phase 5)
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout

### Users (Phase 4)
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Products (Phase 4)
- `GET /api/v1/products` - List products
- `GET /api/v1/products/{id}` - Get product by ID
- `POST /api/v1/products` - Create product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📝 Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT tokens
- `DEBUG` - Enable/disable debug mode
- `ALLOWED_ORIGINS` - CORS allowed origins

## 🗺️ Implementation Status

- [x] **Phase 1**: Basic API Setup ✅
- [ ] **Phase 2**: Database Setup
- [ ] **Phase 3**: Models & ORM
- [ ] **Phase 4**: Basic CRUD Operations
- [ ] **Phase 5**: Authentication
- [ ] **Phase 6**: Authorization
- [ ] **Phase 7**: Middleware
- [ ] **Phase 8**: Advanced Features
- [ ] **Phase 9**: Testing & Documentation

## 📖 Documentation

For detailed implementation plan, see [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)

## 🤝 Contributing

1. Follow the implementation plan phases
2. Write tests for new features
3. Update documentation
4. Follow PEP 8 style guide

## 📄 License

This project is for educational purposes.

---

**Current Phase**: Phase 1 Complete ✅
