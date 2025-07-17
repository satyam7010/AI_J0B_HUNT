"""
Resume-related data models
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class Skill(BaseModel):
    """Skill model"""
    name: str
    category: Optional[str] = None  # technical, soft, language
    level: Optional[str] = None     # beginner, intermediate, expert

class Education(BaseModel):
    """Education model"""
    degree: str
    institution: str
    location: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    relevant_courses: Optional[List[str]] = None

class Experience(BaseModel):
    """Work experience model"""
    title: str
    company: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    description: List[str]
    technologies: Optional[List[str]] = None

class Project(BaseModel):
    """Project model"""
    name: str
    description: str
    technologies: Optional[List[str]] = None
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Certification(BaseModel):
    """Certification model"""
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None
    expires: Optional[str] = None

class Contact(BaseModel):
    """Contact information model"""
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class ResumeBase(BaseModel):
    """Base resume model"""
    name: str
    contact: Contact
    summary: Optional[str] = None
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    projects: Optional[List[Project]] = None
    certifications: Optional[List[Certification]] = None

class ResumeCreate(ResumeBase):
    """Resume creation model"""
    pass

class ResumeResponse(ResumeBase):
    """Resume response model"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ResumeOptimizationRequest(BaseModel):
    """Resume optimization request model"""
    resume_id: int
    job_description: str
    preserve_contact_info: bool = True
    preserve_education: bool = True
    emphasis_recent_experience: bool = True

class ResumeOptimizationResponse(BaseModel):
    """Resume optimization response model"""
    original_resume_id: int
    optimized_resume: str
    match_score: float
    optimization_notes: List[str]
