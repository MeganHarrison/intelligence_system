"""
Test the new project structure
Basic tests to ensure imports work correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_core_imports():
    """Test core module imports"""
    try:
        from core.extractors import SupabaseDocumentExtractor
        from core.agents import StrategicAgentWorkflow
        from core.database import EnhancedDatabaseSetup
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False


def test_ingestion_imports():
    """Test ingestion module imports"""
    try:
        from ingestion.universal import UniversalDocumentProcessor
        from ingestion.deduplication import SmartDocumentManager
        from ingestion.pipelines import EnhancedDocumentIngestionPipeline
        print("✅ Ingestion imports successful")
        return True
    except ImportError as e:
        print(f"❌ Ingestion import failed: {e}")
        return False


def test_analysis_imports():
    """Test analysis module imports"""
    try:
        from analysis.business import BusinessStrategicIntelligenceSystem
        from analysis.projects import ContextualProjectIntelligence
        from analysis.strategic import AIChiefOfStaffEnhanced
        print("✅ Analysis imports successful")
        return True
    except ImportError as e:
        print(f"❌ Analysis import failed: {e}")
        return False


def test_config_imports():
    """Test configuration imports"""
    try:
        from config.settings import get_settings, Settings
        print("✅ Config imports successful")
        return True
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 TESTING PROJECT STRUCTURE")
    print("=" * 40)
    
    tests = [
        test_core_imports,
        test_ingestion_imports,
        test_analysis_imports,
        test_config_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All structure tests passed!")
        return 0
    else:
        print("❌ Some tests failed - check import paths")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)