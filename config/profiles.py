"""
Configuration Profiles
Pre-defined configuration profiles for different environments
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class ConfigProfile:
    """Configuration profile definition"""
    name: str
    description: str
    settings: Dict[str, Any]
    required_env_vars: list = None
    optional_env_vars: list = None


# Development Profile
DEVELOPMENT_PROFILE = ConfigProfile(
    name="development",
    description="Development environment with debug features and relaxed security",
    settings={
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "ENVIRONMENT": "development",
        "DB_TIMEOUT": 30,
        "DB_MAX_RETRIES": 3,
        "DB_BATCH_SIZE": 5,  # Smaller batches for testing
        "MAX_FILE_SIZE": 10 * 1024 * 1024,  # 10MB for dev
        "PROCESSING_BATCH_SIZE": 5,
        "ENABLE_OCR": False,
        "ENABLE_VECTOR_SEARCH": True,
        "ENABLE_DEDUPLICATION": True,
        "ENABLE_ANALYTICS": True,
        "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
        "EMBEDDING_DEVICE": "cpu",
    },
    required_env_vars=["SUPABASE_URL", "SUPABASE_KEY"],
    optional_env_vars=["LOG_FILE_PATH", "EMBEDDING_CACHE_DIR"]
)

# Testing Profile
TESTING_PROFILE = ConfigProfile(
    name="testing",
    description="Testing environment with mock services and test databases",
    settings={
        "DEBUG": True,
        "LOG_LEVEL": "WARNING",
        "ENVIRONMENT": "testing",
        "DB_TIMEOUT": 10,
        "DB_MAX_RETRIES": 1,
        "DB_BATCH_SIZE": 2,  # Very small batches for tests
        "MAX_FILE_SIZE": 1 * 1024 * 1024,  # 1MB for tests
        "PROCESSING_BATCH_SIZE": 2,
        "ENABLE_OCR": False,
        "ENABLE_VECTOR_SEARCH": False,  # Disable for faster tests
        "ENABLE_DEDUPLICATION": False,
        "ENABLE_ANALYTICS": False,
        "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
        "EMBEDDING_DEVICE": "cpu",
    },
    required_env_vars=["SUPABASE_URL", "SUPABASE_KEY"],
    optional_env_vars=[]
)

# Staging Profile
STAGING_PROFILE = ConfigProfile(
    name="staging",
    description="Staging environment that mimics production with additional logging",
    settings={
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "ENVIRONMENT": "staging",
        "DB_TIMEOUT": 60,
        "DB_MAX_RETRIES": 5,
        "DB_BATCH_SIZE": 10,
        "MAX_FILE_SIZE": 100 * 1024 * 1024,  # 100MB
        "PROCESSING_BATCH_SIZE": 10,
        "ENABLE_OCR": True,
        "ENABLE_VECTOR_SEARCH": True,
        "ENABLE_DEDUPLICATION": True,
        "ENABLE_ANALYTICS": True,
        "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
        "EMBEDDING_DEVICE": "cpu",
        "LOG_MAX_BYTES": 50 * 1024 * 1024,  # 50MB logs
        "LOG_BACKUP_COUNT": 10,
    },
    required_env_vars=["SUPABASE_URL", "SUPABASE_KEY"],
    optional_env_vars=["LOG_FILE_PATH", "EMBEDDING_CACHE_DIR"]
)

# Production Profile
PRODUCTION_PROFILE = ConfigProfile(
    name="production",
    description="Production environment with optimized performance and security",
    settings={
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "ENVIRONMENT": "production",
        "DB_TIMEOUT": 120,
        "DB_MAX_RETRIES": 10,
        "DB_BATCH_SIZE": 20,  # Larger batches for efficiency
        "MAX_FILE_SIZE": 500 * 1024 * 1024,  # 500MB
        "PROCESSING_BATCH_SIZE": 20,
        "ENABLE_OCR": True,
        "ENABLE_VECTOR_SEARCH": True,
        "ENABLE_DEDUPLICATION": True,
        "ENABLE_ANALYTICS": True,
        "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
        "EMBEDDING_DEVICE": "auto",  # Auto-detect best device
        "LOG_MAX_BYTES": 100 * 1024 * 1024,  # 100MB logs
        "LOG_BACKUP_COUNT": 20,
    },
    required_env_vars=[
        "SUPABASE_URL", 
        "SUPABASE_KEY", 
        "LOG_FILE_PATH"  # Required in production
    ],
    optional_env_vars=["EMBEDDING_CACHE_DIR"]
)

# High Performance Profile
HIGH_PERFORMANCE_PROFILE = ConfigProfile(
    name="high_performance",
    description="High-performance configuration for large-scale processing",
    settings={
        "DEBUG": False,
        "LOG_LEVEL": "WARNING",  # Reduced logging for performance
        "ENVIRONMENT": "production",
        "DB_TIMEOUT": 300,  # 5 minutes for large operations
        "DB_MAX_RETRIES": 15,
        "DB_BATCH_SIZE": 50,  # Large batches
        "MAX_FILE_SIZE": 1024 * 1024 * 1024,  # 1GB
        "PROCESSING_BATCH_SIZE": 50,
        "ENABLE_OCR": True,
        "ENABLE_VECTOR_SEARCH": True,
        "ENABLE_DEDUPLICATION": True,
        "ENABLE_ANALYTICS": False,  # Disable for performance
        "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
        "EMBEDDING_DEVICE": "auto",
        "LOG_MAX_BYTES": 200 * 1024 * 1024,  # 200MB logs
        "LOG_BACKUP_COUNT": 30,
    },
    required_env_vars=["SUPABASE_URL", "SUPABASE_KEY", "LOG_FILE_PATH"],
    optional_env_vars=["EMBEDDING_CACHE_DIR"]
)

# Profile registry
PROFILES = {
    "development": DEVELOPMENT_PROFILE,
    "testing": TESTING_PROFILE,
    "staging": STAGING_PROFILE,
    "production": PRODUCTION_PROFILE,
    "high_performance": HIGH_PERFORMANCE_PROFILE,
}


def get_profile(name: str) -> Optional[ConfigProfile]:
    """
    Get configuration profile by name
    
    Args:
        name: Profile name
        
    Returns:
        ConfigProfile or None if not found
    """
    return PROFILES.get(name.lower())


def list_profiles() -> Dict[str, str]:
    """
    List available configuration profiles
    
    Returns:
        Dict mapping profile names to descriptions
    """
    return {name: profile.description for name, profile in PROFILES.items()}


def merge_profile_with_env(profile: ConfigProfile, env_vars: Dict[str, str]) -> Dict[str, Any]:
    """
    Merge profile settings with environment variables
    Environment variables take precedence over profile defaults
    
    Args:
        profile: Configuration profile
        env_vars: Environment variables
        
    Returns:
        Merged configuration dictionary
    """
    merged = profile.settings.copy()
    
    # Override with environment variables
    for key, value in env_vars.items():
        if key in merged or key in (profile.required_env_vars or []) or key in (profile.optional_env_vars or []):
            # Convert string values to appropriate types
            if isinstance(merged.get(key), bool):
                merged[key] = value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(merged.get(key), int):
                try:
                    merged[key] = int(value)
                except ValueError:
                    merged[key] = value  # Keep as string if conversion fails
            else:
                merged[key] = value
    
    return merged


def validate_profile_requirements(profile: ConfigProfile, env_vars: Dict[str, str]) -> tuple[bool, list[str]]:
    """
    Validate that all required environment variables are present
    
    Args:
        profile: Configuration profile
        env_vars: Environment variables
        
    Returns:
        Tuple of (is_valid, list_of_missing_vars)
    """
    missing_vars = []
    
    if profile.required_env_vars:
        for var in profile.required_env_vars:
            if var not in env_vars or not env_vars[var]:
                missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars


def create_env_file_for_profile(profile: ConfigProfile, output_path: Path = None) -> str:
    """
    Create a .env file template for a specific profile
    
    Args:
        profile: Configuration profile
        output_path: Optional path to write the file
        
    Returns:
        Environment file content as string
    """
    content = f"""# Intelligence Agent Configuration - {profile.name.upper()} Profile
