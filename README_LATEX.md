# LaTeX Resume Generator

This tool generates optimized LaTeX resumes tailored for specific job descriptions using AI. It leverages the power of LLMs to analyze job requirements and create a targeted resume in LaTeX format.

## Prerequisites

- Python 3.8+
- LaTeX installation (for PDF compilation)
- Required Python packages (install via `pip install -r requirements.txt`)
- Ollama or OpenAI API access (configured in `.env` file)

## Usage

### 1. Prepare Your Input Files

- Place your resume text in a file (e.g., `data/examples/sample_resume.txt`)
- Save the job description in a file (e.g., `data/examples/sample_job_description.txt`)

### 2. Generate LaTeX Resume

Run the following command:

```bash
python generate_latex_resume.py data/examples/sample_resume.txt data/examples/sample_job_description.txt
```

Additional options:
- `--output-dir`: Specify custom output directory (default: `data/resumes/latex`)
- `--optimization-level`: Choose from "conservative", "balanced", or "aggressive" (default: "balanced")

Example with options:
```bash
python generate_latex_resume.py data/examples/sample_resume.txt data/examples/sample_job_description.txt --output-dir ./my_resume --optimization-level aggressive
```

### 3. Review and Compile

The script will:
1. Generate LaTeX content for different resume sections
2. Save these sections in the `src/` subdirectory of the output folder
3. Copy template files if they don't exist
4. Optionally compile the resume to PDF (if `auto_compile_latex` is enabled in settings)

If auto-compilation is disabled, you can compile manually:
```bash
cd <output_directory>
latexmk -pdf main.tex
```

## Configuration

Configuration options are available in the `backend/config/settings.py` file:

- `resume.output_dir`: Default output directory for LaTeX files
- `resume.auto_compile_latex`: Whether to automatically compile the LaTeX to PDF
- `resume.latex_template_dir`: Directory containing LaTeX template files

## LaTeX Template Structure

The LaTeX template uses the following structure:

- `main.tex`: Main LaTeX document with document class, packages, and structure
- `src/profile.tex`: Profile/summary section
- `src/experience.tex`: Work experience section
- `src/projects.tex`: Projects section
- `src/education.tex`: Education section
- `src/skills.tex`: Skills section

## Customization

To customize the LaTeX template:
1. Modify the template files in `data/templates/latex/`
2. Update the prompt in `backend/prompts/resume_prompts.py` to match your LaTeX structure

## Troubleshooting

If you encounter issues:
1. Check the application logs in `logs/application.log`
2. Ensure LaTeX is properly installed on your system
3. Verify that the template files exist and are correctly formatted
4. Check that the LLM service (Ollama or OpenAI) is configured properly
