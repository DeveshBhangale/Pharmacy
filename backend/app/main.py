from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import uvicorn
import logging
from typing import Dict, Any

from app.api.v1 import auth
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pharmacy Management System",
    description="Enterprise-level pharmacy management system with AI-powered features",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["authentication"]
)

# Error handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "pharmacy-management-system"
    }

# Import and include routers
# from app.api.v1 import auth, inventory, prescriptions, recommendations
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
# app.include_router(prescriptions.router, prefix="/api/v1/prescriptions", tags=["Prescriptions"])
# app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Pharmacy Management System API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 