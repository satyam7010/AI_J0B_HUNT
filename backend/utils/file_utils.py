"""
File utility functions for AI Job Hunt system
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Union, Optional
import logging
import tempfile
from fastapi import UploadFile
import PyPDF2
import docx2txt

from utils.logger import setup_logger

logger = setup_logger(__name__)

def ensure_directory(directory_path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        Path object for the directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def save_json(data: Union[Dict, List], file_path: Union[str, Path]) -> None:
    """
    Save data to a JSON file
    
    Args:
        data: Data to save (must be JSON serializable)
        file_path: Path where the JSON file will be saved
    """
    path = Path(file_path)
    ensure_directory(path.parent)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {str(e)}")
        raise

def load_json(file_path: Union[str, Path]) -> Any:
    """
    Load data from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Loaded JSON data
    """
    path = Path(file_path)
    
    try:
        if not path.exists():
            logger.warning(f"JSON file does not exist: {file_path}")
            return None
            
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {str(e)}")
        raise

def backup_file(file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Path:
    """
    Create a backup of a file
    
    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store the backup (defaults to same directory with 'backups' subfolder)
        
    Returns:
        Path to the backup file
    """
    source_path = Path(file_path)
    
    if not source_path.exists():
        logger.warning(f"Cannot backup non-existent file: {file_path}")
        return None
    
    # Determine backup directory
    if backup_dir is None:
        backup_dir = source_path.parent / 'backups'
    
    backup_dir = Path(backup_dir)
    ensure_directory(backup_dir)
    
    # Create backup filename with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{source_path.stem}_{timestamp}{source_path.suffix}"
    backup_path = backup_dir / backup_filename
    
    # Copy the file
    try:
        shutil.copy2(source_path, backup_path)
        logger.info(f"Created backup of {source_path} at {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Error creating backup of {source_path}: {str(e)}")
        raise

async def save_upload_file_temp(upload_file: UploadFile) -> Path:
    """
    Save an uploaded file to a temporary location
    
    Args:
        upload_file: The uploaded file from FastAPI
        
    Returns:
        Path to the saved temporary file
    """
    try:
        suffix = Path(upload_file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            # Read from FastAPI's UploadFile
            contents = await upload_file.read()
            # Write to the temporary file
            temp_file.write(contents)
            temp_path = Path(temp_file.name)
        
        logger.info(f"Saved upload file temporarily to {temp_path}")
        return temp_path
    except Exception as e:
        logger.error(f"Error saving upload file: {str(e)}")
        raise

def extract_text_from_file(file_path: Union[str, Path]) -> str:
    """
    Extract text content from a file based on its type
    
    Args:
        file_path: Path to the file
        
    Returns:
        Extracted text content
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    try:
        if suffix == '.pdf':
            return _extract_text_from_pdf(path)
        elif suffix in ['.docx', '.doc']:
            return _extract_text_from_docx(path)
        elif suffix in ['.txt', '.md', '.csv']:
            return _extract_text_from_text_file(path)
        else:
            logger.warning(f"Unsupported file type for text extraction: {suffix}")
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        return ""

def _extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
        raise

def _extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file"""
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {file_path}: {str(e)}")
        raise

def _extract_text_from_text_file(file_path: Path) -> str:
    """Extract text from a plain text file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {str(e)}")
        raise