# {profile.description}

# ===== REQUIRED SETTINGS =====
"""
    
    # Add required variables
    if profile.required_env_vars:
        for var in profile.required_env_vars:
            if var in ['SUPABASE_URL', 'SUPABASE_KEY']:
                content += f"{var}=your_{var.lower()}_here\n"
            else:
                content += f"{var}=\n"
    
    content += "\n# ===== PROFILE DEFAULTS (can be overridden) =====\n"
    
    # Add profile settings
    for key, value in profile.settings.items():
        if isinstance(value, bool):
            content += f"{key}={str(value).lower()}\n"
        else:
            content += f"{key}={value}\n"
    
    content += "\n# ===== OPTIONAL SETTINGS =====\n"
    
    # Add optional variables
    if profile.optional_env_vars:
        for var in profile.optional_env_vars:
            content += f"# {var}=\n"
    
    # Add profile-specific comments
    if profile.name == "development":
        content += """
# Development-specific notes:
# - Debug mode is enabled
# - Smaller file size limits for testing
# - All features enabled for development
"""
    elif profile.name == "production":
        content += """
# Production-specific notes:
# - LOG_FILE_PATH is required in production
# - Larger batch sizes for efficiency
# - All security features enabled
"""
    elif profile.name == "high_performance":
        content += """
# High-performance notes:
# - Analytics disabled for maximum speed
# - Large batch sizes and file limits
# - Minimal logging for performance
"""
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(content)
    
    return content