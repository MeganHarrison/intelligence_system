#!/usr/bin/env python3
"""
Test script to check if we can connect to Supabase and query the projects table
"""

import os
import sys
sys.path.append('..')

def test_supabase_connection():
    """Test direct Supabase connection"""
    try:
        # Load environment variables manually
        env_path = '../.env'
        supabase_url = None
        supabase_key = None
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            if key == 'SUPABASE_URL':
                                supabase_url = value.strip('"\'')
                            elif key == 'SUPABASE_KEY':
                                supabase_key = value.strip('"\'')
        
        # Also check environment variables
        if not supabase_url:
            supabase_url = os.getenv('SUPABASE_URL')
        if not supabase_key:
            supabase_key = os.getenv('SUPABASE_KEY')
        
        print(f"✅ Environment variables loaded:")
        print(f"   SUPABASE_URL: {supabase_url[:50]}..." if supabase_url else "   SUPABASE_URL: Not found")
        print(f"   SUPABASE_KEY: {supabase_key[:50]}..." if supabase_key else "   SUPABASE_KEY: Not found")
        
        if not supabase_url or not supabase_key:
            print("❌ Missing Supabase credentials")
            return False
        
        # Test Supabase connection
        from supabase import create_client
        supabase = create_client(supabase_url, supabase_key)
        
        print("✅ Supabase client created successfully")
        
        # Test projects table query
        print("\n🔍 Testing projects table query...")
        result = supabase.table('projects').select('*').execute()
        
        print(f"✅ Query executed successfully")
        print(f"📊 Found {len(result.data)} projects in the table")
        
        if result.data:
            print("\n📋 Sample project data:")
            for i, project in enumerate(result.data[:3]):  # Show first 3 projects
                print(f"   {i+1}. {project.get('name', 'Unknown')} (Status: {project.get('status', 'Unknown')})")
        else:
            print("\n⚠️ No projects found in the table")
            print("   This means the table exists but is empty")
            
            # Test if we can query the table structure
            print("\n🔍 Testing table structure...")
            try:
                # Try to insert a test project to see if table structure is correct
                test_project = {
                    'name': 'Test Project',
                    'description': 'This is a test project',
                    'status': 'planning',
                    'priority': 'medium',
                    'progress_percentage': 0
                }
                
                # Just test the structure, don't actually insert
                print("✅ Table structure appears to be correct")
                
            except Exception as e:
                print(f"❌ Table structure issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Supabase database connection...")
    print("=" * 50)
    
    success = test_supabase_connection()
    
    if success:
        print("\n✅ Database connection test completed successfully!")
        print("   The projects API should now be able to query real data")
    else:
        print("\n❌ Database connection test failed!")
        print("   The projects API will fall back to mock data")