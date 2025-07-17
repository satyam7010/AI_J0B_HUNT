"""
Tests for the LLM service
"""

import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock

from services.llm_service import LLMService
from config.settings import settings

# Skip these tests if no LLM API is configured
pytestmark = pytest.mark.skipif(
    not settings.ollama.api_url and not settings.openai.api_key,
    reason="No LLM API configured"
)

class TestLLMService:
    """Test cases for the LLM service"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.llm_service = LLMService()
    
    @patch("backend.services.llm_service.LLMService._ollama_completion")
    async def test_generate_completion_ollama(self, mock_ollama):
        """Test generating a completion with Ollama"""
        # Setup
        mock_ollama.return_value = "Mocked response from Ollama"
        self.llm_service.provider = "ollama"
        
        # Execute
        result = await self.llm_service.generate_completion(
            prompt="Test prompt",
            temperature=0.7,
            max_tokens=100
        )
        
        # Verify
        assert result == "Mocked response from Ollama"
        mock_ollama.assert_called_once()
    
    @patch("backend.services.llm_service.LLMService._openai_completion")
    async def test_generate_completion_openai(self, mock_openai):
        """Test generating a completion with OpenAI"""
        # Setup
        mock_openai.return_value = "Mocked response from OpenAI"
        self.llm_service.provider = "openai"
        
        # Execute
        result = await self.llm_service.generate_completion(
            prompt="Test prompt",
            temperature=0.7,
            max_tokens=100
        )
        
        # Verify
        assert result == "Mocked response from OpenAI"
        mock_openai.assert_called_once()
    
    async def test_invalid_provider(self):
        """Test with an invalid provider"""
        # Setup
        self.llm_service.provider = "invalid_provider"
        
        # Execute and Verify
        with pytest.raises(ValueError):
            await self.llm_service.generate_completion(
                prompt="Test prompt",
                temperature=0.7,
                max_tokens=100
            )
