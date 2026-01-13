# Quick Start Guide

## Phase 1 Implementation Complete ✅

All Phase 1 components have been implemented. Here's how to get started:

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the `backend` directory with the following content:

```env
# Application Settings
APP_NAME=FastAPI E-Commerce Backend
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Server Settings
HOST=0.0.0.0
PORT=8000

# Database Settings (SQLite)
DATABASE_URL=sqlite:///./ecommerce.db

# Security Settings (for future use)
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
ALLOWED_METHODS=GET,POST,PUT,DELETE,PATCH
ALLOWED_HEADERS=*
```

### 3. Run the Application

**Option 1: Using the run script**
```bash
python run.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload
```

**Option 3: Using Python module**
```bash
python -m app.main
```

### 4. Test the API

Once the server is running:

1. **Health Check**: http://localhost:8000/api/v1/health
2. **Detailed Health**: http://localhost:8000/api/v1/health/detailed
3. **API Docs**: http://localhost:8000/docs
4. **ReDoc**: http://localhost:8000/redoc

## ✅ What's Implemented

### Phase 1.1: Project Initialization ✅
- [x] Project structure created
- [x] `requirements.txt` with dependencies
- [x] `.gitignore` configured
- [x] `app/__init__.py` created
- [x] `app/main.py` with FastAPI app
- [x] `app/config.py` for configuration

### Phase 1.2: Basic Routes & Health Check ✅
- [x] `app/routes/__init__.py` created
- [x] `app/routes/api.py` (main router)
- [x] `app/routes/health.py` (health endpoints)
- [x] Health check endpoint: `GET /api/v1/health`
- [x] Detailed health endpoint: `GET /api/v1/health/detailed`
- [x] API documentation accessible at `/docs`

### Phase 1.3: Error Handling Setup ✅
- [x] `app/utils/exceptions.py` with custom exceptions
- [x] `app/utils/responses.py` for standardized responses
- [x] `app/middleware/error_middleware.py` for global error handling
- [x] Exception handlers registered in `main.py`

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              ✅ FastAPI app with CORS, error handlers
│   ├── config.py            ✅ Configuration management
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py          ✅ Main API router
│   │   └── health.py       ✅ Health check endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_middleware.py  ✅ Global error handling
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py   ✅ Custom exceptions
│       └── responses.py     ✅ Standardized responses
├── requirements.txt         ✅ Dependencies
├── .gitignore              ✅ Git ignore rules
├── run.py                  ✅ Run script
├── README.md               ✅ Project documentation
└── QUICK_START.md          ✅ This file
```

## 🧪 Testing the API

### Using curl:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Detailed health check
curl http://localhost:8000/api/v1/health/detailed

# Root endpoint
curl http://localhost:8000/
```

### Expected Responses:

**Health Check:**
```json
{
  "success": true,
  "message": "Service is healthy",
  "status_code": 200,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00",
    "service": "FastAPI E-Commerce Backend",
    "version": "1.0.0",
    "environment": "development"
  }
}
```

## 🎯 Next Steps

Phase 1 is complete! Ready to move to **Phase 2: Database Setup**

The next phase will include:
- SQLAlchemy configuration
- Database connection setup
- Auto-table creation
- Session management

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for details.

---

**Status**: Phase 1 Complete ✅  
**Ready for**: Phase 2 - Database Setup
