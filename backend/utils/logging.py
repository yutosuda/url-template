"""
Logging configuration and utilities.
"""
import logging
import sys
from typing import Optional

from config import settings


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup application logging configuration.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom log format string
        
    Returns:
        Configured logger instance
    """
    log_level = level or settings.log_level
    log_format = format_string or settings.log_format
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Get application logger
    logger = logging.getLogger("url_shortener")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"url_shortener.{name}") 