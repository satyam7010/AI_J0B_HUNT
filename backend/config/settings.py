"""
Configuration settings for AI Job Hunt system
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import Field

class OllamaSettings(BaseSettings):
    """Ollama LLM settings"""
    api_url: str = Field(default="http://localhost:11434/api")
    model_name: str = Field(default="llama3")
    temperature: float = Field(default=0.7)
    top_p: float = Field(default=0.9)
    max_tokens: int = Field(default=2048)
    timeout: int = Field(default=120)  # seconds
    
    class Config:
        env_prefix = "OLLAMA_"

class OpenAISettings(BaseSettings):
    """OpenAI API settings"""
    api_key: Optional[str] = Field(default=None)
    model_name: str = Field(default="gpt-3.5-turbo")
    temperature: float = Field(default=0.7)
    top_p: float = Field(default=0.9)
    max_tokens: int = Field(default=2048)
    timeout: int = Field(default=60)  # seconds
    
    class Config:
        env_prefix = "OPENAI_"

class DatabaseSettings(BaseSettings):
    """Database settings"""
    url: str = Field(default="sqlite:///data/aijobhunt.db")
    connect_args: Dict[str, Any] = Field(default={"check_same_thread": False})
    
    class Config:
        env_prefix = "DB_"

class PathSettings(BaseSettings):
    """Path settings"""
    data_dir: Path = Field(default=Path("data"))
    resumes_dir: Path = Field(default=Path("data/resumes"))
    job_descriptions_dir: Path = Field(default=Path("data/job_descriptions"))
    application_dir: Path = Field(default=Path("data/applications"))
    
    class Config:
        env_prefix = "PATH_"

class ApplicationSettings(BaseSettings):
    """Application behavior settings"""
    log_level: str = Field(default="INFO")
    log_file: Path = Field(default=Path("logs/application.log"))
    auto_apply_enabled: bool = Field(default=False)
    manual_approval_required: bool = Field(default=True)
    max_daily_applications: int = Field(default=10)
    
    class Config:
        env_prefix = "APP_"

class ResumeSettings(BaseSettings):
    """Resume generator settings"""
    output_dir: Path = Field(default=Path("data/resumes/latex"))
    auto_compile_latex: bool = Field(default=False)
    latex_template_dir: Path = Field(default=Path("data/templates/latex"))
    
    class Config:
        env_prefix = "RESUME_"

class Settings(BaseSettings):
    """Main application settings"""
    # Application info
    app_name: str = Field(default="AI Job Hunt")
    app_version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    # API settings
    api_prefix: str = Field(default="/api")
    cors_origins: List[str] = Field(default=["*"])
    
    # Component settings
    ollama: OllamaSettings = Field(default_factory=OllamaSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    paths: PathSettings = Field(default_factory=PathSettings)
    application: ApplicationSettings = Field(default_factory=ApplicationSettings)
    resume: ResumeSettings = Field(default_factory=ResumeSettings)
    
    # Helper methods
    def is_production(self) -> bool:
        """Check if environment is production"""
        return self.environment.lower() == "production"
    
    def preferred_llm_provider(self) -> str:
        """Get the preferred LLM provider based on configuration"""
        if self.openai.api_key:
            return "openai"
        return "ollama"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()

# Ensure required directories exist
for path_attr in ['data_dir', 'resumes_dir', 'job_descriptions_dir', 'application_dir']:
    path = getattr(settings.paths, path_attr)
    path.mkdir(parents=True, exist_ok=True)

# Ensure log directory exists
log_dir = Path(settings.application.log_file).parent
log_dir.mkdir(parents=True, exist_ok=True)
