"""
Dashboard-related API routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from services.db_manager import DatabaseManager

router = APIRouter()
db_manager = DatabaseManager()

@router.get("/stats")
async def get_dashboard_stats():
    """
    Get dashboard statistics
    """
    try:
        stats = await db_manager.get_application_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard stats: {str(e)}")

@router.get("/recent-applications")
async def get_recent_applications(limit: int = 5):
    """
    Get recent applications
    """
    try:
        applications = await db_manager.get_recent_applications(limit)
        return applications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve recent applications: {str(e)}")

@router.get("/skills-analysis")
async def get_skills_analysis():
    """
    Get skills analysis
    """
    try:
        analysis = await db_manager.get_skills_analysis()
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve skills analysis: {str(e)}")

@router.get("/job-trends")
async def get_job_trends():
    """
    Get job trends
    """
    try:
        trends = await db_manager.get_job_trends()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve job trends: {str(e)}")

@router.get("/pending-actions")
async def get_pending_actions():
    """
    Get pending actions that require user attention
    """
    try:
        actions = await db_manager.get_pending_actions()
        return actions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve pending actions: {str(e)}")
