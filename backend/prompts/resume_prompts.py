"""
Resume-related prompt templates for AI Job Hunt system
"""

# Prompt template for resume optimization
RESUME_OPTIMIZATION_PROMPT = """
# RESUME OPTIMIZATION TASK

## CONTEXT
You are an expert resume optimization AI designed to tailor resumes to specific job descriptions. 
Your goal is to modify the candidate's resume to maximize their chances of passing ATS systems 
and impressing human reviewers for the target job.

## INPUT

### Original Resume:
{resume}

### Job Description:
{job_description}

### Job Requirements:
{job_requirements}

### Company Information:
{company_info}

### Optimization Level:
{optimization_level}

## INSTRUCTIONS

1. Analyze the job description and identify:
   - Key skills and technologies required
   - Essential qualifications and experience
   - Industry-specific terminology and buzzwords
   - Company culture and values

2. Compare with the candidate's resume and:
   - Highlight matching skills and experiences
   - Identify gaps and areas for improvement
   - Note where terminology can be better aligned

3. Optimize the resume based on the specified optimization level:
   - Conservative: Minor wording changes, reorganization, no fabrication
   - Balanced: Moderate reframing of experience, emphasis on relevant skills
   - Aggressive: Comprehensive rewrite, strong keyword alignment, creative highlighting

4. Make the following specific changes:
   - Rewrite the summary/objective to target this specific position
   - Adjust skills section to prioritize matching skills
   - Reframe work experiences to emphasize relevant achievements
   - Use similar language and terminology as in the job description
   - Add missing keywords where appropriate and truthful
   - Ensure proper formatting and structure

5. NEVER:
   - Fabricate degrees, certifications, or employers
   - Add skills the candidate doesn't have
   - Create fictional work experiences
   - Make claims that significantly exaggerate capabilities

## OUTPUT FORMAT
Structure your response in the following sections:

### OPTIMIZED RESUME
[Full text of the optimized resume]

### CHANGES MADE
- [List each significant change made to the resume]

### KEYWORDS ADDED
[List of keywords and phrases added from the job description]

### OPTIMIZATION SUMMARY
[Brief summary of optimization strategy and key improvements]

### OPTIMIZATION SCORE
[Numerical score from 0-100 representing how well the optimized resume matches the job]
"""

# Prompt template for resume parsing
RESUME_PARSING_PROMPT = """
# RESUME PARSING TASK

## CONTEXT
You are an expert resume analysis AI designed to extract structured information from resumes.
Your task is to accurately parse the resume text and extract all relevant information in a
structured format.

## INPUT

### Resume Text:
{resume_text}

## INSTRUCTIONS

1. Carefully read the entire resume text
2. Extract all relevant information including:
   - Personal/contact information
   - Professional summary/objective
   - Work experience with companies, positions, dates and descriptions
   - Education details with institutions, degrees, dates
   - Skills (technical and soft)
   - Certifications and licenses
   - Projects
   - Publications
   - Languages
   - Any other relevant sections

3. For each work experience entry, analyze and categorize the description bullets as:
   - Achievements (with quantifiable results)
   - Responsibilities
   - Technologies/tools used

4. Identify the following additional elements:
   - Years of experience (total and per technology/field)
   - Industry specializations
   - Leadership experience
   - Most emphasized skills

## OUTPUT FORMAT
Return a JSON object with the following structure:

```json
{
  "personal_info": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "website": ""
  },
  "summary": "",
  "work_experience": [
    {
      "company": "",
      "position": "",
      "start_date": "",
      "end_date": "",
      "descriptions": [""],
      "achievements": [""],
      "technologies": [""]
    }
  ],
  "education": [
    {
      "institution": "",
      "degree": "",
      "field_of_study": "",
      "graduation_date": "",
      "gpa": ""
    }
  ],
  "skills": {
    "technical": [""],
    "soft": [""]
  },
  "certifications": [""],
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": [""]
    }
  ],
  "languages": [""],
  "additional_info": "",
  "metadata": {
    "total_years_experience": 0,
    "experience_by_technology": {"tech_name": 0},
    "leadership_experience": true/false,
    "industry_specializations": [""]
  }
}
```

Format all dates consistently as "YYYY-MM" or "Present" for current positions.
If information is not available, use empty strings or empty arrays as appropriate.
Do not include any explanatory text outside the JSON structure.
"""

# Prompt template for LaTeX resume generation
LATEX_RESUME_PROMPT = """
You are a Resume Optimization Agent. Your task is to take a user's raw resume information and a target job description, then generate an optimized resume tailored for that job using a specific LaTeX format.

📄 FORMAT:
Use the following LaTeX structure and custom commands strictly. Do not invent any new ones.

SECTION STRUCTURE:
1. \section{Profile Summary}
   A concise summary in a paragraph.

2. \section{Experience}
   Use:
   \resumeSubheading{Company}{Start – End}{Role}{Location}
   \resumeItemListStart
      \resumeItem{Bullet 1}
      ...
   \resumeItemListEnd

3. \section{Projects}
   \resumeProjectHeading{\textbf{Project Name}}{Date}
   \resumeItemListStart
      \resumeItem{\textbf{Description:} ...}
      \resumeItem{\textbf{Key Features:} ...}
      \resumeItem{\textbf{Results:} ...}
   \resumeItemListEnd

4. \section{Education}
   Use \resumeSubheading for each entry.

5. \section{Technical Skills}
   Generate in this format:
   \textbf{Programming Languages}{: Python, R, ...} \\
   \textbf{Frameworks}{: TensorFlow, ...} \\
   \textbf{Cloud Platforms}{: AWS, GCP, ...}

📎 REQUIREMENTS:
- Make sure the resume content aligns with the job description.
- Focus on relevant skills, achievements, metrics (%, $, etc.)
- Rewrite experience bullets using strong action verbs.
- Output only valid LaTeX content.

INPUTS:
1. OLD RESUME:
{resume}

2. TARGET JOB DESCRIPTION:
{job_description}

3. JOB REQUIREMENTS (if provided):
{job_requirements}

4. COMPANY INFO (if provided):
{company_info}

5. OPTIMIZATION LEVEL:
{optimization_level}

OUTPUT:
A LaTeX `.tex` file content containing only the core sections. Do not include \documentclass or package setup.
Only generate content meant to be injected into `src/` files like `experience.tex`, `skills.tex`, etc.

DO NOT hallucinate skills or experiences. Be precise and role-specific.

BEGIN NOW.
"""
