"""
Application-related data models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ApplicationBase(BaseModel):
    """Base application model"""
    job_id: int
    resume_id: int
    optimized_resume_id: Optional[int] = None
    cover_letter_id: Optional[int] = None
    status: str = "pending"  # pending, submitted, interview, rejected, offer, accepted
    notes: Optional[str] = None
    platform: Optional[str] = None  # linkedin, indeed, etc.
    platform_application_id: Optional[str] = None  # application ID on the platform

class ApplicationCreate(ApplicationBase):
    """Application creation model"""
    pass

class ApplicationResponse(ApplicationBase):
    """Application response model"""
    id: int
    created_at: datetime
    updated_at: datetime
    job: Dict[str, Any]  # Simplified job info
    resume: Dict[str, Any]  # Simplified resume info
    last_activity: Optional[datetime] = None
    next_action_date: Optional[datetime] = None
    next_action_type: Optional[str] = None  # follow-up, interview, etc.
    
    class Config:
        orm_mode = True

class ApplicationStatusUpdate(BaseModel):
    """Application status update model"""
    status: str
    notes: Optional[str] = None
    next_action_date: Optional[datetime] = None
    next_action_type: Optional[str] = None

class ApplicationActivity(BaseModel):
    """Application activity model"""
    id: int
    application_id: int
    activity_type: str  # status_change, note_added, follow_up, etc.
    timestamp: datetime
    details: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True

class CoverLetterRequest(BaseModel):
    """Cover letter generation request model"""
    resume_id: int
    job_id: int
    style: Optional[str] = "professional"  # professional, creative, technical, etc.
    
class CoverLetterResponse(BaseModel):
    """Cover letter response model"""
    id: int
    content: str
    created_at: datetime
