"""
Application Agent for AI Job Hunt system
"""

import logging
from typing import Dict, List, Any, Optional, Union
import asyncio

from ..config.settings import settings
from ..utils.logger import setup_logger
from .resume_optimizer_agent import ResumeOptimizerAgent
from .job_description_agent import JobDescriptionAnalysisAgent
from ..services.llm_service import LLMService
from ..services.db_manager import DatabaseManager

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
        self.job_analyzer = JobDescriptionAnalysisAgent(llm_service=self.llm_service)
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
                
                # Step 3: Save the processed job to the database
                self.db_manager.save_processed_job(
                    job_data=job_data,
                    analysis=job_analysis,
                    optimized_resume=optimization_result,
                    match_score=result["match_score"]
                )
                
                # Step 4: Automatically apply if enabled and score is high
                if (auto_apply and 
                    settings.application.auto_apply_enabled and 
                    result["match_score"] >= settings.application.auto_apply_threshold):
                    
                    # This would integrate with the job application service
                    # to actually submit applications, which is not implemented here
                    logger.info(f"Auto-apply criteria met for {result['title']} at {result['company']}")
                    result["application_status"] = "auto_submitted"
                    result["application_submitted"] = True
                    
            else:
                logger.info(f"Match score {result['match_score']} below threshold, skipping optimization")
                result["application_status"] = "rejected_low_match"
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing job opportunity: {str(e)}")
            result["application_status"] = "error"
            result["error"] = str(e)
            return result
    
    async def process_multiple_jobs(
        self,
        job_list: List[Dict[str, Any]],
        resume_text: str,
        candidate_skills: Optional[List[str]] = None,
        auto_apply: bool = False,
        optimization_level: str = "balanced",
        max_parallel: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Process multiple job opportunities in parallel
        
        Args:
            job_list: List of job posting data
            resume_text: Candidate's resume text
            candidate_skills: List of candidate's skills (optional)
            auto_apply: Whether to automatically apply
            optimization_level: Level of resume optimization
            max_parallel: Maximum number of jobs to process in parallel
            
        Returns:
            List of dictionaries with processing results
        """
        results = []
        
        # Process jobs in batches to control concurrency
        for i in range(0, len(job_list), max_parallel):
            batch = job_list[i:i + max_parallel]
            
            # Create tasks for each job in the batch
            tasks = [
                self.process_job_opportunity(
                    job_data=job,
                    resume_text=resume_text,
                    candidate_skills=candidate_skills,
                    auto_apply=auto_apply,
                    optimization_level=optimization_level
                )
                for job in batch
            ]
            
            # Execute batch of tasks concurrently
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results, converting exceptions to error entries
            for job, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Error processing job {job.get('title', 'Unknown')}: {str(result)}")
                    results.append({
                        "job_id": job.get("id", ""),
                        "title": job.get("title", ""),
                        "company": job.get("company", ""),
                        "application_status": "error",
                        "error": str(result),
                        "match_score": 0.0,
                        "application_submitted": False
                    })
                else:
                    results.append(result)
        
        return results
