"""
Job Description Analysis Agent for AI Job Hunt system
"""

import logging
from typing import Dict, List, Any, Optional, Union
import asyncio

from ..config.settings import settings
from ..utils.logger import setup_logger
from ..services.llm_service import LLMService
from ..prompts.job_prompts import JOB_ANALYSIS_PROMPT

logger = setup_logger(__name__)

class JobDescriptionAnalysisAgent:
    """
    Agent responsible for analyzing job descriptions to extract key information,
    skills, requirements, and suitability for the candidate
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize the job description analysis agent
        
        Args:
            llm_service: LLM service to use (creates a new one if not provided)
        """
        self.llm_service = llm_service or LLMService()
        logger.info("Job Description Analysis Agent initialized")
    
    async def analyze_job_description(
        self, 
        job_description: str, 
        resume_text: Optional[str] = None,
        candidate_skills: Optional[List[str]] = None,
        desired_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a job description and evaluate suitability
        
        Args:
            job_description: Job description text to analyze
            resume_text: Candidate's resume text (optional)
            candidate_skills: List of candidate's skills (optional)
            desired_role: Candidate's desired role (optional)
            
        Returns:
            Dictionary containing analysis results
        """
        logger.info("Analyzing job description")
        
        # Prepare the prompt with all relevant information
        prompt_vars = {
            "job_description": job_description,
            "resume": resume_text or "",
            "candidate_skills": candidate_skills or [],
            "desired_role": desired_role or ""
        }
        
        # Generate the prompt
        prompt = JOB_ANALYSIS_PROMPT.format(**prompt_vars)
        
        try:
            # Get response from LLM
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                temperature=0.3,  # Lower temperature for more factual extraction
                max_tokens=settings.ollama.max_tokens
            )
            
            # Parse and structure the LLM response
            parsed_response = self._parse_analysis_response(llm_response)
            
            logger.info("Job description analysis completed successfully")
            return parsed_response
            
        except Exception as e:
            logger.error(f"Error analyzing job description: {str(e)}")
            raise
    
    def _parse_analysis_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse the LLM response into a structured format
        
        Args:
            llm_response: Raw response from the LLM
            
        Returns:
            Structured dictionary with job analysis data
        """
        # Default structure
        result = {
            "title": "",
            "company": "",
            "required_skills": [],
            "preferred_skills": [],
            "experience_level": "",
            "education_requirements": [],
            "job_responsibilities": [],
            "match_score": 0.0,
            "missing_skills": [],
            "matching_skills": [],
            "application_recommendations": "",
            "keywords": []
        }
        
        # Simple parsing based on section headers
        sections = llm_response.split("###")
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
                
            # Extract section title and content
            lines = section.split("\n", 1)
            if len(lines) < 2:
                continue
                
            title = lines[0].strip().lower()
            content = lines[1].strip()
            
            # Map to result structure
            if "job title" in title:
                result["title"] = content
            elif "company" in title:
                result["company"] = content
            elif "required skills" in title:
                result["required_skills"] = [
                    skill.strip() 
                    for skill in content.split("-") 
                    if skill.strip()
                ]
            elif "preferred skills" in title:
                result["preferred_skills"] = [
                    skill.strip() 
                    for skill in content.split("-") 
                    if skill.strip()
                ]
            elif "experience level" in title:
                result["experience_level"] = content
            elif "education" in title:
                result["education_requirements"] = [
                    edu.strip() 
                    for edu in content.split("-") 
                    if edu.strip()
                ]
            elif "responsibilities" in title:
                result["job_responsibilities"] = [
                    resp.strip() 
                    for resp in content.split("-") 
                    if resp.strip()
                ]
            elif "match score" in title:
                try:
                    # Extract just the number
                    import re
                    score_match = re.search(r'(\d+(\.\d+)?)', content)
                    if score_match:
                        result["match_score"] = float(score_match.group(1))
                except ValueError:
                    # If conversion fails, keep default
                    pass
            elif "missing skills" in title:
                result["missing_skills"] = [
                    skill.strip() 
                    for skill in content.split(",") 
                    if skill.strip()
                ]
            elif "matching skills" in title:
                result["matching_skills"] = [
                    skill.strip() 
                    for skill in content.split(",") 
                    if skill.strip()
                ]
            elif "recommendations" in title:
                result["application_recommendations"] = content
            elif "keywords" in title:
                result["keywords"] = [
                    keyword.strip() 
                    for keyword in content.split(",") 
                    if keyword.strip()
                ]
        
        return result
