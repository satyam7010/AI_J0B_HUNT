"""
Automation helpers for AI Job Hunt system
"""

import os
import time
import random
from typing import Dict, List, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

def add_human_delay(min_seconds: float = 0.5, max_seconds: float = 3.0) -> None:
    """
    Add a random delay to simulate human interaction
    
    Args:
        min_seconds: Minimum delay in seconds
        max_seconds: Maximum delay in seconds
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def retry_operation(
    operation: Callable,
    max_attempts: int = 3,
    retry_delay: float = 2.0,
    backoff_factor: float = 1.5,
    exceptions_to_catch: tuple = (Exception,),
    retry_message: Optional[str] = None
) -> Any:
    """
    Retry an operation with exponential backoff
    
    Args:
        operation: Function to retry
        max_attempts: Maximum number of retry attempts
        retry_delay: Initial delay between retries in seconds
        backoff_factor: Factor by which to increase delay after each failure
        exceptions_to_catch: Tuple of exceptions that should trigger a retry
        retry_message: Custom message to log on retry (defaults to generic message)
        
    Returns:
        The result of the operation if successful
        
    Raises:
        The last exception encountered if all attempts fail
    """
    attempt = 1
    last_exception = None
    
    while attempt <= max_attempts:
        try:
            return operation()
        except exceptions_to_catch as e:
            last_exception = e
            
            if attempt < max_attempts:
                message = retry_message or f"Operation failed: {str(e)}. Retrying ({attempt}/{max_attempts})..."
                logger.warning(message)
                
                # Calculate delay with exponential backoff
                current_delay = retry_delay * (backoff_factor ** (attempt - 1))
                time.sleep(current_delay)
                
                attempt += 1
            else:
                logger.error(f"Operation failed after {max_attempts} attempts: {str(e)}")
                break
    
    # If we got here, all attempts failed
    raise last_exception

def parse_boolean_env(env_var: str, default: bool = False) -> bool:
    """
    Parse a boolean environment variable
    
    Args:
        env_var: Name of the environment variable
        default: Default value if env var is not set
        
    Returns:
        Boolean value of the environment variable
    """
    value = os.getenv(env_var)
    if value is None:
        return default
        
    # Check for common true/false values
    return value.lower() in ('true', 'yes', '1', 'y', 'on')
