"""
Pytest configuration file with shared fixtures
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the root directory to Python path to ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import services
from services.llm_service import LLMService
from services.db_manager import DatabaseManager
from services.resume_parser import ResumeParser
from services.job_scraper import JobScraper
from services.application_engine import ApplicationEngine

# Import agents
from backend.agents.resume_optimizer_agent import ResumeOptimizerAgent
from backend.agents.job_description_agent import JobDescriptionAnalysisAgent
from backend.agents.application_agent import ApplicationAgent

@pytest.fixture
def mock_llm_service():
    """Fixture for a mocked LLM service"""
    mock_service = MagicMock(spec=LLMService)
    
    # Setup common mock behaviors
    async def mock_generate_completion(*args, **kwargs):
        return "Mocked LLM response"
    
    mock_service.generate_completion.side_effect = mock_generate_completion
    return mock_service

@pytest.fixture
def mock_db_manager():
    """Fixture for a mocked database manager"""
    return MagicMock(spec=DatabaseManager)

@pytest.fixture
def mock_resume_parser():
    """Fixture for a mocked resume parser"""
    return MagicMock(spec=ResumeParser)

@pytest.fixture
def mock_job_scraper():
    """Fixture for a mocked job scraper"""
    return MagicMock(spec=JobScraper)

@pytest.fixture
def mock_application_engine():
    """Fixture for a mocked application engine"""
    return MagicMock(spec=ApplicationEngine)

@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing"""
    return """
JOHN DOE
Software Engineer

SUMMARY
Experienced software engineer with 5+ years of experience in Python, JavaScript, and cloud technologies.

SKILLS
- Python, JavaScript, TypeScript
- React, Vue.js, Node.js
- AWS, Docker, Kubernetes
- Machine Learning, Data Analysis

EXPERIENCE
Senior Software Engineer, TechCorp (2020-Present)
- Developed and maintained microservices architecture
- Implemented ML models for predictive analytics
- Led team of 5 engineers on key projects

Software Engineer, CodeInnovation (2018-2020)
- Built responsive web applications with React
- Integrated third-party APIs and services
- Improved application performance by 40%

EDUCATION
Bachelor of Science in Computer Science
University of Technology (2014-2018)
    """

@pytest.fixture
def sample_job_description():
    """Sample job description for testing"""
    return """
# Senior Software Engineer

## About Us
We are a leading technology company building innovative solutions for enterprise clients.

## Job Description
We are seeking a Senior Software Engineer with strong Python skills to join our growing team.

## Requirements
- 5+ years of experience in software development
- Strong Python and JavaScript skills
- Experience with cloud platforms (AWS preferred)
- Bachelor's degree in Computer Science or related field
- Experience with machine learning is a plus

## Responsibilities
- Design and develop scalable backend services
- Work with cross-functional teams to deliver high-quality solutions
- Mentor junior engineers
- Contribute to architectural decisions
    """
