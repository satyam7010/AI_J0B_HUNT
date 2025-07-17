"""
Resume parser service
Extracts structured information from resumes
"""

import os
import re
from typing import Dict, Any, List, Optional
from fastapi import UploadFile
import json
from datetime import datetime

from ..utils.file_utils import save_upload_file_temp, extract_text_from_file
from ..utils.logger import setup_logger
from ..config.settings import settings

logger = setup_logger(__name__)

class ResumeParser:
    """Resume parsing service"""
    
    def __init__(self):
        """Initialize resume parser"""
        self.logger = logger
    
    async def parse_resume_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Parse a resume file uploaded via FastAPI
        
        Args:
            file: The uploaded resume file
            
        Returns:
            Dict: Structured resume data
        """
        try:
            # Save uploaded file temporarily
            temp_file_path = await save_upload_file_temp(file)
            
            # Parse the resume
            parsed_data = self.parse_resume(temp_file_path)
            
            # Clean up temporary file
            os.remove(temp_file_path)
            
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error parsing resume file: {str(e)}")
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a resume file and extract structured data
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Dict: Structured resume data
        """
        try:
            # Extract text from file (PDF, DOCX, TXT)
            text = extract_text_from_file(file_path)
            
            # Extract information using AI (call to LLM happens here)
            # For now, we'll use a simple rule-based approach
            parsed_data = self._extract_information(text)
            
            self.logger.info(f"Resume parsed successfully: {parsed_data.get('name', 'Unknown')}")
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error parsing resume: {str(e)}")
            raise
    
    def _extract_information(self, text: str) -> Dict[str, Any]:
        """
        Extract structured information from resume text
        
        Args:
            text: The resume text content
            
        Returns:
            Dict: Structured resume data
        """
        # This is a simplified version - in production, use LLM or more sophisticated NLP
        
        # Basic information extraction
        name = self._extract_name(text)
        contact = self._extract_contact_info(text)
        skills = self._extract_skills(text)
        experience = self._extract_experience(text)
        education = self._extract_education(text)
        
        return {
            "name": name,
            "contact": contact,
            "skills": skills,
            "experience": experience,
            "education": education,
            "summary": self._extract_summary(text),
            "projects": self._extract_projects(text),
            "certifications": self._extract_certifications(text)
        }
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text"""
        # Simple heuristic: first line is often the name
        lines = text.strip().split('\n')
        if lines:
            name = lines[0].strip()
            # Check if it looks like a name (no special chars, not too long)
            if len(name) < 40 and re.match(r'^[A-Za-z\s\.\-]+$', name):
                return name
        
        # Fallback: look for common name patterns
        name_match = re.search(r'^([A-Z][a-z]+\s[A-Z][a-z]+)', text)
        if name_match:
            return name_match.group(1)
            
        return "Unknown"
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information"""
        contact = {
            "email": None,
            "phone": None,
            "location": None,
            "linkedin": None
        }
        
        # Email extraction
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            contact["email"] = email_match.group(0)
        
        # Phone extraction
        phone_match = re.search(r'(\+\d{1,3}[-\.\s]?)?(\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4})', text)
        if phone_match:
            contact["phone"] = phone_match.group(0)
        
        # LinkedIn extraction
        linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact["linkedin"] = "https://" + linkedin_match.group(0)
        
        # Location extraction (simplified)
        location_patterns = [
            r'([A-Z][a-z]+,\s[A-Z]{2})',  # City, State
            r'([A-Z][a-z]+,\s[A-Z][a-z]+)'  # City, Country
        ]
        
        for pattern in location_patterns:
            location_match = re.search(pattern, text)
            if location_match:
                contact["location"] = location_match.group(0)
                break
        
        return contact
    
    def _extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills from resume text"""
        skills = []
        
        # Look for a skills section
        skills_section_match = re.search(r'SKILLS[:\s]+(.*?)(?:\n\n|\Z)', text, re.IGNORECASE | re.DOTALL)
        
        if skills_section_match:
            skills_text = skills_section_match.group(1)
            # Split by commas, or bullet points
            skill_items = re.split(r'[,•]', skills_text)
            
            for item in skill_items:
                item = item.strip()
                if item and len(item) > 2:  # Avoid empty or too short items
                    skills.append({"name": item, "category": "technical"})
        
        # If no skills found, try to extract from whole text
        if not skills:
            # Common programming languages and technologies
            tech_keywords = [
                "Python", "Java", "JavaScript", "C\\+\\+", "C#", "Ruby", "PHP", "Swift",
                "HTML", "CSS", "SQL", "React", "Angular", "Vue", "Node.js", "Django",
                "Flask", "Spring", "AWS", "Azure", "Docker", "Kubernetes", "Git",
                "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn"
            ]
            
            for keyword in tech_keywords:
                if re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE):
                    skills.append({"name": keyword, "category": "technical"})
        
        return skills
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience"""
        experience = []
        
        # Look for experience section
        experience_section_match = re.search(
            r'(?:EXPERIENCE|EMPLOYMENT|WORK\sEXPERIENCE)[:\s]+(.*?)(?:EDUCATION|SKILLS|PROJECTS|\Z)', 
            text, 
            re.IGNORECASE | re.DOTALL
        )
        
        if experience_section_match:
            experience_text = experience_section_match.group(1)
            
            # Split into individual positions (simplified approach)
            positions = re.split(r'\n\n+', experience_text)
            
            for position in positions:
                if not position.strip():
                    continue
                    
                # Extract title and company
                title_company_match = re.search(r'(.*?)\s*\|\s*(.*?)\s*\|', position)
                
                if title_company_match:
                    title = title_company_match.group(1).strip()
                    company = title_company_match.group(2).strip()
                    
                    # Extract dates
                    dates_match = re.search(r'\|\s*(.*?)(?:\n|$)', position)
                    dates = dates_match.group(1).strip() if dates_match else ""
                    
                    start_date = ""
                    end_date = ""
                    
                    if " - " in dates:
                        date_parts = dates.split(" - ")
                        start_date = date_parts[0].strip()
                        end_date = date_parts[1].strip()
                    else:
                        start_date = dates
                    
                    # Extract description bullets
                    description_lines = []
                    for line in position.split('\n'):
                        if line.strip().startswith('•'):
                            description_lines.append(line.strip()[1:].strip())
                    
                    experience.append({
                        "title": title,
                        "company": company,
                        "start_date": start_date,
                        "end_date": end_date if end_date != "Present" else None,
                        "description": description_lines
                    })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        education = []
        
        # Look for education section
        education_section_match = re.search(
            r'EDUCATION[:\s]+(.*?)(?:EXPERIENCE|SKILLS|PROJECTS|\Z)', 
            text, 
            re.IGNORECASE | re.DOTALL
        )
        
        if education_section_match:
            education_text = education_section_match.group(1)
            
            # Split into individual education entries
            entries = re.split(r'\n\n+', education_text)
            
            for entry in entries:
                if not entry.strip():
                    continue
                
                # Extract degree and institution
                degree_match = re.search(r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|M\.A\.|B\.A\.|Doctorate).*?([^\|]+)', entry, re.IGNORECASE)
                
                if degree_match:
                    degree = degree_match.group(0).strip()
                    
                    # Extract institution
                    institution_match = re.search(r'\|\s*(.*?)\s*\|', entry)
                    institution = institution_match.group(1).strip() if institution_match else ""
                    
                    # Extract graduation date
                    grad_date_match = re.search(r'(?:Graduated|Graduation):\s*(\w+\s+\d{4})', entry, re.IGNORECASE)
                    grad_date = grad_date_match.group(1) if grad_date_match else ""
                    
                    if not grad_date:
                        # Try another pattern
                        date_match = re.search(r'\|\s*(\d{4})', entry)
                        grad_date = date_match.group(1) if date_match else ""
                    
                    education.append({
                        "degree": degree,
                        "institution": institution,
                        "graduation_date": grad_date
                    })
        
        return education
    
    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract summary/objective section"""
        summary_patterns = [
            r'(?:SUMMARY|PROFESSIONAL\sSUMMARY|OBJECTIVE)[:\s]+(.*?)(?:\n\n|\Z)',
            r'(?:PROFILE|ABOUT\sME)[:\s]+(.*?)(?:\n\n|\Z)'
        ]
        
        for pattern in summary_patterns:
            summary_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if summary_match:
                return summary_match.group(1).strip()
        
        return None
    
    def _extract_projects(self, text: str) -> List[Dict[str, Any]]:
        """Extract projects information"""
        projects = []
        
        # Look for projects section
        projects_section_match = re.search(
            r'PROJECTS[:\s]+(.*?)(?:EDUCATION|EXPERIENCE|SKILLS|\Z)', 
            text, 
            re.IGNORECASE | re.DOTALL
        )
        
        if projects_section_match:
            projects_text = projects_section_match.group(1)
            
            # Split into individual projects
            project_entries = re.split(r'\n\n+', projects_text)
            
            for entry in project_entries:
                if not entry.strip():
                    continue
                
                # Extract project name
                name_match = re.search(r'^(.*?)(?:\||\n|$)', entry)
                if name_match:
                    name = name_match.group(1).strip()
                    
                    # Extract description
                    lines = entry.split('\n')
                    description = ""
                    
                    # Skip the first line (name) and compile description
                    for line in lines[1:]:
                        if line.strip() and not line.strip().startswith('•'):
                            description += line.strip() + " "
                    
                    # Extract technologies
                    tech_match = re.search(r'Technologies:?\s*(.*?)(?:\n|$)', entry, re.IGNORECASE)
                    technologies = []
                    
                    if tech_match:
                        tech_text = tech_match.group(1)
                        technologies = [t.strip() for t in tech_text.split(',')]
                    
                    projects.append({
                        "name": name,
                        "description": description.strip(),
                        "technologies": technologies
                    })
        
        return projects
    
    def _extract_certifications(self, text: str) -> List[Dict[str, Any]]:
        """Extract certifications information"""
        certifications = []
        
        # Look for certifications section
        cert_section_match = re.search(
            r'(?:CERTIFICATIONS|CERTIFICATES)[:\s]+(.*?)(?:EDUCATION|EXPERIENCE|SKILLS|PROJECTS|\Z)', 
            text, 
            re.IGNORECASE | re.DOTALL
        )
        
        if cert_section_match:
            cert_text = cert_section_match.group(1)
            
            # Split into individual certifications
            cert_entries = re.split(r'\n+', cert_text)
            
            for entry in cert_entries:
                if not entry.strip():
                    continue
                
                # Look for certification name and issuer
                cert_match = re.search(r'(.*?)(?:\s*\|\s*(.*?))?(?:\s*\|\s*(.*?))?$', entry)
                
                if cert_match:
                    name = cert_match.group(1).strip()
                    issuer = cert_match.group(2).strip() if cert_match.group(2) else None
                    date = cert_match.group(3).strip() if cert_match.group(3) else None
                    
                    certifications.append({
                        "name": name,
                        "issuer": issuer,
                        "date": date
                    })
        
        return certifications
    
    async def get_all_resumes(self) -> List[Dict[str, Any]]:
        """
        Get all resumes from the database
        
        Returns:
            List[Dict]: List of resumes
        """
        # This would typically involve a database call
        # For now, return a mock response
        return [{
            "id": 1,
            "name": "John Doe",
            "contact": {
                "email": "john.doe@example.com",
                "phone": "555-123-4567",
                "location": "San Francisco, CA",
                "linkedin": "https://linkedin.com/in/johndoe"
            },
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }]
    
    async def get_resume(self, resume_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific resume by ID
        
        Args:
            resume_id: ID of the resume to retrieve
            
        Returns:
            Dict: Resume data or None if not found
        """
        # This would typically involve a database call
        # For now, return a mock response if ID is 1
        if resume_id == 1:
            return {
                "id": 1,
                "name": "John Doe",
                "contact": {
                    "email": "john.doe@example.com",
                    "phone": "555-123-4567",
                    "location": "San Francisco, CA",
                    "linkedin": "https://linkedin.com/in/johndoe"
                },
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        return None
