# Advanced Usage Guide

This guide covers advanced features and usage patterns for the AI Job Hunt system.

## Custom Resume Templates

### Creating LaTeX Templates

You can create custom LaTeX templates in the `data/templates/latex/` directory. The system uses a template-based approach to generate LaTeX documents.

1. Create a new template file (e.g., `modern.tex`) in the `data/templates/latex/` directory
2. Use the following placeholders in your template:
   - `{{name}}` - Candidate name
   - `{{email}}` - Email address
   - `{{phone}}` - Phone number
   - `{{linkedin}}` - LinkedIn URL
   - `{{summary}}` - Professional summary
   - `{{skills}}` - List of skills
   - `{{experience}}` - Work experience
   - `{{education}}` - Education details
   - `{{projects}}` - Projects
   - `{{certifications}}` - Certifications

Example template snippet:

```latex
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\usepackage{multicol}
\setlength{\multicolsep}{-3.0pt}
\setlength{\columnsep}{-1pt}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.6in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.19in}
\addtolength{\topmargin}{-.7in}
\addtolength{\textheight}{1.4in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

\begin{center}
    \textbf{\Huge \scshape {{name}}} \\ \vspace{1pt}
    \small {{phone}} $|$ \href{mailto:{{email}}}{{\underline{{email}}}} $|$ 
    \href{https://linkedin.com/in/{{linkedin}}}{{\underline{linkedin.com/in/{{linkedin}}}}}
\end{center}

\section{Summary}
{{summary}}

\section{Skills}
\resumeSubHeadingListStart
\resumeSubItem{
    \textbf{Languages}{: {{skills.languages}}}
}
\resumeSubItem{
    \textbf{Frameworks}{: {{skills.frameworks}}}
}
\resumeSubItem{
    \textbf{Tools}{: {{skills.tools}}}
}
\resumeSubHeadingListEnd

% ... rest of the template
```

3. To use the custom template, specify it when generating a resume:
   ```python
   from backend.services.resume_parser import ResumeParser
   from backend.services.application_engine import ApplicationEngine
   
   resume_parser = ResumeParser()
   application_engine = ApplicationEngine()
   
   # Parse resume
   resume_data = resume_parser.parse("path/to/resume.pdf")
   
   # Generate optimized resume with custom template
   optimized_resume = application_engine.optimize_resume(
       resume_data=resume_data,
       job_id="job_123",
       template="modern"  # Specify your custom template name
   )
   ```

## API Integration

### Using the API Programmatically

You can integrate the AI Job Hunt system into your own applications using the API:

```python
import requests
import json

API_URL = "http://localhost:8000/api"

# Upload and parse a resume
def upload_resume(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_URL}/resumes/upload", files=files)
    return response.json()

# Analyze a job description
def analyze_job(job_description):
    data = {"job_description": job_description}
    response = requests.post(f"{API_URL}/jobs/analyze", json=data)
    return response.json()

# Optimize a resume for a job
def optimize_resume(resume_id, job_id):
    data = {
        "resume_id": resume_id,
        "job_id": job_id,
        "optimization_level": "balanced"
    }
    response = requests.post(f"{API_URL}/applications/optimize", json=data)
    return response.json()

# Example usage
resume_data = upload_resume("path/to/resume.pdf")
job_data = analyze_job("Job description text...")
application = optimize_resume(resume_data["resume_id"], job_data["job_id"])
```

## Advanced Configuration

### Custom LLM Providers

You can configure the system to use different LLM providers by modifying the `backend/config/settings.py` file:

```python
# Example for using Anthropic Claude
LLM_PROVIDER = "anthropic"
LLM_MODEL = "claude-3-opus-20240229"
ANTHROPIC_API_KEY = "your-api-key"
```

Then, update the `backend/services/llm_service.py` file to handle the new provider:

```python
def get_completion(self, prompt, max_tokens=1000):
    if self.provider == "ollama":
        # Existing Ollama code
        ...
    elif self.provider == "openai":
        # Existing OpenAI code
        ...
    elif self.provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    else:
        raise ValueError(f"Unsupported LLM provider: {self.provider}")
```

