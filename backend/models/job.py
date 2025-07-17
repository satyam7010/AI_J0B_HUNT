"""
Job-related data models
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

class JobBase(BaseModel):
    """Base job model"""
    title: str
    company: str
    location: Optional[str] = None
    description: str
    url: Optional[HttpUrl] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None  # full-time, part-time, contract, etc.
    experience_level: Optional[str] = None  # entry, mid, senior, executive
    remote_status: Optional[str] = None  # remote, hybrid, on-site
    application_deadline: Optional[datetime] = None
    platform: Optional[str] = None  # linkedin, indeed, etc.

class JobCreate(BaseModel):
    """Job creation model"""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    url: Optional[HttpUrl] = None
    platform: Optional[str] = None

class JobResponse(JobBase):
    """Job response model"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class JobRequirement(BaseModel):
    """Job requirement model"""
    type: str  # education, experience, certification, etc.
    description: str
    essential: bool = True  # is this requirement essential or preferred

class JobAnalysisResponse(BaseModel):
    """Job analysis response model"""
    job_id: Optional[int] = None
    job_title: str
    company: Optional[str] = None
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    requirements: List[JobRequirement]
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    salary_range: Optional[str] = None
    benefits: Optional[List[str]] = None
    company_info: Optional[str] = None
    remote_status: Optional[str] = None
    key_technologies: List[str]
    application_process: Optional[str] = None

class JobSearchCriteria(BaseModel):
    """Job search criteria model"""
    job_titles: List[str]
    skills: List[str]
    locations: Optional[List[str]] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    exclude_companies: Optional[List[str]] = None
