"""
File utility functions for AI Job Hunt system
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Union, Optional
import logging

logger = logging.getLogger(__name__)

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
    
    # Create the backup
    try:
        shutil.copy2(source_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Error creating backup of {file_path}: {str(e)}")
        raise
