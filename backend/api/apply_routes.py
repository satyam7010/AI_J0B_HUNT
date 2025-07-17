"""
Application-related API routes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from models.application import ApplicationResponse, ApplicationCreate, ApplicationStatusUpdate
from services.application_engine import ApplicationEngine

router = APIRouter()
application_engine = ApplicationEngine()

@router.post("/", response_model=ApplicationResponse)
async def create_application(application: ApplicationCreate):
    """
    Create a new application
    """
    try:
        created = await application_engine.create_application(application)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Application creation failed: {str(e)}")

@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get all applications with optional filtering
    """
    try:
        applications = await application_engine.get_applications(status, limit, offset)
        return applications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve applications: {str(e)}")

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: int):
    """
    Get a specific application by ID
    """
    try:
        application = await application_engine.get_application(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        return application
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve application: {str(e)}")

@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate
):
    """
    Update application status
    """
    try:
        updated = await application_engine.update_status(application_id, status_update.status)
        if not updated:
            raise HTTPException(status_code=404, detail="Application not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update application status: {str(e)}")

@router.post("/automated", response_model=List[ApplicationResponse])
async def run_automated_applications():
    """
    Run automated job application process
    """
    try:
        results = await application_engine.run_automation()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation failed: {str(e)}")
