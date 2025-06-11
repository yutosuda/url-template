"""
Validation utilities for URL shortener.
"""
import re
from urllib.parse import urlparse
from typing import Optional


def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_safe_url(url: str) -> bool:
    """
    Check if URL is safe (not pointing to localhost or private networks).
    
    Args:
        url: URL string to check
        
    Returns:
        True if safe URL, False otherwise
    """
    if not is_valid_url(url):
        return False
    
    parsed = urlparse(url)
    hostname = parsed.hostname
    
    if not hostname:
        return False
    
    # Block localhost and private networks
    blocked_patterns = [
        r'^localhost$',
        r'^127\.',
        r'^10\.',
        r'^172\.(1[6-9]|2[0-9]|3[01])\.',
        r'^192\.168\.',
        r'^0\.',
        r'^169\.254\.',
        r'^::1$',
        r'^fc00:',
        r'^fe80:',
    ]
    
    for pattern in blocked_patterns:
        if re.match(pattern, hostname, re.IGNORECASE):
            return False
    
    return True


def validate_short_code(short_code: str) -> bool:
    """
    Validate short code format.
    
    Args:
        short_code: Short code to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not short_code:
        return False
    
    # Allow alphanumeric characters and some safe symbols
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, short_code)) and len(short_code) <= 20 