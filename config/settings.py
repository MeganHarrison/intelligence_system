"""
Configuration Management for Intelligence Agent
Centralized settings and environment management with validation and profiles
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

from .validators import validate_all_settings, ConfigValidationError
from .profiles import get_profile, merge_profile_with_env, validate_profile_requirements


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    url: str
    key: str
    timeout: int = 30
    max_retries: int = 3
    batch_size: int = 10


@dataclass
class EmbeddingConfig:
    """Embedding model configuration"""
    model_name: str = "all-MiniLM-L6-v2"
    dimension: int = 384
    cache_dir: Optional[str] = None
    device: str = "cpu"


@dataclass
class ProcessingConfig:
    """Document processing configuration"""
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    supported_extensions: tuple = (
        '.txt', '.md', '.pdf', '.docx', '.xlsx', '.pptx', '.html', '.csv'
    )
    batch_size: int = 10
    enable_ocr: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


@dataclass
class Settings:
    """Main application settings"""
    database: DatabaseConfig
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Runtime settings
    debug: bool = False
    environment: str = "development"
    project_root: Path = field(default_factory=lambda: Path.cwd())
    
    # Feature flags
    enable_vector_search: bool = True
    enable_deduplication: bool = True
    enable_analytics: bool = True


def load_environment_variables() -> Dict[str, Any]:
    """Load environment variables from .env file"""
    # Try to load from project root
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    # Try to load from config directory
    config_env_path = Path(__file__).parent / ".env"
    if config_env_path.exists():
        load_dotenv(config_env_path)
    
    return dict(os.environ)


def get_settings(profile_name: str = None, validate: bool = True) -> Settings:
    """
    Get application settings from environment variables and configuration profiles
    
    Args:
        profile_name: Configuration profile to use (development, production, etc.)
        validate: Whether to validate configuration settings
    
    Environment Variables:
    - CONFIG_PROFILE: Configuration profile name
    - SUPABASE_URL: Supabase project URL (required)
    - SUPABASE_KEY: Supabase service key (required)
    - EMBEDDING_MODEL: Embedding model name (optional)
    - LOG_LEVEL: Logging level (optional)
    - DEBUG: Enable debug mode (optional)
    - ENVIRONMENT: Environment name (optional)
    
    Returns:
        Settings object with validated configuration
        
    Raises:
        ConfigValidationError: If configuration is invalid
        ValueError: If required settings are missing
    """
    env_vars = load_environment_variables()
    
    # Determine profile to use
    if not profile_name:
        profile_name = env_vars.get('CONFIG_PROFILE', 'development')
    
    # Get the configuration profile
    profile = get_profile(profile_name)
    if not profile:
        available_profiles = list(get_profile.__globals__['PROFILES'].keys())
        raise ValueError(f"Unknown profile '{profile_name}'. Available profiles: {available_profiles}")
    
    # Validate profile requirements
    profile_valid, missing_vars = validate_profile_requirements(profile, env_vars)
    if not profile_valid:
        raise ValueError(f"Missing required environment variables for profile '{profile_name}': {missing_vars}")
    
    # Merge profile settings with environment variables
    merged_config = merge_profile_with_env(profile, env_vars)
    
    # Validate configuration if requested
    if validate:
        config_valid, validation_errors = validate_all_settings(merged_config)
        if not config_valid:
            error_msg = f"Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in validation_errors)
            raise ConfigValidationError(error_msg)
    
    # Extract settings from merged configuration
    supabase_url = merged_config.get('SUPABASE_URL')
    supabase_key = merged_config.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY environment variables are required. "
            "Please check your .env file or configuration profile."
        )
    
    # Database configuration
    database_config = DatabaseConfig(
        url=supabase_url,
        key=supabase_key,
        timeout=int(merged_config.get('DB_TIMEOUT', 30)),
        max_retries=int(merged_config.get('DB_MAX_RETRIES', 3)),
        batch_size=int(merged_config.get('DB_BATCH_SIZE', 10))
    )
    
    # Embedding configuration
    embedding_config = EmbeddingConfig(
        model_name=merged_config.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2'),
        dimension=int(merged_config.get('EMBEDDING_DIMENSION', 384)),
        cache_dir=merged_config.get('EMBEDDING_CACHE_DIR'),
        device=merged_config.get('EMBEDDING_DEVICE', 'cpu')
    )
    
    # Processing configuration
    processing_config = ProcessingConfig(
        max_file_size=int(merged_config.get('MAX_FILE_SIZE', 50 * 1024 * 1024)),
        batch_size=int(merged_config.get('PROCESSING_BATCH_SIZE', 10)),
        enable_ocr=merged_config.get('ENABLE_OCR', False)
    )
    
    # Logging configuration
    logging_config = LoggingConfig(
        level=merged_config.get('LOG_LEVEL', 'INFO'),
        file_path=merged_config.get('LOG_FILE_PATH'),
        max_bytes=int(merged_config.get('LOG_MAX_BYTES', 10 * 1024 * 1024)),
        backup_count=int(merged_config.get('LOG_BACKUP_COUNT', 5))
    )
    
    # Main settings
    settings = Settings(
        database=database_config,
        embedding=embedding_config,
        processing=processing_config,
        logging=logging_config,
        debug=merged_config.get('DEBUG', False),
        environment=merged_config.get('ENVIRONMENT', 'development'),
        enable_vector_search=merged_config.get('ENABLE_VECTOR_SEARCH', True),
        enable_deduplication=merged_config.get('ENABLE_DEDUPLICATION', True),
        enable_analytics=merged_config.get('ENABLE_ANALYTICS', True)
    )
    
    return settings


def create_env_template(output_path: Path = None) -> str:
    """Create a .env template file"""
    template = """# Intelligence Agent Configuration
