"""
Resume-related API routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from typing import List, Optional

from models.resume import ResumeResponse, ResumeCreate
from services.resume_parser import ResumeParser
from agents.resume_optimizer_agent import ResumeOptimizerAgent

router = APIRouter()
resume_parser = ResumeParser()
resume_optimizer = ResumeOptimizerAgent()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    save_to_db: bool = Form(True)
):
    """
    Upload and parse a resume file
    """
    try:
        parsed_resume = await resume_parser.parse_resume_file(file)
        return parsed_resume
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing failed: {str(e)}")

@router.post("/optimize", response_model=str)
async def optimize_resume(
    resume_id: int,
    job_description: str
):
    """
    Optimize a resume for a specific job description
    """
    try:
        optimized_resume = await resume_optimizer.optimize(resume_id, job_description)
        return optimized_resume
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume optimization failed: {str(e)}")

@router.get("/", response_model=List[ResumeResponse])
async def get_resumes():
    """
    Get all resumes
    """
    try:
        resumes = await resume_parser.get_all_resumes()
        return resumes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve resumes: {str(e)}")

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int):
    """
    Get a specific resume by ID
    """
    try:
        resume = await resume_parser.get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve resume: {str(e)}")

@router.post("/latex", response_model=dict)
async def generate_latex_resume(
    resume_id: int,
    job_description: str,
    optimization_level: Optional[str] = "balanced"
):
    """
    Generate a LaTeX resume optimized for a specific job description
    """
    try:
        # Get the resume text from the database
        resume = await resume_parser.get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_text = resume_parser.resume_to_text(resume)
        
        # Generate LaTeX resume
        latex_sections = await resume_optimizer.generate_latex_resume(
            resume_text=resume_text,
            job_description=job_description,
            optimization_level=optimization_level
        )
        
        return {
            "message": "LaTeX resume generated successfully",
            "sections": latex_sections
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate LaTeX resume: {str(e)}")
