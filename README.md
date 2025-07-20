# AI Job Hunt - Automated Job Application System

An AI-powered job application automation system that uses Gemma 3.4b model via Ollama to optimize your job search process.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Command-line Interface](#command-line-interface)
  - [Web Dashboard](#web-dashboard)
  - [Complete Workflow](#complete-workflow)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [AI Features](#ai-features)
- [Advanced Features](#advanced-features)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

AI Job Hunt automates and optimizes the job application process by:
- Parsing resumes and extracting structured content
- Analyzing job descriptions and requirements
- Using Gemma 3.4b model via Ollama to optimize resumes for specific positions
- Automatically applying to job portals (LinkedIn, Indeed, Naukri)
- Tracking applications and maintaining a dashboard for monitoring

## Features

### 🔍 Core Features
- **Resume Parsing**: Extract structured content from PDF, DOCX, and TXT resumes
- **Job Analysis**: Analyze job descriptions to extract requirements, skills, and other key information
- **AI Optimization**: Use Gemma 3.4b model via Ollama to optimize resumes for specific job descriptions
- **Automated Applications**: Apply to jobs on LinkedIn, Indeed, and Naukri automatically
- **Application Tracking**: Track all applications with status updates and analytics
- **Manual Review**: Review and approve applications before submission
- **Dashboard**: Web-based dashboard for managing the entire process

### 🤖 AI-Powered Features
- **Resume Optimization**: Tailor resumes to specific job requirements
- **ATS Optimization**: Ensure resumes are ATS-friendly
- **Job Matching**: Analyze how well your resume matches job requirements
- **Cover Letter Generation**: Auto-generate personalized cover letters
- **Skills Gap Analysis**: Identify missing skills and improvement areas

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed for local AI model inference
- Chrome or Firefox browser installed (for automated job applications)
- Internet connection

## Installation

### Step 1: Set up your environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Ollama

Download and install Ollama from [https://ollama.ai/](https://ollama.ai/)

#### Windows
1. Download the Windows installer from [ollama.ai](https://ollama.ai/)
2. Run the installer and follow the prompts
3. Once installed, Ollama will run as a service in the background

#### macOS
1. Download the macOS app from [ollama.ai](https://ollama.ai/)
2. Move it to your Applications folder
3. Launch the app

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 3: Pull the Gemma model

```bash
ollama pull gemma:3.4b
```

### Step 4: Configure environment variables

Copy the `.env.example` file to `.env` and edit it according to your needs:

```bash
cp .env.example .env
```

## Configuration

For detailed configuration options, see the [Configuration Guide](backend/docs/configuration.md).

### Basic Configuration
Edit the `.env` file with your preferences:

```env
# Database
DATABASE_URL=sqlite:///job_applications.db

# LLM Configuration
LLM_PROVIDER=ollama  # Options: ollama, openai
LLM_MODEL=gemma:3.4b  # For Ollama

# API
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
FRONTEND_PORT=8501

# Job Portal Credentials (optional)
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
INDEED_EMAIL=your_email@example.com
INDEED_PASSWORD=your_password
```

## Usage

### Command-line Interface

The system provides several entry points:

```bash
# Run both backend and frontend
python main.py

# Run backend only
python run_backend.bat

# Run frontend dashboard only
python run_dashboard.py
```

### Web Dashboard

You can access the Streamlit web dashboard by opening http://localhost:8501 in your web browser.

#### Dashboard Sections

- **📊 Dashboard Page**: View application statistics, monitor success rates, track recent applications
- **📄 Resume Management**: Upload and parse resumes, view parsed content, manage multiple resumes
- **🔍 Job Analysis**: Analyze job postings, extract required skills, identify requirements
- **🤖 AI Optimization**: Optimize resumes for specific jobs, analyze compatibility, generate cover letters
- **📝 Applications**: View all applications, review pending applications, update status
- **⚙️ Settings**: Configure job search criteria, set skill requirements, test platform credentials

### Complete Workflow

Here's a complete workflow for using the system:

1. **Upload your resume**
   - Use option 1 in the CLI or the "Resume Upload" section in the dashboard.
   - The system will parse your resume and extract structured information.

2. **Configure job search settings**
   - Set up your job search criteria in the dashboard:
     - Job titles
     - Skills
     - Location
     - Experience level
     - Job portals to search

3. **Analyze job descriptions**
   - Use option 2 in the CLI or the "Job Analysis" section in the dashboard.
   - The system will identify required skills, responsibilities, and qualifications.

4. **Optimize your resume**
   - Use option 3 in the CLI or the "Resume Optimization" section in the dashboard.
   - The system will use the Gemma 3.4b model to tailor your resume for the specific job.

5. **Review and approve applications**
   - In the dashboard, review optimized resumes and approve them for submission.

6. **Monitor application status**
   - Track your applications in the dashboard:
     - Pending applications
     - Submitted applications
     - Application status
     - Follow-up reminders

### Automated Job Search and Application

To enable fully automated job searching and applications:

1. Set `AUTO_APPLY_ENABLED=true` in your `.env` file
2. Configure your credentials for job portals in the `.env` file
3. Run option 4 in the CLI or use the "Automation" section in the dashboard

The system will:
1. Search for jobs matching your criteria
2. Analyze job descriptions
3. Optimize your resume for each job
4. Apply to jobs (with manual approval if configured)
5. Track application status

## Architecture

The AI Job Hunt system follows a modular architecture with two main components:

- **Backend** - Core API, agents, and services
- **Frontend** - Web dashboard for user interaction

## Project Structure

The project is organized into two main directories:

```
AI_JOB_HUNT/
├── README.md           - Main documentation
├── .env                - Environment variables
├── .gitignore          - Git ignore rules
├── main.py             - Main entry point
├── run_backend.bat     - Backend launcher
├── run_dashboard.py    - Dashboard launcher
├── requirements.txt    - Python dependencies
├── backend/            - Backend API and services
│   ├── main.py         - Backend entry point
│   ├── agents/         - AI agents (resume optimizer, job analyzer)
│   │   ├── __init__.py
│   │   ├── application_agent.py
│   │   ├── job_description_agent.py
│   │   └── resume_optimizer_agent.py
│   ├── api/            - API routes and controllers
│   │   ├── __init__.py
│   │   ├── apply_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── job_routes.py
│   │   └── resume_routes.py
│   ├── config/         - Configuration settings
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── docs/           - Documentation
│   │   ├── README.md
│   │   ├── api-reference.md
│   │   ├── architecture.md
│   │   ├── configuration.md
│   │   ├── database-schema.md
│   │   └── deployment.md
│   ├── examples/       - Example scripts
│   │   ├── README.md
│   │   └── example_usage.py
│   ├── models/         - Data models
│   │   ├── application.py
│   │   ├── job.py
│   │   └── resume.py
│   ├── prompts/        - AI prompt templates
│   │   ├── __init__.py
│   │   ├── job_prompts.py
│   │   └── resume_prompts.py
│   ├── services/       - Core services
│   │   ├── __init__.py
│   │   ├── application_engine.py
│   │   ├── db_manager.py
│   │   ├── job_scraper.py
│   │   ├── llm_service.py
│   │   └── resume_parser.py
│   ├── tests/          - Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_llm_service.py
│   │   └── test_resume_optimizer_agent.py
│   └── utils/          - Utility functions
│       ├── __init__.py
│       ├── automation_helpers.py
│       ├── file_utils.py
│       └── logger.py
├── data/               - Data storage
│   └── examples/       - Example data files
│       ├── sample_job_description.txt
│       └── sample_resume.txt
├── frontend/           - Frontend dashboard
│   ├── public/         - Public assets
│   └── src/            - Frontend source code
│       ├── assets/     - Static assets
│       ├── components/ - UI components
│       ├── hooks/      - React hooks
│       ├── pages/      - Page components
│       └── services/   - Frontend services
├── logs/               - Application logs
│   └── application.log
└── job_applications.db - SQLite database
```

## AI Features

### Resume Optimization
The AI optimizer uses Gemma 3.4b to:
- Analyze job descriptions
- Extract key requirements
- Tailor resume content
- Improve ATS compatibility
- Enhance keyword matching
- Quantify achievements

### Job Matching
- Calculate compatibility scores
- Identify skill gaps
- Suggest improvements
- Highlight strengths
- Recommend focus areas

### Cover Letter Generation
- Create personalized cover letters
- Match company culture
- Highlight relevant experience
- Professional formatting
- Compelling narrative

## Advanced Features

### Custom Resume Templates
You can create custom resume templates in the `templates` directory using Jinja2 syntax.

### Scheduled Job Searches
Configure scheduled job searches in the dashboard or by editing the `.env` file:

```
# Schedule Settings
SCHEDULE_ENABLED=true
SCHEDULE_TIME=08:00
```

## Documentation

Comprehensive documentation is available in the `backend/docs/` directory:

- [API Reference](backend/docs/api-reference.md) - API endpoint documentation
- [Architecture](backend/docs/architecture.md) - System architecture overview
- [Configuration](backend/docs/configuration.md) - Detailed configuration options
- [Database Schema](backend/docs/database-schema.md) - Database structure
- [Deployment](backend/docs/deployment.md) - Deployment instructions
SCHEDULE_TIME=08:00
```

### Application Analytics
The dashboard provides analytics on your job applications, including:
- Application success rate
- Most requested skills
- Job market trends
- Application timeline

### Using the Python API Programmatically

You can also use the system programmatically in your own Python scripts:

```python
import asyncio
from src.resume_parser import ResumeParser
from src.job_analyzer import JobAnalyzer
from src.ai_optimizer import AIOptimizer
from src.job_applier import JobApplier
from src.database import DatabaseManager

async def main():
    # Initialize components
    db_manager = DatabaseManager()
    resume_parser = ResumeParser()
    job_analyzer = JobAnalyzer()
    ai_optimizer = AIOptimizer()
    job_applier = JobApplier()
    
    # Parse resume
    resume_path = "data/my_resume.pdf"
    resume_data = resume_parser.parse_resume(resume_path)
    
    # Analyze job
    job_url = "https://www.example.com/jobs/12345"
    job_data = job_analyzer.analyze_job_url(job_url)
    
    # Optimize resume
    optimized_resume = await ai_optimizer.optimize_resume(
        job_data['description'], 
        resume_data
    )
    
    # Apply to job
    result = await job_applier.apply_to_job(job_data, optimized_resume)
    
    # Save application
    db_manager.save_application_result(job_data, result)
    
    print(f"Application result: {result['status']}")

# Run the async function
asyncio.run(main())
```

## Ollama Setup

### System Requirements

To run Gemma 3.4b with Ollama, you'll need:

- **CPU**: A modern multi-core CPU (4+ cores recommended)
- **RAM**: At least 8GB of RAM (16GB recommended)
- **Storage**: At least 5GB of free disk space
- **GPU (Optional)**: A CUDA-compatible NVIDIA GPU with 6GB+ VRAM for faster inference

### Verifying Ollama Installation

Open a terminal or command prompt and run:

```bash
ollama --version
```

You should see the version number displayed.

### Starting Ollama Server

If not already running, start the Ollama server:

```bash
ollama serve
```

### Testing the Model

Test if the model is working correctly:

```bash
ollama run gemma:3.4b "Hello, I'm looking for a job in software engineering. Can you help me optimize my resume?"
```

The model should respond with helpful advice.

### GPU Acceleration

If you have a compatible NVIDIA GPU:

1. Make sure you have the latest CUDA drivers installed
2. Ollama should automatically use the GPU

To verify GPU usage:
```bash
nvidia-smi
```

During model inference, you should see the Ollama process using GPU resources.

### Alternatives to Gemma 3.4b

If you have issues with the Gemma model, you can try these alternatives:

- `llama3:8b` - The Llama 3 8B model
- `mistral:7b` - The Mistral 7B model
- `phi3:3.8b` - The Phi-3 3.8B model

To use an alternative model, update your `.env` file:

```
GEMMA_MODEL=llama3:8b
```

Then pull the model:

```bash
ollama pull llama3:8b
```

## Prompt Templates

The prompts are organized in the `src/prompt_template.py` file and include:

1. **System prompts** - Define the AI's role and general behavior
2. **User prompt templates** - Dynamic templates for specific tasks
3. **Helper functions** - For generating formatted prompts

### Using Prompt Templates

```python
# Import system prompts directly
from src.prompt_template import AI_OPTIMIZER_PROMPT, JOB_ANALYZER_PROMPT

# Import template functions
from src.prompt_template import get_optimizer_prompt, get_job_analysis_prompt

# Generate a prompt for optimizing a resume
resume_text = "..."  # Original resume
job_description = "..."  # Job description
prompt = get_optimizer_prompt(resume_text, job_description)

# Use the prompt with the AI model
response = await call_ai_model(prompt)
```

### Customizing Prompts

You can customize the prompts to adjust the AI's behavior:

1. Edit the prompt constants in `src/prompt_template.py`
2. Create new template functions for specific use cases
3. Use environment variables to allow runtime configuration

## Troubleshooting

### Ollama Issues

If you encounter issues with Ollama:

1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

2. Verify the model is properly installed:
   ```bash
   ollama list
   ```

3. Check the OLLAMA_API_URL in your .env file (default: http://localhost:11434)

### API Connection Issues

If the application can't connect to Ollama:

1. Make sure the Ollama server is running:
   ```bash
   ollama serve
   ```

2. Check if the API is accessible:
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. Verify the URL in your `.env` file matches the actual Ollama server address.

### Memory Issues

If you encounter out-of-memory errors:

1. Close other resource-intensive applications
2. Try using a smaller model like `gemma:2b` (though with reduced quality)
3. If using GPU acceleration, try switching to CPU-only mode

### Selenium/Playwright Issues

If you encounter issues with automated applications:

1. Make sure you have Chrome or Firefox installed
2. Try installing the browser drivers manually:
   ```bash
   playwright install
   ```

3. Check your internet connection and job portal credentials

### Database Issues
```bash
# Delete database to reset
rm job_applications.db

# Restart application
python main.py
```

### Platform Login Issues
- Check credentials in .env file
- Verify account access
- Clear browser cache
- Check for CAPTCHA requirements

### Resume Parsing Issues
- Ensure file format is supported (PDF, DOCX, TXT)
- Check file permissions
- Verify file isn't corrupted
- Try different file formats

## Best Practices

### Resume Optimization
1. **Use Multiple Resumes**: Create different versions for different job types
2. **Update Regularly**: Keep resumes current with latest experience
3. **Keyword Matching**: Ensure resumes contain relevant keywords
4. **ATS Friendly**: Use standard formatting and avoid graphics
5. **Quantify Results**: Include numbers and metrics where possible

### Job Applications
1. **Quality Over Quantity**: Focus on relevant positions
2. **Customize Applications**: Tailor each application to the specific job
3. **Review Before Applying**: Always review auto-generated content
4. **Follow Up**: Track applications and follow up appropriately
5. **Maintain Records**: Keep detailed records of all applications

### Platform Usage
1. **Respect Rate Limits**: Don't exceed platform limits
2. **Use Real Information**: Provide accurate and truthful information
3. **Professional Profiles**: Maintain professional social media presence
4. **Network Actively**: Engage with industry professionals
5. **Stay Updated**: Keep profiles and resumes current

## Security Considerations

### Credential Management
- Store credentials securely in .env file
- Never commit credentials to version control
- Use environment-specific configurations
- Rotate passwords regularly

### Data Privacy
- All data stored locally by default
- No data transmitted to external services (except AI model)
- Resume content processed locally
- Application data encrypted in database

### Platform Compliance
- Follow platform terms of service
- Respect rate limits and usage policies
- Use legitimate automation practices
- Maintain professional conduct

## Contributing

### Development Setup
1. Fork the repository
2. Create virtual environment
3. Install development dependencies
4. Run tests: `python test_system.py`
5. Submit pull requests

### Code Structure
- `src/` - Core application modules
- `data/` - Data storage
- `logs/` - Application logs
- `templates/` - HTML templates
- `static/` - Static assets

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Disclaimer**: This software is provided as-is for educational and personal use. Users are responsible for compliance with platform terms of service and applicable laws. The developers are not responsible for any misuse or consequences of using this software.
