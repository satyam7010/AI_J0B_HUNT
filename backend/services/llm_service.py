"""
LLM Service for AI Job Hunt system
"""

import os
import json
import logging
import aiohttp
import asyncio
from typing import Dict, List, Any, Optional, Union

from ..config.settings import settings
from ..utils.logger import setup_logger
from ..utils.automation_helpers import retry_operation

logger = setup_logger(__name__)

class LLMService:
    """
    Service for interacting with Large Language Models (LLMs)
    through various providers (Ollama, OpenAI)
    """
    
    def __init__(self):
        """Initialize the LLM service"""
        self.provider = settings.preferred_llm_provider()
        logger.info(f"LLM Service initialized with provider: {self.provider}")
    
    async def generate_completion(
        self, 
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        top_p: float = 0.9,
        stop_sequences: Optional[List[str]] = None,
        system_message: Optional[str] = None
    ) -> str:
        """
        Generate a completion using the configured LLM provider
        
        Args:
            prompt: The prompt to send to the LLM
            model: Model name to use (defaults to configured model)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            stop_sequences: List of sequences that stop generation
            system_message: System message for chat models
            
        Returns:
            Generated text from the LLM
        """
        if self.provider == "ollama":
            return await self._ollama_completion(
                prompt=prompt,
                model=model or settings.ollama.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stop_sequences=stop_sequences,
                system_message=system_message
            )
        elif self.provider == "openai":
            return await self._openai_completion(
                prompt=prompt,
                model=model or settings.openai.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stop_sequences=stop_sequences,
                system_message=system_message
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def _ollama_completion(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        stop_sequences: Optional[List[str]],
        system_message: Optional[str]
    ) -> str:
        """
        Generate a completion using Ollama API
        
        Args:
            See generate_completion method
            
        Returns:
            Generated text from Ollama
        """
        api_url = f"{settings.ollama.api_url.rstrip('/')}/generate"
        
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "num_predict": max_tokens,
            "top_p": top_p
        }
        
        # Add optional parameters if provided
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        if system_message:
            payload["system"] = system_message
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url, 
                    json=payload,
                    timeout=settings.ollama.timeout
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama API error: {response.status}, {error_text}")
                        raise Exception(f"Ollama API error: {response.status}, {error_text}")
                    
                    data = await response.json()
                    return data.get("response", "")
                    
        except aiohttp.ClientError as e:
            logger.error(f"Ollama API connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Ollama API unexpected error: {str(e)}")
            raise
    
    async def _openai_completion(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        stop_sequences: Optional[List[str]],
        system_message: Optional[str]
    ) -> str:
        """
        Generate a completion using OpenAI API
        
        Args:
            See generate_completion method
            
        Returns:
            Generated text from OpenAI
        """
        if not settings.openai.api_key:
            raise ValueError("OpenAI API key not configured")
        
        api_url = "https://api.openai.com/v1/chat/completions"
        
        # Prepare messages
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        # Prepare the request payload
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        
        # Add optional parameters if provided
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.openai.api_key}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url, 
                    json=payload,
                    headers=headers,
                    timeout=settings.openai.timeout
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"OpenAI API error: {response.status}, {error_text}")
                        raise Exception(f"OpenAI API error: {response.status}, {error_text}")
                    
                    data = await response.json()
                    return data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
        except aiohttp.ClientError as e:
            logger.error(f"OpenAI API connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"OpenAI API unexpected error: {str(e)}")
            raise
