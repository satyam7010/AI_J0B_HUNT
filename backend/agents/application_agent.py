"""
Application Agent for AI Job Hunt system
"""

import logging
from typing import Dict, List, Any, Optional, Union
import asyncio

from config.settings import settings
from utils.logger import setup_logger
from agents.resume_optimizer_agent import ResumeOptimizerAgent
from agents.job_description_agent import JobDescriptionAgent
from services.llm_service import LLMService
from services.db_manager import DatabaseManager

logger = setup_logger(__name__)

class ApplicationAgent:
    """
    Agent responsible for orchestrating the job application process,
    coordinating between job analysis, resume optimization, and application submission
    """
    
    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        db_manager: Optional[DatabaseManager] = None
    ):
        """
        Initialize the application agent
        
        Args:
            llm_service: LLM service to use
            db_manager: Database manager to use
        """
        self.llm_service = llm_service or LLMService()
        self.db_manager = db_manager or DatabaseManager()
        self.resume_optimizer = ResumeOptimizerAgent(llm_service=self.llm_service)
        self.job_analyzer = JobDescriptionAgent(llm_service=self.llm_service)
        logger.info("Application Agent initialized")
    
    async def process_job_opportunity(
        self,
        job_data: Dict[str, Any],
        resume_text: str,
        candidate_skills: Optional[List[str]] = None,
        auto_apply: bool = False,
        optimization_level: str = "balanced"
    ) -> Dict[str, Any]:
        """
        Process a job opportunity through analysis, matching, and resume optimization
        
        Args:
            job_data: Job posting data including description
            resume_text: Candidate's resume text
            candidate_skills: List of candidate's skills (optional)
            auto_apply: Whether to automatically apply
            optimization_level: Level of resume optimization
            
        Returns:
            Dictionary with processing results
        """
        result = {
            "job_id": job_data.get("id", ""),
            "title": job_data.get("title", ""),
            "company": job_data.get("company", ""),
            "analysis": None,
            "optimized_resume": None,
            "application_status": "pending",
            "match_score": 0.0,
            "application_submitted": False,
            "submission_result": None
        }
        
        try:
            # Step 1: Analyze the job description
            logger.info(f"Analyzing job: {result['title']} at {result['company']}")
            job_analysis = await self.job_analyzer.analyze_job_description(
                job_description=job_data.get("description", ""),
                resume_text=resume_text,
                candidate_skills=candidate_skills
            )
            
            result["analysis"] = job_analysis
            result["match_score"] = job_analysis.get("match_score", 0)
            
            # Step 2: Optimize the resume if match score is high enough
            if result["match_score"] >= settings.application.min_match_score:
                logger.info(f"Match score {result['match_score']} meets threshold, optimizing resume")
                
                optimization_result = await self.resume_optimizer.optimize_resume(
                    resume_text=resume_text,
                    job_description=job_data.get("description", ""),
                    job_requirements=job_analysis.get("required_skills", []),
                    company_info=job_data.get("company_info", ""),
                    optimization_level=optimization_level
                )
                
                result["optimized_resume"] = optimization_result
                
                # Step 3: Auto-apply if configured
                if auto_apply and settings.application.auto_apply_enabled:
                    result["application_status"] = "auto_applying"
                    # Auto-apply implementation would go here
                    # This is a placeholder for actual implementation
                    logger.info(f"Auto-applying to job: {result['title']} at {result['company']}")
                    
                    # Simulate application submission
                    result["application_submitted"] = True
                    result["application_status"] = "submitted"
                    result["submission_result"] = {
                        "success": True,
                        "submission_time": "2023-06-01T12:00:00",
                        "confirmation_id": "SAMPLE-12345"
                    }
                else:
                    # Mark for manual review
                    result["application_status"] = "ready_for_review"
            else:
                logger.info(f"Match score {result['match_score']} below threshold, skipping optimization")
                result["application_status"] = "low_match_score"
            
            # Save to database
            await self.db_manager.save_application_result(job_data, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing job opportunity: {str(e)}")
            result["application_status"] = "error"
            result["error_message"] = str(e)
            
            # Save failed attempt to database
            await self.db_manager.save_application_result(job_data, result)
            
            return result
    
    async def submit_application(
        self,
        application_id: str,
        resume_text: Optional[str] = None,
        cover_letter: Optional[str] = None,
        additional_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Submit a job application
        
        Args:
            application_id: ID of the application to submit
            resume_text: Optimized resume text (optional)
            cover_letter: Cover letter text (optional)
            additional_fields: Additional application fields (optional)
            
        Returns:
            Dictionary with submission results
        """
        logger.info(f"Submitting application {application_id}")
        
        try:
            # Get application data from database
            application_data = await self.db_manager.get_application(application_id)
            
            if not application_data:
                raise ValueError(f"Application {application_id} not found")
            
            # Update with latest resume and cover letter if provided
            if resume_text:
                application_data["optimized_resume"]["optimized_resume"] = resume_text
                
            if cover_letter:
                application_data["cover_letter"] = cover_letter
                
            if additional_fields:
                application_data["additional_fields"] = additional_fields
            
            # Application submission would go here
            # This is a placeholder for actual implementation
            
            # Update status
            application_data["application_status"] = "submitted"
            application_data["application_submitted"] = True
            application_data["submission_result"] = {
                "success": True,
                "submission_time": "2023-06-01T12:00:00",
                "confirmation_id": "SAMPLE-12345"
            }
            
            # Save updated status to database
            await self.db_manager.update_application(application_id, application_data)
            
            logger.info(f"Application {application_id} submitted successfully")
            return application_data
            
        except Exception as e:
            logger.error(f"Error submitting application {application_id}: {str(e)}")
            
            # Update status to failed
            await self.db_manager.update_application_status(
                application_id, 
                "submission_failed",
                error_message=str(e)
            )
            
            raise
