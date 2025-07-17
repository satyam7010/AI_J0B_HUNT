"""
Application Engine Service for AI Job Hunt system
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from ..config.settings import settings
from ..utils.logger import setup_logger
from ..utils.file_utils import ensure_directory, save_json, load_json
from ..agents.application_agent import ApplicationAgent
from .db_manager import DatabaseManager

logger = setup_logger(__name__)

class ApplicationEngine:
    """
    Service for managing the job application workflow,
    including tracking applications, generating metrics,
    and orchestrating the application process
    """
    
    def __init__(self):
        """Initialize the application engine"""
        self.db_manager = DatabaseManager()
        self.application_agent = ApplicationAgent(db_manager=self.db_manager)
        
        # Ensure application directories exist
        self.app_dir = settings.paths.application_dir
        ensure_directory(self.app_dir)
        ensure_directory(self.app_dir / "pending")
        ensure_directory(self.app_dir / "submitted")
        ensure_directory(self.app_dir / "rejected")
        
        logger.info("Application Engine initialized")
    
    async def process_new_job_opportunities(
        self,
        job_list: List[Dict[str, Any]],
        resume_id: str,
        auto_apply: bool = False,
        optimization_level: str = "balanced"
    ) -> Dict[str, Any]:
        """
        Process a list of new job opportunities
        
        Args:
            job_list: List of job posting data
            resume_id: ID of the resume to use
            auto_apply: Whether to automatically apply
            optimization_level: Level of resume optimization
            
        Returns:
            Dictionary with processing results summary
        """
        logger.info(f"Processing {len(job_list)} new job opportunities")
        
        # Get resume data
        resume_data = self.db_manager.get_resume(resume_id)
        if not resume_data:
            logger.error(f"Resume with ID {resume_id} not found")
            return {
                "status": "error",
                "error": f"Resume with ID {resume_id} not found",
                "processed": 0,
                "successful": 0,
                "failed": 0
            }
        
        # Process jobs
        results = await self.application_agent.process_multiple_jobs(
            job_list=job_list,
            resume_text=resume_data.get("text", ""),
            candidate_skills=resume_data.get("skills", []),
            auto_apply=auto_apply,
            optimization_level=optimization_level
        )
        
        # Save results
        successful = [r for r in results if r.get("application_status") not in ["error", "rejected_low_match"]]
        failed = [r for r in results if r.get("application_status") == "error"]
        rejected = [r for r in results if r.get("application_status") == "rejected_low_match"]
        
        logger.info(
            f"Job processing completed: {len(successful)} successful, "
            f"{len(rejected)} rejected, {len(failed)} failed"
        )
        
        # Return summary
        return {
            "status": "completed",
            "processed": len(results),
            "successful": len(successful),
            "rejected": len(rejected),
            "failed": len(failed),
            "auto_applied": len([r for r in results if r.get("application_submitted", False)]),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_application_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about applications
        
        Returns:
            Dictionary with application statistics
        """
        # Query the database for application stats
        stats = self.db_manager.get_application_statistics()
        
        # Calculate conversion rates
        total_jobs_analyzed = stats.get("total_jobs_analyzed", 0)
        if total_jobs_analyzed > 0:
            stats["match_rate"] = stats.get("total_matches", 0) / total_jobs_analyzed
            stats["application_rate"] = stats.get("total_applications", 0) / total_jobs_analyzed
            stats["success_rate"] = stats.get("successful_applications", 0) / max(1, stats.get("total_applications", 0))
        else:
            stats["match_rate"] = 0
            stats["application_rate"] = 0
            stats["success_rate"] = 0
            
        # Add time-based metrics
        stats["applications_last_7_days"] = self.db_manager.get_recent_application_count(days=7)
        stats["applications_last_30_days"] = self.db_manager.get_recent_application_count(days=30)
        
        return stats
    
    def mark_application_as_submitted(self, application_id: str, result: Dict[str, Any]) -> bool:
        """
        Mark an application as submitted
        
        Args:
            application_id: ID of the application
            result: Result data from the submission
            
        Returns:
            Success status
        """
        try:
            # Update the application status in the database
            self.db_manager.update_application_status(
                application_id=application_id,
                status="submitted",
                result=result
            )
            
            # Move application file from pending to submitted directory
            pending_file = self.app_dir / "pending" / f"{application_id}.json"
            submitted_file = self.app_dir / "submitted" / f"{application_id}.json"
            
            if os.path.exists(pending_file):
                # Load, update, and save to new location
                data = load_json(pending_file)
                if data:
                    data["status"] = "submitted"
                    data["submission_result"] = result
                    data["submitted_at"] = datetime.now().isoformat()
                    save_json(data, submitted_file)
                    os.remove(pending_file)
            
            logger.info(f"Application {application_id} marked as submitted")
            return True
            
        except Exception as e:
            logger.error(f"Error marking application {application_id} as submitted: {str(e)}")
            return False
    
    def reject_application(self, application_id: str, reason: str) -> bool:
        """
        Reject an application
        
        Args:
            application_id: ID of the application
            reason: Reason for rejection
            
        Returns:
            Success status
        """
        try:
            # Update the application status in the database
            self.db_manager.update_application_status(
                application_id=application_id,
                status="rejected",
                result={"reason": reason}
            )
            
            # Move application file from pending to rejected directory
            pending_file = self.app_dir / "pending" / f"{application_id}.json"
            rejected_file = self.app_dir / "rejected" / f"{application_id}.json"
            
            if os.path.exists(pending_file):
                # Load, update, and save to new location
                data = load_json(pending_file)
                if data:
                    data["status"] = "rejected"
                    data["rejection_reason"] = reason
                    data["rejected_at"] = datetime.now().isoformat()
                    save_json(data, rejected_file)
                    os.remove(pending_file)
            
            logger.info(f"Application {application_id} rejected: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error rejecting application {application_id}: {str(e)}")
            return False
