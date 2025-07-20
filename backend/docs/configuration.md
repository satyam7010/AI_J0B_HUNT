# Configuration Guide

This document explains how to configure the AI Job Hunt system.

## Environment Variables

The system uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

```
# Database
DATABASE_URL=sqlite:///job_applications.db

# LLM Configuration
LLM_PROVIDER=ollama  # Options: ollama, openai
LLM_MODEL=gemma:3.4b  # For Ollama
# LLM_MODEL=gpt-4  # For OpenAI
# OPENAI_API_KEY=your-api-key  # Only needed for OpenAI

# API
API_HOST=0.0.0.0
API_PORT=8000
ENABLE_CORS=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8501

# Frontend
FRONTEND_PORT=8501

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/application.log

# Job Scraper
SCRAPER_INTERVAL=3600  # In seconds
MAX_JOBS_PER_SEARCH=20
```

## Configuration File

For more complex configuration, the system also uses a settings file located at `backend/config/settings.py`. This file provides sensible defaults that can be overridden by environment variables.

Key settings:

```python
# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///job_applications.db")

# LLM settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma:3.4b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
ENABLE_CORS = os.getenv("ENABLE_CORS", "true").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")

# Frontend settings
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/application.log")

# Job scraper settings
SCRAPER_INTERVAL = int(os.getenv("SCRAPER_INTERVAL", "3600"))
MAX_JOBS_PER_SEARCH = int(os.getenv("MAX_JOBS_PER_SEARCH", "20"))
```

## LLM Configuration

### Ollama (Default)

The system is configured to use Ollama with the Gemma 3.4b model by default. Ensure Ollama is installed and the model is downloaded:

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Download the Gemma model
ollama pull gemma:3.4b
```

### OpenAI (Alternative)

To use OpenAI instead:

1. Set the environment variables:
   ```
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4
   OPENAI_API_KEY=your-api-key
   ```

2. Or modify the settings in `backend/config/settings.py`:
   ```python
   LLM_PROVIDER = "openai"
   LLM_MODEL = "gpt-4"
   OPENAI_API_KEY = "your-api-key"
   ```

## Logging Configuration

Logs are stored in the `logs/application.log` file by default. The logging level can be configured in the `.env` file or in `backend/config/settings.py`.

Available log levels:
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

For more verbose logging, set `LOG_LEVEL=DEBUG`.

## Advanced Configuration

For advanced configuration options, refer to the specific module documentation:

- Resume Parser Configuration: See `backend/services/resume_parser.py`
- Job Scraper Configuration: See `backend/services/job_scraper.py`
- Application Engine Configuration: See `backend/services/application_engine.py`