# Copy this to .env and fill in your actual values

# ===== REQUIRED SETTINGS =====
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# ===== OPTIONAL SETTINGS =====

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
EMBEDDING_DEVICE=cpu
# EMBEDDING_CACHE_DIR=/path/to/cache

# Database Configuration
DB_TIMEOUT=30
DB_MAX_RETRIES=3
DB_BATCH_SIZE=10

# Processing Configuration
MAX_FILE_SIZE=52428800  # 50MB in bytes
PROCESSING_BATCH_SIZE=10
ENABLE_OCR=false

# Logging Configuration
LOG_LEVEL=INFO
# LOG_FILE_PATH=/path/to/logfile.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Application Configuration
DEBUG=false
ENVIRONMENT=development

# Feature Flags
ENABLE_VECTOR_SEARCH=true
ENABLE_DEDUPLICATION=true
ENABLE_ANALYTICS=true
"""
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(template)
    
    return template


# Global settings instance
_settings: Optional[Settings] = None


def get_cached_settings() -> Settings:
    """Get cached settings instance"""
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings


def reload_settings(profile_name: str = None) -> Settings:
    """Reload settings from environment"""
    global _settings
    _settings = get_settings(profile_name)
    return _settings


def setup_logging(settings: Settings) -> None:
    """
    Configure logging based on settings
    
    Args:
        settings: Settings object with logging configuration
    """
    import logging.handlers
    
    # Create logger
    logger = logging.getLogger('intelligence_agent')
    logger.setLevel(getattr(logging, settings.logging.level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(settings.logging.format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if configured)
    if settings.logging.file_path:
        file_handler = logging.handlers.RotatingFileHandler(
            settings.logging.file_path,
            maxBytes=settings.logging.max_bytes,
            backupCount=settings.logging.backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Set propagate to False to avoid duplicate logs
    logger.propagate = False


def validate_configuration(profile_name: str = None) -> tuple[bool, list[str]]:
    """
    Validate configuration without creating Settings object
    
    Args:
        profile_name: Configuration profile to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    try:
        get_settings(profile_name, validate=True)
        return True, []
    except (ConfigValidationError, ValueError) as e:
        return False, [str(e)]
    except Exception as e:
        return False, [f"Unexpected error: {str(e)}"]


def export_configuration(settings: Settings, include_secrets: bool = False) -> Dict[str, Any]:
    """
    Export configuration as dictionary
    
    Args:
        settings: Settings object to export
        include_secrets: Whether to include sensitive information
        
    Returns:
        Configuration dictionary
    """
    config = {
        'environment': settings.environment,
        'debug': settings.debug,
        'database': {
            'timeout': settings.database.timeout,
            'max_retries': settings.database.max_retries,
            'batch_size': settings.database.batch_size,
        },
        'embedding': {
            'model_name': settings.embedding.model_name,
            'dimension': settings.embedding.dimension,
            'device': settings.embedding.device,
            'cache_dir': settings.embedding.cache_dir,
        },
        'processing': {
            'max_file_size': settings.processing.max_file_size,
            'batch_size': settings.processing.batch_size,
            'enable_ocr': settings.processing.enable_ocr,
            'supported_extensions': settings.processing.supported_extensions,
        },
        'logging': {
            'level': settings.logging.level,
            'file_path': settings.logging.file_path,
            'max_bytes': settings.logging.max_bytes,
            'backup_count': settings.logging.backup_count,
        },
        'features': {
            'enable_vector_search': settings.enable_vector_search,
            'enable_deduplication': settings.enable_deduplication,
            'enable_analytics': settings.enable_analytics,
        }
    }
    
    if include_secrets:
        config['database']['url'] = settings.database.url
        config['database']['key'] = settings.database.key
    else:
        config['database']['url'] = '[HIDDEN]'
        config['database']['key'] = '[HIDDEN]'
    
    return config


def print_configuration_summary(settings: Settings) -> None:
    """
    Print a formatted configuration summary
    
    Args:
        settings: Settings object to summarize
    """
    print("🔧 CONFIGURATION SUMMARY")
    print("=" * 40)
    print(f"Environment: {settings.environment}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Database Timeout: {settings.database.timeout}s")
    print(f"Embedding Model: {settings.embedding.model_name}")
    print(f"Embedding Device: {settings.embedding.device}")
    print(f"Max File Size: {settings.processing.max_file_size / (1024*1024):.1f}MB")
    print(f"Batch Size: {settings.processing.batch_size}")
    print(f"Log Level: {settings.logging.level}")
    
    print("\nFeature Flags:")
    print(f"  Vector Search: {'✅' if settings.enable_vector_search else '❌'}")
    print(f"  Deduplication: {'✅' if settings.enable_deduplication else '❌'}")
    print(f"  Analytics: {'✅' if settings.enable_analytics else '❌'}")
    print(f"  OCR: {'✅' if settings.processing.enable_ocr else '❌'}")


# Environment detection utilities
def is_development() -> bool:
    """Check if running in development environment"""
    return get_cached_settings().environment == 'development'


def is_production() -> bool:
    """Check if running in production environment"""
    return get_cached_settings().environment == 'production'


def is_testing() -> bool:
    """Check if running in testing environment"""
    return get_cached_settings().environment == 'testing'


def get_profile_info() -> Dict[str, str]:
    """Get information about available configuration profiles"""
    from .profiles import list_profiles
    return list_profiles()