### Custom Job Scrapers

You can create custom job scrapers by extending the base `JobScraper` class:

```python
from backend.services.job_scraper import JobScraper

class CustomJobScraper(JobScraper):
    def __init__(self, settings):
        super().__init__(settings)
        # Custom initialization
        
    def search_jobs(self, query, location, max_results=10):
        # Custom implementation to search for jobs
        jobs = []
        # ... your implementation ...
        return jobs
        
    def extract_job_details(self, job_url):
        # Custom implementation to extract job details
        details = {}
        # ... your implementation ...
        return details
```

Register your custom scraper in `backend/services/job_scraper.py`:

```python
def get_scraper(self, platform):
    if platform == "linkedin":
        return LinkedInScraper(self.settings)
    elif platform == "indeed":
        return IndeedScraper(self.settings)
    elif platform == "custom":
        return CustomJobScraper(self.settings)
    else:
        raise ValueError(f"Unsupported platform: {platform}")
```

## Batch Processing

### Processing Multiple Resumes and Jobs

You can batch process multiple resumes and jobs using the backend API or directly with the services:

```python
from backend.services.db_manager import DBManager
from backend.services.resume_parser import ResumeParser
from backend.services.application_engine import ApplicationEngine

db = DBManager()
parser = ResumeParser()
engine = ApplicationEngine()

# Parse multiple resumes
resume_files = ["resume1.pdf", "resume2.pdf", "resume3.pdf"]
resume_ids = []

for file in resume_files:
    resume_data = parser.parse(file)
    resume_id = db.save_resume(resume_data)
    resume_ids.append(resume_id)

# Analyze multiple job descriptions
job_files = ["job1.txt", "job2.txt", "job3.txt"]
job_ids = []

for file in job_files:
    with open(file, 'r') as f:
        job_description = f.read()
    job_analysis = engine.analyze_job(job_description)
    job_id = db.save_job(job_analysis)
    job_ids.append(job_id)

# Create optimized applications for all combinations
for resume_id in resume_ids:
    for job_id in job_ids:
        application = engine.optimize_resume(
            resume_id=resume_id,
            job_id=job_id
        )
        db.save_application(application)
```

## Performance Optimization

### Caching LLM Responses

For improved performance, you can implement caching for LLM responses:

```python
from functools import lru_cache
import hashlib

class CachedLLMService:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        
    @lru_cache(maxsize=100)
    def get_cached_completion(self, prompt_hash):
        # This function is cached
        prompt = self.hash_to_prompt_map.get(prompt_hash)
        return self.llm_service.get_completion(prompt)
        
    def get_completion(self, prompt, max_tokens=1000):
        # Hash the prompt to use as a cache key
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        # Store the mapping of hash to actual prompt
        if not hasattr(self, 'hash_to_prompt_map'):
            self.hash_to_prompt_map = {}
        self.hash_to_prompt_map[prompt_hash] = prompt
        
        # Use the cached function
        return self.get_cached_completion(prompt_hash)
```

Update the LLM service initialization in your application:

```python
from backend.services.llm_service import LLMService

# Create the base LLM service
llm_service = LLMService()

# Wrap it with caching
cached_llm_service = CachedLLMService(llm_service)

# Use the cached service
response = cached_llm_service.get_completion("Your prompt here")
```

## Advanced Testing

### Automated Testing with Pytest

The project includes a pytest setup for automated testing. You can run tests with:

```bash
pytest backend/tests/
```

To write new tests, create files in the `backend/tests/` directory:

```python
# backend/tests/test_custom_feature.py
import pytest
from backend.services.your_service import YourService

def test_your_feature():
    # Setup
    service = YourService()
    
    # Execute
    result = service.your_method()
    
    # Assert
    assert result == expected_value
```

### Performance Testing

For performance testing, you can use the built-in timing utilities:

```python
import time
from backend.utils.logger import get_logger

logger = get_logger(__name__)

def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
    return result, execution_time

# Example usage
result, time_taken = measure_performance(
    llm_service.get_completion, 
    "Your prompt here"
)
```
