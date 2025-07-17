"""
Prompt templates module for AI Job Hunt system
"""

from .resume_prompts import RESUME_OPTIMIZATION_PROMPT, RESUME_PARSING_PROMPT
from .job_prompts import JOB_ANALYSIS_PROMPT, JOB_SEARCH_CRITERIA_PROMPT

__all__ = [
    'RESUME_OPTIMIZATION_PROMPT',
    'RESUME_PARSING_PROMPT',
    'JOB_ANALYSIS_PROMPT',
    'JOB_SEARCH_CRITERIA_PROMPT'
]
