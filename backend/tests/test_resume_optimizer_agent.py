"""
Tests for the resume optimizer agent
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from agents.resume_optimizer_agent import ResumeOptimizerAgent
from services.llm_service import LLMService

class TestResumeOptimizerAgent:
    """Test cases for the resume optimizer agent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_llm_service = MagicMock(spec=LLMService)
        self.resume_optimizer = ResumeOptimizerAgent(llm_service=self.mock_llm_service)
    
    @pytest.mark.asyncio
    async def test_optimize_resume(self):
        """Test optimizing a resume"""
        # Setup mock LLM response
        self.mock_llm_service.generate_completion.return_value = asyncio.Future()
        self.mock_llm_service.generate_completion.return_value.set_result("""
### OPTIMIZED RESUME
This is an optimized resume

### CHANGES MADE
- Updated summary
- Added keywords

### KEYWORDS ADDED
python, machine learning, data science

### OPTIMIZATION SUMMARY
Made the resume more targeted for the role

### OPTIMIZATION SCORE
85
""")
        
        # Execute
        result = await self.resume_optimizer.optimize_resume(
            resume_text="Original resume",
            job_description="Job description",
            job_requirements=["Python", "Machine Learning"],
            optimization_level="balanced"
        )
        
        # Verify
        assert "optimized_resume" in result
        assert "changes_made" in result
        assert "keywords_added" in result
        assert "optimization_summary" in result
        assert "optimization_score" in result
        assert result["optimization_score"] == 85.0
        assert "python" in result["keywords_added"]
        
        # Verify LLM was called with correct parameters
        self.mock_llm_service.generate_completion.assert_called_once()
    
    def test_parse_optimization_response(self):
        """Test parsing the LLM response"""
        # Setup
        llm_response = """
### OPTIMIZED RESUME
This is an optimized resume with tailored content

### CHANGES MADE
- Updated professional summary
- Reordered work experience
- Added relevant keywords

### KEYWORDS ADDED
Python, TensorFlow, Machine Learning, Data Analysis

### OPTIMIZATION SUMMARY
This resume has been optimized to highlight relevant experience

### OPTIMIZATION SCORE
92.5
"""
        
        # Execute
        result = self.resume_optimizer._parse_optimization_response(llm_response)
        
        # Verify
        assert result["optimized_resume"] == "This is an optimized resume with tailored content"
        assert len(result["changes_made"]) == 3
        assert "Updated professional summary" in result["changes_made"]
        assert "Python" in result["keywords_added"][0]
        assert result["optimization_score"] == 92.5
