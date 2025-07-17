"""
Job-related API routes
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from models.job import JobResponse, JobCreate, JobAnalysisResponse
from services.job_scraper import JobScraper
from agents.job_description_agent import JobDescriptionAnalysisAgent

router = APIRouter()
job_scraper = JobScraper()
job_analyzer = JobDescriptionAnalysisAgent()

@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(job_data: JobCreate):
    """
    Analyze a job description
    """
    try:
        analysis = await job_analyzer.analyze_job(job_data.description)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Job analysis failed: {str(e)}")

@router.get("/search", response_model=List[JobResponse])
async def search_jobs(
    keywords: Optional[str] = Query(None, description="Job keywords"),
    location: Optional[str] = Query(None, description="Job location"),
    experience_level: Optional[str] = Query(None, description="Experience level"),
    job_type: Optional[str] = Query(None, description="Job type"),
    limit: int = Query(10, description="Maximum number of results")
):
    """
    Search for jobs
    """
    try:
        jobs = await job_scraper.search_jobs(
            keywords=keywords,
            location=location,
            experience_level=experience_level,
            job_type=job_type,
            limit=limit
        )
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int):
    """
    Get a specific job by ID
    """
    try:
        job = await job_scraper.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve job: {str(e)}")

@router.post("/url", response_model=JobAnalysisResponse)
async def analyze_job_url(job_url: str):
    """
    Analyze a job from URL
    """
    try:
        job_details = await job_scraper.scrape_job_url(job_url)
        analysis = await job_analyzer.analyze_job(job_details.description)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Job URL analysis failed: {str(e)}")
