"""
Resume Optimizer Agent for AI Job Hunt system
"""

import logging
from typing import Dict, List, Any, Optional, Union
import asyncio
import os
import re
import subprocess
from pathlib import Path

from ..config.settings import settings
from ..utils.logger import setup_logger
from ..utils.file_utils import ensure_directory
from ..services.llm_service import LLMService
from ..prompts.resume_prompts import RESUME_OPTIMIZATION_PROMPT, LATEX_RESUME_PROMPT

logger = setup_logger(__name__)

class ResumeOptimizerAgent:
    """
    Agent responsible for optimizing resumes based on job descriptions
    using LLM-powered analysis and tailoring
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize the resume optimizer agent
        
        Args:
            llm_service: LLM service to use (creates a new one if not provided)
        """
        self.llm_service = llm_service or LLMService()
        logger.info("Resume Optimizer Agent initialized")
    
    async def optimize_resume(
        self, 
        resume_text: str, 
        job_description: str,
        job_requirements: Optional[List[str]] = None,
        company_info: Optional[str] = None,
        optimization_level: str = "balanced"
    ) -> Dict[str, Any]:
        """
        Optimize a resume for a specific job
        
        Args:
            resume_text: Original resume content
            job_description: Job description text
            job_requirements: List of specific job requirements (optional)
            company_info: Information about the company (optional)
            optimization_level: Level of optimization (conservative, balanced, aggressive)
            
        Returns:
            Dictionary containing the optimized resume and optimization metadata
        """
        logger.info(f"Optimizing resume with {optimization_level} optimization level")
        
        # Prepare the prompt with all relevant information
        prompt_vars = {
            "resume": resume_text,
            "job_description": job_description,
            "job_requirements": job_requirements or [],
            "company_info": company_info or "",
            "optimization_level": optimization_level
        }
        
        # Generate the prompt
        prompt = RESUME_OPTIMIZATION_PROMPT.format(**prompt_vars)
        
        try:
            # Get response from LLM
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                temperature=settings.ollama.temperature,
                max_tokens=settings.ollama.max_tokens
            )
            
            # Parse and structure the LLM response
            # This is a simplified version - in a real implementation,
            # we would add more robust parsing of the structured output
            parsed_response = self._parse_optimization_response(llm_response)
            
            logger.info("Resume optimization completed successfully")
            return parsed_response
            
        except Exception as e:
            logger.error(f"Error optimizing resume: {str(e)}")
            raise
    
    def _parse_optimization_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse the LLM response into a structured format
        
        Args:
            llm_response: Raw response from the LLM
            
        Returns:
            Structured dictionary with optimized resume and metadata
        """
        # This is a simplified parser - in a real implementation, 
        # we would use more robust parsing techniques
        
        # Default structure
        result = {
            "optimized_resume": "",
            "changes_made": [],
            "keywords_added": [],
            "optimization_summary": "",
            "optimization_score": 0.0
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
            if "optimized resume" in title:
                result["optimized_resume"] = content
            elif "changes made" in title:
                result["changes_made"] = [
                    change.strip() 
                    for change in content.split("-") 
                    if change.strip()
                ]
            elif "keywords added" in title:
                result["keywords_added"] = [
                    keyword.strip() 
                    for keyword in content.split(",") 
                    if keyword.strip()
                ]
            elif "summary" in title:
                result["optimization_summary"] = content
            elif "score" in title:
                try:
                    # Extract just the number
                    score_match = re.search(r'(\d+(\.\d+)?)', content)
                    if score_match:
                        result["optimization_score"] = float(score_match.group(1))
                except ValueError:
                    # If conversion fails, keep default
                    pass
        
        return result
    
    async def generate_latex_resume(
        self, 
        resume_text: str, 
        job_description: str,
        job_requirements: Optional[List[str]] = None,
        company_info: Optional[str] = None,
        optimization_level: str = "balanced",
        output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a LaTeX-formatted resume optimized for a specific job
        
        Args:
            resume_text: Original resume content
            job_description: Job description text
            job_requirements: List of specific job requirements (optional)
            company_info: Information about the company (optional)
            optimization_level: Level of optimization (conservative, balanced, aggressive)
            output_dir: Directory to save LaTeX section files (optional)
            
        Returns:
            Dictionary containing LaTeX content for each section
        """
        logger.info(f"Generating LaTeX resume with {optimization_level} optimization level")
        
        # Prepare the prompt with all relevant information
        prompt_vars = {
            "resume": resume_text,
            "job_description": job_description,
            "job_requirements": "\n".join(job_requirements) if job_requirements else "",
            "company_info": company_info or "",
            "optimization_level": optimization_level
        }
        
        # Generate the prompt
        prompt = LATEX_RESUME_PROMPT.format(**prompt_vars)
        
        try:
            # Get response from LLM
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                temperature=settings.ollama.temperature,
                max_tokens=settings.ollama.max_tokens
            )
            
            # Parse and structure the LaTeX sections
            latex_sections = self._parse_latex_response(llm_response)
            
            # If output directory is provided, save sections to files
            if output_dir:
                self._save_latex_sections(latex_sections, output_dir)
                
                # Optionally compile the LaTeX document
                if settings.resume.auto_compile_latex:
                    self._compile_latex(output_dir)
            
            logger.info("LaTeX resume generation completed successfully")
            return latex_sections
            
        except Exception as e:
            logger.error(f"Error generating LaTeX resume: {str(e)}")
            raise
    
    def _parse_latex_response(self, llm_response: str) -> Dict[str, str]:
        """
        Parse the LLM response to extract LaTeX sections
        
        Args:
            llm_response: Raw response from the LLM
            
        Returns:
            Dictionary with section names as keys and LaTeX content as values
        """
        # Default sections
        latex_sections = {
            "profile": "",
            "experience": "",
            "projects": "",
            "education": "",
            "skills": ""
        }
        
        try:
            # Try to extract JSON from the response
            json_start = llm_response.find('{')
            json_end = llm_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                import json
                json_str = llm_response[json_start:json_end]
                parsed_sections = json.loads(json_str)
                
                # Update sections with parsed content
                for key, value in parsed_sections.items():
                    if key in latex_sections:
                        latex_sections[key] = value
            else:
                # Fallback to section extraction if JSON parsing fails
                section_patterns = {
                    "profile": r"\\section\{Profile Summary\}(.*?)(?=\\section|$)",
                    "experience": r"\\section\{Experience\}(.*?)(?=\\section|$)",
                    "projects": r"\\section\{Projects\}(.*?)(?=\\section|$)",
                    "education": r"\\section\{Education\}(.*?)(?=\\section|$)",
                    "skills": r"\\section\{Technical Skills\}(.*?)(?=\\section|$)"
                }
                
                for section_name, pattern in section_patterns.items():
                    matches = re.search(pattern, llm_response, re.DOTALL)
                    if matches:
                        latex_sections[section_name] = f"\\section{{{section_name.title()}}}{matches.group(1).strip()}"
        
        except Exception as e:
            logger.error(f"Error parsing LaTeX sections: {str(e)}")
        
        return latex_sections
    
    def _save_latex_sections(self, latex_sections: Dict[str, str], output_dir: str) -> None:
        """
        Save LaTeX sections to individual files
        
        Args:
            latex_sections: Dictionary with section names and LaTeX content
            output_dir: Directory to save files
        """
        # Ensure output directory exists
        src_dir = os.path.join(output_dir, "src")
        ensure_directory(src_dir)
        
        # Save each section to a file
        for section_name, content in latex_sections.items():
            if content.strip():
                file_path = os.path.join(src_dir, f"{section_name}.tex")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"Saved {section_name} section to {file_path}")
    
    def _compile_latex(self, output_dir: str) -> bool:
        """
        Compile the LaTeX resume
        
        Args:
            output_dir: Directory containing LaTeX files
            
        Returns:
            True if compilation was successful, False otherwise
        """
        try:
            # Assuming main.tex exists in the output directory
            main_tex_path = os.path.join(output_dir, "main.tex")
            
            if not os.path.exists(main_tex_path):
                logger.error(f"Main LaTeX file not found at {main_tex_path}")
                return False
            
            # Compile using latexmk
            result = subprocess.run(
                ["latexmk", "-pdf", main_tex_path],
                cwd=output_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"LaTeX compilation successful. PDF saved to {output_dir}")
                return True
            else:
                logger.error(f"LaTeX compilation failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error compiling LaTeX: {str(e)}")
            return False
