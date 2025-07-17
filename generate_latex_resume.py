#!/usr/bin/env python3
"""
Example script to demonstrate LaTeX resume generation functionality
"""

import os
import asyncio
import argparse
from pathlib import Path

from backend.agents.resume_optimizer_agent import ResumeOptimizerAgent
from backend.config.settings import settings
from backend.utils.file_utils import ensure_directory


async def generate_latex_resume(
    resume_file: str,
    job_description_file: str,
    output_dir: str = None,
    optimization_level: str = "balanced"
):
    """
    Generate a LaTeX resume from input files
    
    Args:
        resume_file: Path to the resume text file
        job_description_file: Path to the job description text file
        output_dir: Directory to save LaTeX output (optional)
        optimization_level: Level of optimization (conservative, balanced, aggressive)
    """
    # Use default output directory if not specified
    if not output_dir:
        output_dir = str(settings.resume.output_dir)
    
    # Ensure output directory exists
    ensure_directory(output_dir)
    
    # Read input files
    with open(resume_file, "r", encoding="utf-8") as f:
        resume_text = f.read()
    
    with open(job_description_file, "r", encoding="utf-8") as f:
        job_description = f.read()
    
    # Create resume optimizer agent
    agent = ResumeOptimizerAgent()
    
    # Generate LaTeX resume
    print(f"Generating LaTeX resume with {optimization_level} optimization level...")
    latex_sections = await agent.generate_latex_resume(
        resume_text=resume_text,
        job_description=job_description,
        optimization_level=optimization_level,
        output_dir=output_dir
    )
    
    print(f"LaTeX resume sections generated and saved to {output_dir}/src/")
    
    # Copy template files if they don't exist in the output directory
    template_dir = settings.resume.latex_template_dir
    if os.path.exists(template_dir):
        main_tex_path = os.path.join(output_dir, "main.tex")
        if not os.path.exists(main_tex_path):
            print(f"Copying LaTeX template files from {template_dir} to {output_dir}...")
            import shutil
            for file in os.listdir(template_dir):
                src_file = os.path.join(template_dir, file)
                dst_file = os.path.join(output_dir, file)
                if os.path.isfile(src_file) and not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
    
    # Compile LaTeX if enabled
    if settings.resume.auto_compile_latex:
        print("Compiling LaTeX resume...")
        success = agent._compile_latex(output_dir)
        if success:
            pdf_path = os.path.join(output_dir, "main.pdf")
            print(f"Resume compiled successfully. PDF available at: {pdf_path}")
        else:
            print("LaTeX compilation failed. Check logs for details.")
    else:
        print(f"Auto-compilation is disabled. To compile manually, run: cd {output_dir} && latexmk -pdf main.tex")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a LaTeX resume from a text resume and job description")
    parser.add_argument("resume", help="Path to the resume text file")
    parser.add_argument("job_description", help="Path to the job description text file")
    parser.add_argument("--output-dir", help="Directory to save LaTeX output")
    parser.add_argument("--optimization-level", choices=["conservative", "balanced", "aggressive"], 
                        default="balanced", help="Level of optimization")
    
    args = parser.parse_args()
    
    asyncio.run(generate_latex_resume(
        resume_file=args.resume,
        job_description_file=args.job_description,
        output_dir=args.output_dir,
        optimization_level=args.optimization_level
    ))
