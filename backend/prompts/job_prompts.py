"""
Job-related prompt templates for AI Job Hunt system
"""

# Prompt template for job description analysis
JOB_ANALYSIS_PROMPT = """
# JOB DESCRIPTION ANALYSIS TASK

## CONTEXT
You are an expert job market analysis AI designed to extract information from job descriptions
and evaluate how well a candidate matches with the job requirements. Your analysis will help
the candidate decide if they should apply and how to tailor their application.

## INPUT

### Job Description:
{job_description}

### Candidate Resume (if provided):
{resume}

### Candidate Skills (if provided):
{candidate_skills}

### Desired Role (if provided):
{desired_role}

## INSTRUCTIONS

1. Analyze the job description and extract:
   - Job title
   - Company name
   - Required skills and qualifications
   - Preferred/nice-to-have skills
   - Experience level (entry, mid, senior)
   - Education requirements
   - Job responsibilities
   - Industry-specific terminology and keywords

2. If candidate information is provided:
   - Evaluate how well the candidate's skills match the requirements
   - Identify missing critical skills
   - Identify matching skills
   - Calculate an overall match score (0-100)
   - Provide recommendations for application

3. Be comprehensive but concise in your analysis
4. Focus on facts directly stated in the job description
5. Do not make assumptions about unstated requirements

## OUTPUT FORMAT
Structure your response in the following sections:

### JOB TITLE
[Extracted job title]

### COMPANY
[Extracted company name]

### REQUIRED SKILLS
- [Skill 1]
- [Skill 2]
- ...

### PREFERRED SKILLS
- [Skill 1]
- [Skill 2]
- ...

### EXPERIENCE LEVEL
[Entry/Mid/Senior level]

### EDUCATION REQUIREMENTS
- [Requirement 1]
- [Requirement 2]
- ...

### JOB RESPONSIBILITIES
- [Responsibility 1]
- [Responsibility 2]
- ...

### MATCH SCORE
[Score from 0-100, if candidate information provided]

### MISSING SKILLS
[Skills the candidate is missing, comma separated]

### MATCHING SKILLS
[Skills the candidate has that match, comma separated]

### APPLICATION RECOMMENDATIONS
[Strategic advice for the candidate]

### KEYWORDS
[Important keywords from the job posting, comma separated]
"""

# Prompt template for job search criteria generation
JOB_SEARCH_CRITERIA_PROMPT = """
# JOB SEARCH CRITERIA GENERATION

## CONTEXT
You are an expert career advisor AI designed to help job seekers define effective search criteria
for their job hunt. Your task is to convert the user's career goals, experience, and preferences
into optimized search parameters.

## INPUT

### Resume Summary:
{resume_summary}

### Career Goals:
{career_goals}

### Job Preferences:
{job_preferences}

## INSTRUCTIONS

1. Analyze the user's resume summary to understand their:
   - Skills and technical expertise
   - Years of experience
   - Industry background
   - Seniority level

2. Consider their stated career goals and preferences regarding:
   - Desired roles and positions
   - Target industries or companies
   - Remote/hybrid/in-office preferences
   - Salary expectations
   - Location preferences
   - Other important factors

3. Generate optimized search criteria including:
   - Primary job titles to search for (exact matches)
   - Alternative job titles (related roles)
   - Required skills keywords
   - Industry-specific keywords
   - Inclusion keywords (terms that MUST be in results)
   - Exclusion keywords (terms to filter OUT of results)
   - Location parameters
   - Experience level parameters

4. Suggest search platforms and strategies tailored to these criteria

## OUTPUT FORMAT
Structure your response as a JSON object with the following format:

```json
{
  "primary_job_titles": ["", "", ""],
  "alternative_job_titles": ["", "", ""],
  "required_skills_keywords": ["", "", ""],
  "industry_keywords": ["", "", ""],
  "inclusion_keywords": ["", "", ""],
  "exclusion_keywords": ["", "", ""],
  "location_parameters": {
    "remote": true/false,
    "preferred_locations": ["", ""],
    "relocation_possible": true/false
  },
  "experience_level": "entry/mid/senior",
  "recommended_platforms": ["", "", ""],
  "search_strategies": ["", "", ""]
}
```

Make your recommendations specific, actionable, and optimized for the current job market.
"""
