# AI Job Hunt Architecture

This document outlines the architecture of the AI Job Hunt system.

## System Components

The AI Job Hunt system consists of the following main components:

### Backend Components

1. **API Layer**
   - FastAPI-based RESTful API
   - Handles incoming requests and responses
   - Routes in `api/` directory

2. **Agents**
   - `resume_optimizer_agent.py` - Optimizes resumes using LLM
   - `job_description_agent.py` - Analyzes job descriptions using LLM
   - `application_agent.py` - Handles application automation and submission

3. **Services**
   - `db_manager.py` - Handles database operations
   - `llm_service.py` - Provides LLM integration
   - `resume_parser.py` - Parses and extracts information from resumes
   - Other utility services

4. **Models**
   - Data models for applications, jobs, and resumes
   - Located in `models/` directory

5. **Utilities**
   - Logger
   - File utilities
   - Automation helpers

### Frontend Components

- Streamlit dashboard for visualization and interaction
- Located in `frontend/` directory

## Data Flow

1. Resume is uploaded and parsed by `resume_parser.py`
2. Job descriptions are analyzed by `job_description_agent.py`
3. Resumes are optimized by `resume_optimizer_agent.py`
4. Applications are submitted by `application_agent.py`
5. All data is stored and retrieved using `db_manager.py`

## Technology Stack

- Python 3.8+
- FastAPI for backend API
- Streamlit for frontend dashboard
- SQLite for database (via SQLAlchemy)
- Ollama for local LLM inference
- Selenium/Playwright for web automation
