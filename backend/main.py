"""
AI Job Hunt - FastAPI Backend
Main application entry point
"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Import API routers
from backend.api.resume_routes import router as resume_router
from backend.api.job_routes import router as job_router
from backend.api.apply_routes import router as apply_router
from backend.api.dashboard_routes import router as dashboard_router

# Configure logging
from backend.utils.logger import setup_logger
logger = setup_logger()
logger = setup_logger()

# Create FastAPI app
app = FastAPI(
    title="AI Job Hunt API",
    description="API for AI-powered job application automation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(resume_router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(job_router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(apply_router, prefix="/api/applications", tags=["Applications"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "online", "service": "AI Job Hunt API"}

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "services": {
            "database": "connected",
            "ollama": "connected" if os.getenv("OLLAMA_API_URL") else "not configured"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
