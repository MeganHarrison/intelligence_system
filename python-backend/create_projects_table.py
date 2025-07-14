#!/usr/bin/env python3
"""
Simple script to create the projects table in Supabase
"""

import os
import sys
sys.path.append('..')

def create_projects_table():
    """Create the projects table and insert sample data"""
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
        
        if not supabase_url or not supabase_key:
            print("❌ Missing Supabase credentials")
            return False
        
        from supabase import create_client
        supabase = create_client(supabase_url, supabase_key)
        
        print("✅ Connected to Supabase")
        
        # Create sample projects data
        sample_projects = [
            {
                'name': 'Paradise Isle Resort Development',
                'description': 'Complete resort development project including architecture, construction management, and interior design',
                'project_type': 'resort_development',
                'status': 'active',
                'priority': 'high',
                'start_date': '2024-01-15',
                'end_date': '2025-06-30',
                'budget': 2500000.00,
                'actual_cost': 1875000.00,
                'progress_percentage': 75,
                'project_manager': 'Sarah Johnson'
            },
            {
                'name': 'Goodwill Bloomington Store Renovation',
                'description': 'Complete renovation of Bloomington retail location with modern design and accessibility upgrades',
                'project_type': 'retail_renovation',
                'status': 'active',
                'priority': 'medium',
                'start_date': '2024-03-01',
                'end_date': '2024-09-15',
                'budget': 850000.00,
                'actual_cost': 680000.00,
                'progress_percentage': 80,
                'project_manager': 'Mike Chen'
            },
            {
                'name': 'PowerHIVE Energy Systems Integration',
                'description': 'Advanced energy management system implementation for sustainable operations',
                'project_type': 'energy_systems',
                'status': 'planning',
                'priority': 'high',
                'start_date': '2024-08-01',
                'end_date': '2024-12-31',
                'budget': 1200000.00,
                'actual_cost': 120000.00,
                'progress_percentage': 10,
                'project_manager': 'Lisa Rodriguez'
            },
            {
                'name': 'Niemann Foods Distribution Center',
                'description': 'Large-scale distribution facility design and construction management',
                'project_type': 'commercial_construction',
                'status': 'active',
                'priority': 'high',
                'start_date': '2024-04-01',
                'end_date': '2025-02-28',
                'budget': 3200000.00,
                'actual_cost': 1600000.00,
                'progress_percentage': 50,
                'project_manager': 'David Wilson'
            },
            {
                'name': 'Uniqlo Flagship Store Design',
                'description': 'Premium retail space design with modern aesthetic and customer experience focus',
                'project_type': 'retail_design',
                'status': 'completed',
                'priority': 'medium',
                'start_date': '2023-10-01',
                'end_date': '2024-04-30',
                'budget': 750000.00,
                'actual_cost': 720000.00,
                'progress_percentage': 100,
                'project_manager': 'Emma Thompson'
            }
        ]
        
        # First, let's try to create the table using raw SQL through RPC
        print("🔄 Trying to create projects table...")
        
        # Create table SQL
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS projects (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            project_type VARCHAR(100),
            status VARCHAR(50) DEFAULT 'planning',
            priority VARCHAR(50) DEFAULT 'medium',
            start_date DATE,
            end_date DATE,
            budget DECIMAL(15,2),
            actual_cost DECIMAL(15,2),
            progress_percentage INTEGER DEFAULT 0,
            project_manager VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """
        
        try:
            # Try to execute raw SQL - this might not work in all Supabase configs
            print("   Attempting to create table via RPC...")
            supabase.rpc('exec_sql', {'sql': create_table_sql}).execute()
            print("   ✅ Table created successfully")
        except Exception as e:
            print(f"   ⚠️ RPC method failed: {e}")
            print("   📝 Table might need to be created manually in Supabase dashboard")
            print("   📋 SQL to execute:")
            print(create_table_sql)
            print("\n   You can create the table manually in Supabase dashboard:")
            print("   1. Go to your Supabase project dashboard")
            print("   2. Go to SQL Editor")
            print("   3. Execute the SQL above")
            print("   4. Run this script again")
            return False
        
        # Insert projects
        print("🔄 Inserting sample projects...")
        result = supabase.table('projects').insert(sample_projects).execute()
        
        print(f"✅ Successfully inserted {len(result.data)} projects")
        
        # Verify the data
        projects = supabase.table('projects').select('*').execute()
        print(f"📊 Total projects in database: {len(projects.data)}")
        
        for project in projects.data:
            print(f"   • {project['name']} (Status: {project['status']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Creating projects table and inserting sample data...")
    print("=" * 50)
    
    success = create_projects_table()
    
    if success:
        print("\n✅ Projects table setup completed successfully!")
        print("   The projects API should now return real data")
    else:
        print("\n❌ Projects table setup failed!")
        print("   Check your Supabase configuration")