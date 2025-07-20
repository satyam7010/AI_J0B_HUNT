# AI Job Hunt Examples

This directory contains example scripts and usage patterns for the AI Job Hunt system.

## Available Examples

1. `example_usage.py` - Demonstrates basic usage of the AI Job Hunt system
2. `generate_latex_resume.py` - Shows how to generate LaTeX resumes using the system

## Running the Examples

To run an example:

```bash
cd AI_JOB_HUNT
python -m backend.examples.example_usage
python -m backend.examples.generate_latex_resume --resume path/to/resume.pdf --job path/to/job_description.txt
```

## Example Workflow

The `example_usage.py` file demonstrates a basic workflow:

```python
# Import from the backend
from backend.services.resume_parser import ResumeParser
from backend.services.llm_service import LLMService
from backend.agents.resume_optimizer_agent import ResumeOptimizerAgent

# Basic workflow example
def example_workflow():
    # Initialize services
    resume_parser = ResumeParser()
    llm_service = LLMService()
    optimizer = ResumeOptimizerAgent(llm_service)
    
    # Parse a resume
    resume_data = resume_parser.parse("../data/examples/sample_resume.txt")
    
    # Load a job description
    with open("../data/examples/sample_job_description.txt", "r") as f:
        job_description = f.read()
    
    # Optimize the resume
    optimized_resume = optimizer.optimize(resume_data, job_description)
    
    # Print the results
    print("Original Resume:")
    print(resume_data)
    print("\nOptimized Resume:")
    print(optimized_resume)
    
if __name__ == "__main__":
    example_workflow()
```

## Available Services

The following services are available for use in your examples:

- `backend.services.resume_parser.ResumeParser` - Parse resumes from various formats
- `backend.services.llm_service.LLMService` - Interact with the LLM (Gemma 3.4b via Ollama)
- `backend.services.job_scraper.JobScraper` - Scrape job listings from various platforms
- `backend.services.db_manager.DBManager` - Interact with the database
- `backend.services.application_engine.ApplicationEngine` - Core application engine

## Available Agents

The following agents are available for use in your examples:

- `backend.agents.resume_optimizer_agent.ResumeOptimizerAgent` - Optimize resumes for specific jobs
- `backend.agents.job_description_agent.JobDescriptionAgent` - Analyze job descriptions
- `backend.agents.application_agent.ApplicationAgent` - Manage job applications

## Example Data

Example data files are available in the `data/examples/` directory:

- `sample_resume.txt` - A sample resume
- `sample_job_description.txt` - A sample job description
