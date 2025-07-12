#!/usr/bin/env python3
"""
Configuration Manager CLI
Manage configuration profiles and environment settings
"""

import sys
import argparse
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import (
    get_settings, validate_configuration, export_configuration,
    print_configuration_summary
)
from config.profiles import get_profile, create_env_file_for_profile, PROFILES
from config.validators import ConfigValidationError


def list_profiles():
    """List available configuration profiles"""
    print("📋 AVAILABLE CONFIGURATION PROFILES")
    print("=" * 50)
    
    for name, profile in PROFILES.items():
        print(f"📁 {name}")
        print(f"   {profile.description}")
        print()


def show_profile(profile_name: str):
    """Show details of a specific profile"""
    profile = get_profile(profile_name)
    if not profile:
        print(f"❌ Profile '{profile_name}' not found")
        return False
    
    print(f"📁 PROFILE: {profile.name.upper()}")
    print("=" * 50)
    print(f"Description: {profile.description}")
    print()
    
    print("📋 Settings:")
    for key, value in profile.settings.items():
        print(f"  {key}: {value}")
    print()
    
    if profile.required_env_vars:
        print("🔑 Required Environment Variables:")
        for var in profile.required_env_vars:
            print(f"  - {var}")
        print()
    
    if profile.optional_env_vars:
        print("⚙️  Optional Environment Variables:")
        for var in profile.optional_env_vars:
            print(f"  - {var}")
        print()
    
    return True


def validate_config(profile_name: str = None):
    """Validate configuration"""
    print("🔍 VALIDATING CONFIGURATION")
    print("=" * 40)
    
    if profile_name:
        print(f"Profile: {profile_name}")
    
    is_valid, errors = validate_configuration(profile_name)
    
    if is_valid:
        print("✅ Configuration is valid!")
        
        # Show configuration summary
        try:
            settings = get_settings(profile_name)
            print()
            print_configuration_summary(settings)
        except Exception as e:
            print(f"⚠️  Could not load settings for summary: {e}")
    else:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  • {error}")
    
    return is_valid


def create_env_template(profile_name: str, output_file: str = None):
    """Create environment file template for a profile"""
    profile = get_profile(profile_name)
    if not profile:
        print(f"❌ Profile '{profile_name}' not found")
        return False
    
    output_path = Path(output_file) if output_file else Path(f".env.{profile_name}")
    
    try:
        content = create_env_file_for_profile(profile, output_path)
        print(f"✅ Created environment template: {output_path}")
        print()
        print("📋 Template content:")
        print("-" * 30)
        print(content[:500] + "..." if len(content) > 500 else content)
        return True
    except Exception as e:
        print(f"❌ Failed to create template: {e}")
        return False


def export_config(profile_name: str = None, output_file: str = None, include_secrets: bool = False):
    """Export configuration to JSON"""
    try:
        settings = get_settings(profile_name)
        config = export_configuration(settings, include_secrets)
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(config, f, indent=2, default=str)
            print(f"✅ Configuration exported to: {output_file}")
        else:
            print("📋 CONFIGURATION EXPORT")
            print("=" * 30)
            print(json.dumps(config, indent=2, default=str))
        
        return True
    except Exception as e:
        print(f"❌ Failed to export configuration: {e}")
        return False


def test_config(profile_name: str = None):
    """Test configuration by loading all components"""
    print("🧪 TESTING CONFIGURATION")
    print("=" * 30)
    
    try:
        # Test loading settings
        print("Loading settings...", end=" ")
        settings = get_settings(profile_name)
        print("✅")
        
        # Test logging setup
        print("Setting up logging...", end=" ")
        from config.settings import setup_logging
        setup_logging(settings)
        print("✅")
        
        # Test environment detection
        print("Testing environment detection...", end=" ")
        from config.settings import is_development, is_production, is_testing
        env_type = "development" if is_development() else "production" if is_production() else "testing" if is_testing() else "unknown"
        print(f"✅ ({env_type})")
        
        # Test feature flags
        print("Testing feature flags...", end=" ")
        features = []
        if settings.enable_vector_search:
            features.append("vector_search")
        if settings.enable_deduplication:
            features.append("deduplication")
        if settings.enable_analytics:
            features.append("analytics")
        print(f"✅ ({', '.join(features) if features else 'none'})")
        
        print()
        print("🎯 All configuration tests passed!")
        print_configuration_summary(settings)
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Intelligence Agent Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                              # List all profiles
  %(prog)s show development                  # Show development profile
  %(prog)s validate                          # Validate current config
  %(prog)s validate --profile production     # Validate production config
  %(prog)s template development              # Create .env template
  %(prog)s export --output config.json      # Export config to file
  %(prog)s test --profile staging           # Test staging config
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List profiles command
    subparsers.add_parser('list', help='List available configuration profiles')
    
    # Show profile command
    show_parser = subparsers.add_parser('show', help='Show profile details')
    show_parser.add_argument('profile', help='Profile name to show')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate configuration')
    validate_parser.add_argument('--profile', help='Configuration profile to validate')
    
    # Template command
    template_parser = subparsers.add_parser('template', help='Create environment file template')
    template_parser.add_argument('profile', help='Profile name for template')
    template_parser.add_argument('--output', help='Output file path (default: .env.{profile})')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export configuration to JSON')
    export_parser.add_argument('--profile', help='Configuration profile to export')
    export_parser.add_argument('--output', help='Output file path')
    export_parser.add_argument('--include-secrets', action='store_true', 
                              help='Include sensitive information in export')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test configuration')
    test_parser.add_argument('--profile', help='Configuration profile to test')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute commands
    success = True
    
    try:
        if args.command == 'list':
            list_profiles()
        elif args.command == 'show':
            success = show_profile(args.profile)
        elif args.command == 'validate':
            success = validate_config(args.profile)
        elif args.command == 'template':
            success = create_env_template(args.profile, args.output)
        elif args.command == 'export':
            success = export_config(args.profile, args.output, args.include_secrets)
        elif args.command == 'test':
            success = test_config(args.profile)
        else:
            print(f"❌ Unknown command: {args.command}")
            success = False
    
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)