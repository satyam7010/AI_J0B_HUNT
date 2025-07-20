#!/usr/bin/env python3
"""
Example Usage Script for AI Job Hunt System
This script demonstrates how to use the AI Job Hunt system programmatically
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.services.db_manager import DatabaseManager
from backend.services.resume_parser import ResumeParser
from backend.agents.job_description_agent import JobDescriptionAgent
from backend.agents.resume_optimizer_agent import ResumeOptimizerAgent
from backend.agents.application_agent import ApplicationAgent


async def example_workflow():
    """Example workflow demonstrating the complete job application process"""
    
    print("🎯 AI Job Hunt - Example Workflow")
    print("=" * 50)
    
    # Initialize components
    db = DatabaseManager()
    resume_parser = ResumeParser()
    job_description_agent = JobDescriptionAgent()
    resume_optimizer_agent = ResumeOptimizerAgent()
    application_agent = ApplicationAgent()
    
    # Initialize database
    print("✅ Database initialized")
    
    # Step 1: Parse a sample resume
    print("\n📄 Step 1: Parsing resume")
    sample_resume_path = Path(__file__).parent.parent / "data" / "examples" / "sample_resume.txt"
    if sample_resume_path.exists():
        resume_data = resume_parser.parse_resume(str(sample_resume_path))
        print(f"✅ Resume parsed: {sample_resume_path}")
        print(f"   Found {len(resume_data.get('skills', []))} skills")
    else:
        print(f"❌ Sample resume not found at: {sample_resume_path}")
    
    # Step 2: Analyze a job description
    print("\n🔍 Step 2: Analyzing job description")
    sample_job_path = Path(__file__).parent.parent / "data" / "examples" / "sample_job_description.txt"
    if sample_job_path.exists():
        with open(sample_job_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        try:
            job_analysis = await job_description_agent.analyze_job_description(job_description)
            print(f"✅ Job analyzed: {sample_job_path}")
            print(f"   Required skills: {', '.join(job_analysis.get('required_skills', [])[:5])}...")
        except Exception as e:
            print(f"❌ Error analyzing job: {str(e)}")
    else:
        print(f"❌ Sample job description not found at: {sample_job_path}")
    
    # Step 3: Check if Ollama is available
    print("\n🤖 Step 3: Checking Ollama availability")
    try:
        ollama_status = await resume_optimizer_agent.check_ollama_connection()
        if ollama_status:
            print("✅ Ollama is available")
            
            # Step 4: Optimize resume for job (if Ollama is available)
            print("\n✨ Step 4: Optimizing resume for job")
            try:
                print("   This would optimize the resume for the job...")
                # Actual implementation would call:
                # optimized_resume = await resume_optimizer_agent.optimize_resume_for_job(resume_data, job_analysis)
                print("✅ Resume optimization simulation completed")
            except Exception as e:
                print(f"❌ Error in resume optimization: {str(e)}")
        else:
            print("❌ Ollama is not available")
    except Exception as e:
        print(f"❌ Error checking Ollama: {str(e)}")
    
    print("\n🎉 Example workflow completed")


if __name__ == "__main__":
    asyncio.run(example_workflow())
