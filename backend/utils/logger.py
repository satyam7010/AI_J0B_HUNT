"""
Logging utility for AI Job Hunt system
"""

import os
import logging
from pathlib import Path
from typing import Optional

def setup_logger(
    logger_name: Optional[str] = None,
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        logger_name: Name of the logger (defaults to __name__ of caller)
        log_level: Logging level (defaults to env var LOG_LEVEL or INFO)
        log_file: Path to log file (defaults to env var LOG_FILE or logs/application.log)
        
    Returns:
        Configured logger instance
    """
    # Set defaults from environment variables
    log_level = log_level or os.getenv('LOG_LEVEL', 'INFO')
    log_file = log_file or os.getenv('LOG_FILE', 'logs/application.log')
    
    # Create logs directory if it doesn't exist
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Get the appropriate logger (or root logger if None)
    logger = logging.getLogger(logger_name)
    
    # Only configure if handlers haven't been set up
    if not logger.handlers:
        logger.setLevel(getattr(logging, log_level))
        
        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Set formatter for handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
