#!/usr/bin/env python3
"""
Database Connection Diagnostics - scripts/database_diagnostics.py
Troubleshoot MCP database server connection issues
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_environment_setup():
    """Test environment configuration"""
    print("🔍 TESTING ENVIRONMENT SETUP")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url:
            print("❌ SUPABASE_URL not found in environment")
            return False
        if not supabase_key:
            print("❌ SUPABASE_KEY not found in environment")
            return False
            
        print(f"✅ SUPABASE_URL configured: {supabase_url[:30]}...")
        print(f"✅ SUPABASE_KEY configured: {supabase_key[:20]}...")
        return True
        
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False

async def test_supabase_direct_connection():
    """Test direct Supabase connection (bypassing MCP)"""
    print("\n🔗 TESTING DIRECT SUPABASE CONNECTION")
    print("=" * 50)
    
    try:
        from supabase import create_client
        from dotenv import load_dotenv
        
        load_dotenv()
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")
        
        # Test basic connectivity
        result = supabase.table('strategic_documents').select('id').limit(1).execute()
        print(f"✅ Strategic documents table accessible: {len(result.data)} records")
        
        # Test project table
        result = supabase.table('project').select('project_number').limit(1).execute()
        print(f"✅ Project table accessible: {len(result.data)} records")
        
        # Test clients table
        result = supabase.table('clients').select('id').limit(1).execute()
        print(f"✅ Clients table accessible: {len(result.data)} records")
        
        return True
        
    except ImportError:
        print("❌ Supabase package not installed. Run: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

async def test_core_imports():
    """Test if core intelligence components can be imported"""
    print("\n📦 TESTING CORE IMPORTS")
    print("=" * 30)
    
    import_tests = [
        ("config.settings", "Configuration system"),
        ("core.extractors", "Document extractor"),
        ("analysis.business", "Business intelligence"),
        ("analysis.projects", "Project analysis"),
        ("analysis.strategic", "Strategic briefing")
    ]
    
    success_count = 0
    for module, description in import_tests:
        try:
            __import__(module)
            print(f"✅ {description} imported successfully")
            success_count += 1
        except ImportError as e:
            print(f"❌ {description} import failed: {e}")
        except Exception as e:
            print(f"⚠️ {description} import warning: {e}")
    
    print(f"\n📊 Import Success Rate: {success_count}/{len(import_tests)}")
    return success_count == len(import_tests)

async def test_database_queries():
    """Test specific database queries that are failing"""
    print("\n🔍 TESTING DATABASE QUERIES")
    print("=" * 35)
    
    try:
        from supabase import create_client
        from dotenv import load_dotenv
        
        load_dotenv()
        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        
        # Test the queries from your intelligence system
        test_queries = [
            ("Project Count", "project", "project_number"),
            ("Client Analysis", "clients", "name"),
            ("Strategic Documents", "strategic_documents", "title"),
            ("Task Management", "tasks", "title"),
            ("Meeting Data", "meetings", "meeting")
        ]
        
        for test_name, table, field in test_queries:
            try:
                result = supabase.table(table).select(field).limit(5).execute()
                print(f"✅ {test_name}: {len(result.data)} records")
                
                # Show sample data if available
                if result.data and len(result.data) > 0:
                    sample = result.data[0].get(field, 'No data')
                    print(f"   Sample: {str(sample)[:50]}...")
                    
            except Exception as e:
                print(f"❌ {test_name} failed: {e}")
    
    except Exception as e:
        print(f"❌ Database query testing failed: {e}")

async def diagnose_mcp_error():
    """Diagnose the specific MCP error"""
    print("\n🩺 DIAGNOSING MCP ERROR")
    print("=" * 30)
    
    print("The error 'SQL query cannot be empty or None' indicates:")
    print("1. ❌ Empty query string passed to MCP queryDatabase function")
    print("2. ❌ Function called with missing SQL parameter")
    print("3. ❌ Variable containing SQL is None or undefined")
    print()
    
    print("🔧 RECOMMENDED SOLUTIONS:")
    print("1. Use direct Supabase connection (bypass MCP)")
    print("2. Add query validation before MCP calls")
    print("3. Implement fallback error handling")
    print("4. Use the database_direct_connection.py script")
    print()
    
    print("💡 IMMEDIATE WORKAROUND:")
    print("Run: python scripts/database_direct_connection.py")
    print("This bypasses MCP and connects directly to your database")

async def create_sample_env_file():
    """Create a sample .env file if missing"""
    env_path = Path(project_root / ".env")
    env_example_path = Path(project_root / ".env.example")
    
    if not env_path.exists() and not env_example_path.exists():
        print("\n📝 CREATING SAMPLE .ENV FILE")
        print("=" * 35)
        
        sample_env = """# Intelligence Agent Configuration
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Optional Configuration
CONFIG_PROFILE=development
DEBUG=true
LOG_LEVEL=INFO

# Feature Flags
ENABLE_VECTOR_SEARCH=true
ENABLE_DEDUPLICATION=true
ENABLE_ANALYTICS=true
"""
        
        try:
            with open(env_example_path, 'w') as f:
                f.write(sample_env)
            print(f"✅ Created sample environment file: {env_example_path}")
            print("⚠️ Copy .env.example to .env and configure your Supabase credentials")
        except Exception as e:
            print(f"❌ Failed to create .env.example: {e}")

async def main():
    """Run complete diagnostic suite"""
    print("🚀 DATABASE CONNECTION DIAGNOSTICS")
    print("=" * 60)
    print("Analyzing your intelligence agent database connections...")
    print()
    
    # Run all diagnostic tests
    tests = [
        test_environment_setup,
        test_supabase_direct_connection,
        test_core_imports,
        test_database_queries
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    # Create env file if needed
    await create_sample_env_file()
    
    # Show diagnosis
    await diagnose_mcp_error()
    
    # Final summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 25)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All diagnostics passed - MCP issue is isolated")
        print("💡 Solution: Use database_direct_connection.py as fallback")
    elif passed >= total - 1:
        print("⚠️ Most systems working - minor configuration needed")
        print("💡 Solution: Fix remaining issues and use direct connection")
    else:
        print("❌ Multiple system issues detected")
        print("💡 Solution: Check environment setup and run database_direct_connection.py")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Run: python scripts/database_direct_connection.py")
    print("2. Update core components with fallback error handling")
    print("3. Test your intelligence system with: python main.py")

if __name__ == "__main__":
    asyncio.run(main())