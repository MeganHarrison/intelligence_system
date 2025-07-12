#!/usr/bin/env python3
"""
Intelligence Agent Setup Script
Automated installation and dependency management
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_dependencies(requirements_file="requirements.txt"):
    """Install dependencies from requirements file"""
    if not Path(requirements_file).exists():
        print(f"❌ {requirements_file} not found")
        return False
    
    return run_command(
        f"pip install -r {requirements_file}",
        f"Installing dependencies from {requirements_file}"
    )


def setup_environment():
    """Set up environment file template"""
    env_template = """# Intelligence Agent Configuration
# Copy this to .env and fill in your actual values

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Optional: Advanced Configuration
# EMBEDDING_MODEL=all-MiniLM-L6-v2
# LOG_LEVEL=INFO
# MAX_BATCH_SIZE=10
"""
    
    env_example_path = Path(".env.example")
    if not env_example_path.exists():
        with open(env_example_path, 'w') as f:
            f.write(env_template)
        print("✅ Created .env.example template")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("⚠️  Please copy .env.example to .env and configure your settings")
        return False
    else:
        print("✅ .env file exists")
        return True


def test_installation():
    """Test basic functionality"""
    print("🧪 Testing basic imports...")
    
    test_imports = [
        ("supabase", "Supabase client"),
        ("sentence_transformers", "Sentence Transformers"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("dotenv", "Python dotenv")
    ]
    
    success = True
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"✅ {description} imported successfully")
        except ImportError as e:
            print(f"❌ {description} import failed: {e}")
            success = False
    
    return success


def main():
    """Main installation process"""
    print("🚀 INTELLIGENCE AGENT SETUP")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Offer installation options
    print("\nInstallation options:")
    print("1. Minimal (core functionality only)")
    print("2. Full (all document processing features)")
    print("3. Development (includes testing and linting tools)")
    
    choice = input("\nSelect installation type (1-3) or press Enter for full: ").strip()
    
    if choice == "1":
        requirements_file = "requirements-minimal.txt"
    elif choice == "3":
        requirements_file = "requirements-dev.txt"
    else:
        requirements_file = "requirements.txt"
    
    print(f"\n📦 Installing {requirements_file}...")
    
    # Install dependencies
    if not install_dependencies(requirements_file):
        print("❌ Installation failed")
        sys.exit(1)
    
    # Set up environment
    setup_environment()
    
    # Test installation
    if test_installation():
        print("\n🎯 INSTALLATION COMPLETE!")
        print("=" * 30)
        print("Next steps:")
        print("1. Configure your .env file with Supabase credentials")
        print("2. Run: python database_setup.py")
        print("3. Test with: python strategic_code.py")
        print("\n🚀 Your intelligence agent is ready!")
    else:
        print("\n❌ Installation completed with errors")
        print("Please check the error messages above and try again")
        sys.exit(1)


if __name__ == "__main__":
    main()