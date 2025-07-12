"""
Configuration Validators
Validation functions for configuration settings
"""

import re
import os
from pathlib import Path
from typing import Any, List, Tuple, Optional
from urllib.parse import urlparse


class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


def validate_url(url: str, schemes: List[str] = None) -> bool:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        schemes: Allowed URL schemes (default: ['http', 'https'])
    
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If URL is invalid
    """
    if not url:
        raise ConfigValidationError("URL cannot be empty")
    
    schemes = schemes or ['http', 'https']
    
    try:
        parsed = urlparse(url)
        if parsed.scheme not in schemes:
            raise ConfigValidationError(f"URL scheme must be one of {schemes}, got: {parsed.scheme}")
        if not parsed.netloc:
            raise ConfigValidationError("URL must have a valid hostname")
        return True
    except Exception as e:
        if isinstance(e, ConfigValidationError):
            raise
        raise ConfigValidationError(f"Invalid URL format: {e}")


def validate_supabase_key(key: str) -> bool:
    """
    Validate Supabase API key format
    
    Args:
        key: Supabase API key
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If key is invalid
    """
    if not key:
        raise ConfigValidationError("Supabase key cannot be empty")
    
    # Supabase keys are typically JWT tokens or have specific prefixes
    if len(key) < 20:
        raise ConfigValidationError("Supabase key appears too short")
    
    # Check for common Supabase key patterns
    valid_patterns = [
        r'^eyJ',  # JWT token
        r'^sb-',  # Supabase service key prefix
    ]
    
    if not any(re.match(pattern, key) for pattern in valid_patterns):
        raise ConfigValidationError("Supabase key format appears invalid")
    
    return True


def validate_file_path(path: str, must_exist: bool = False, must_be_writable: bool = False) -> bool:
    """
    Validate file path
    
    Args:
        path: File path to validate
        must_exist: Whether file must already exist
        must_be_writable: Whether path must be writable
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If path is invalid
    """
    if not path:
        raise ConfigValidationError("File path cannot be empty")
    
    path_obj = Path(path)
    
    if must_exist and not path_obj.exists():
        raise ConfigValidationError(f"Path does not exist: {path}")
    
    if must_be_writable:
        # Check if directory is writable
        parent_dir = path_obj.parent
        if not parent_dir.exists():
            try:
                parent_dir.mkdir(parents=True)
            except PermissionError:
                raise ConfigValidationError(f"Cannot create directory: {parent_dir}")
        
        if not os.access(parent_dir, os.W_OK):
            raise ConfigValidationError(f"Directory not writable: {parent_dir}")
    
    return True


def validate_log_level(level: str) -> bool:
    """
    Validate logging level
    
    Args:
        level: Logging level string
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If level is invalid
    """
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    
    if level.upper() not in valid_levels:
        raise ConfigValidationError(f"Log level must be one of {valid_levels}, got: {level}")
    
    return True


def validate_positive_integer(value: Any, name: str, min_value: int = 1) -> bool:
    """
    Validate positive integer
    
    Args:
        value: Value to validate
        name: Name of the setting (for error messages)
        min_value: Minimum allowed value
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If value is invalid
    """
    try:
        int_value = int(value)
        if int_value < min_value:
            raise ConfigValidationError(f"{name} must be >= {min_value}, got: {int_value}")
        return True
    except (ValueError, TypeError):
        raise ConfigValidationError(f"{name} must be a valid integer, got: {value}")


def validate_file_size(size: Any, name: str = "File size") -> bool:
    """
    Validate file size in bytes
    
    Args:
        size: Size value to validate
        name: Name of the setting
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If size is invalid
    """
    max_size = 1024 * 1024 * 1024  # 1GB
    
    try:
        size_bytes = int(size)
        if size_bytes <= 0:
            raise ConfigValidationError(f"{name} must be positive, got: {size_bytes}")
        if size_bytes > max_size:
            raise ConfigValidationError(f"{name} too large (max 1GB), got: {size_bytes}")
        return True
    except (ValueError, TypeError):
        raise ConfigValidationError(f"{name} must be a valid integer, got: {size}")


def validate_environment(env: str) -> bool:
    """
    Validate environment name
    
    Args:
        env: Environment name
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If environment is invalid
    """
    valid_environments = ['development', 'staging', 'production', 'testing']
    
    if env not in valid_environments:
        raise ConfigValidationError(f"Environment must be one of {valid_environments}, got: {env}")
    
    return True


def validate_embedding_model(model: str) -> bool:
    """
    Validate embedding model name
    
    Args:
        model: Model name
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If model name is invalid
    """
    if not model:
        raise ConfigValidationError("Embedding model name cannot be empty")
    
    # Common valid model patterns
    valid_patterns = [
        r'^all-MiniLM-L\d+-v\d+$',  # all-MiniLM models
        r'^sentence-transformers/',  # HuggingFace sentence-transformers
        r'^multi-qa-',  # Multi-QA models
        r'^paraphrase-',  # Paraphrase models
        r'^distilbert-',  # DistilBERT models
    ]
    
    # Allow some flexibility for custom models
    if len(model) < 3:
        raise ConfigValidationError("Embedding model name too short")
    
    return True


def validate_device(device: str) -> bool:
    """
    Validate compute device
    
    Args:
        device: Device name (cpu, cuda, mps, etc.)
        
    Returns:
        True if valid
        
    Raises:
        ConfigValidationError: If device is invalid
    """
    valid_devices = ['cpu', 'cuda', 'mps', 'auto']
    
    # Allow cuda:0, cuda:1, etc.
    if device.startswith('cuda:'):
        try:
            int(device.split(':')[1])
            return True
        except (IndexError, ValueError):
            pass
    
    if device not in valid_devices:
        raise ConfigValidationError(f"Device must be one of {valid_devices} or 'cuda:N', got: {device}")
    
    return True


def validate_all_settings(settings_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate all configuration settings
    
    Args:
        settings_dict: Dictionary of settings to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required settings
    required_keys = ['SUPABASE_URL', 'SUPABASE_KEY']
    for key in required_keys:
        if key not in settings_dict or not settings_dict[key]:
            errors.append(f"Missing required setting: {key}")
    
    # Validate specific settings
    validators = [
        ('SUPABASE_URL', lambda: validate_url(settings_dict.get('SUPABASE_URL', ''))),
        ('SUPABASE_KEY', lambda: validate_supabase_key(settings_dict.get('SUPABASE_KEY', ''))),
        ('LOG_LEVEL', lambda: validate_log_level(settings_dict.get('LOG_LEVEL', 'INFO'))),
        ('ENVIRONMENT', lambda: validate_environment(settings_dict.get('ENVIRONMENT', 'development'))),
        ('EMBEDDING_MODEL', lambda: validate_embedding_model(settings_dict.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2'))),
        ('EMBEDDING_DEVICE', lambda: validate_device(settings_dict.get('EMBEDDING_DEVICE', 'cpu'))),
        ('DB_TIMEOUT', lambda: validate_positive_integer(settings_dict.get('DB_TIMEOUT', 30), 'DB_TIMEOUT')),
        ('DB_BATCH_SIZE', lambda: validate_positive_integer(settings_dict.get('DB_BATCH_SIZE', 10), 'DB_BATCH_SIZE')),
        ('MAX_FILE_SIZE', lambda: validate_file_size(settings_dict.get('MAX_FILE_SIZE', 50*1024*1024))),
    ]
    
    for key, validator in validators:
        try:
            validator()
        except ConfigValidationError as e:
            errors.append(f"{key}: {str(e)}")
        except Exception as e:
            errors.append(f"{key}: Unexpected validation error: {str(e)}")
    
    # Validate optional file paths
    if 'LOG_FILE_PATH' in settings_dict and settings_dict['LOG_FILE_PATH']:
        try:
            validate_file_path(settings_dict['LOG_FILE_PATH'], must_be_writable=True)
        except ConfigValidationError as e:
            errors.append(f"LOG_FILE_PATH: {str(e)}")
    
    if 'EMBEDDING_CACHE_DIR' in settings_dict and settings_dict['EMBEDDING_CACHE_DIR']:
        try:
            validate_file_path(settings_dict['EMBEDDING_CACHE_DIR'], must_be_writable=True)
        except ConfigValidationError as e:
            errors.append(f"EMBEDDING_CACHE_DIR: {str(e)}")
    
    return len(errors) == 0, errors