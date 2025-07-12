#!/usr/bin/env python3
"""
Database Setup Script for Enhanced Project Management Dashboard
Initializes the interconnected schema for contextual intelligence
"""

import asyncio
import os
from dotenv import load_dotenv
from supabase import create_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDatabaseSetup:
    """Sets up the enhanced project management database schema"""
    
    def __init__(self):
        load_dotenv()
        
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")
        
        self.supabase = create_client(self.supabase_url, self.supabase_key)
    
    async def setup_complete_schema(self):
        """Set up the complete enhanced schema"""
        
        logger.info("🚀 Setting up enhanced project management database...")
        
        # Step 1: Enable extensions
        await self._enable_extensions()
        
        # Step 2: Create tables
        await self._create_tables()
        
        # Step 3: Create indexes
        await self._create_indexes()
        
        # Step 4: Create views and functions
        await self._create_views_and_functions()
        
        # Step 5: Set up Row Level Security
        await self._setup_security()
        
        # Step 6: Insert sample data (optional)
        sample_data = input("Would you like to insert sample data? (y/n): ").lower().strip()
        if sample_data == 'y':
            await self._insert_sample_data()
        
        logger.info("✅ Enhanced database setup complete!")
        logger.info("🎯 You can now run python ai_chief_of_staff_enhanced.py")
    
    async def _enable_extensions(self):
        """Enable required PostgreSQL extensions"""
        
        extensions = [
            'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
            'CREATE EXTENSION IF NOT EXISTS vector;'
        ]
        
        for ext in extensions:
            try:
                await self._execute_sql(ext)
                logger.info(f"✅ Extension enabled: {ext.split()[-1].replace(';', '')}")
            except Exception as e:
                logger.warning(f"⚠️ Extension warning: {e}")
    
    async def _create_tables(self):
        """Create all enhanced tables"""
        
        # Clients table
        clients_sql = """
        CREATE TABLE IF NOT EXISTS clients (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            company VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            industry VARCHAR(100),
            tier VARCHAR(20) DEFAULT 'standard',
            status VARCHAR(20) DEFAULT 'active',
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Projects table
        projects_sql = """
        CREATE TABLE IF NOT EXISTS projects (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            project_type VARCHAR(100),
            status VARCHAR(50) DEFAULT 'planning',
            priority VARCHAR(20) DEFAULT 'medium',
            start_date DATE,
            end_date DATE,
            budget DECIMAL(15,2),
            actual_cost DECIMAL(15,2) DEFAULT 0,
            progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
            project_manager VARCHAR(255),
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Enhanced documents table
        documents_sql = """
        CREATE TABLE IF NOT EXISTS documents (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
            client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            document_type VARCHAR(100) NOT NULL,
            file_path VARCHAR(500),
            file_size BIGINT,
            mime_type VARCHAR(100),
            source_meeting_id UUID,
            embedding VECTOR(384),
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Tasks table
        tasks_sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
            parent_task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            priority VARCHAR(20) DEFAULT 'medium',
            assigned_to VARCHAR(255),
            assigned_by VARCHAR(255),
            due_date TIMESTAMP WITH TIME ZONE,
            completed_at TIMESTAMP WITH TIME ZONE,
            estimated_hours DECIMAL(5,2),
            actual_hours DECIMAL(5,2),
            source_meeting_id UUID,
            source_document_id UUID REFERENCES documents(id),
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Meetings table
        meetings_sql = """
        CREATE TABLE IF NOT EXISTS meetings (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
            client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
            title VARCHAR(255) NOT NULL,
            meeting_type VARCHAR(100),
            scheduled_date TIMESTAMP WITH TIME ZONE,
            actual_date TIMESTAMP WITH TIME ZONE,
            duration_minutes INTEGER,
            attendees TEXT[],
            location VARCHAR(255),
            meeting_url VARCHAR(500),
            agenda TEXT,
            summary TEXT,
            sentiment VARCHAR(20),
            action_items_count INTEGER DEFAULT 0,
            transcript_document_id UUID REFERENCES documents(id),
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Project reports table
        project_reports_sql = """
        CREATE TABLE IF NOT EXISTS project_reports (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
            report_type VARCHAR(100),
            report_period_start DATE,
            report_period_end DATE,
            generated_by VARCHAR(255),
            executive_summary TEXT,
            key_achievements TEXT[],
            risks_identified TEXT[],
            issues_resolved TEXT[],
            budget_status JSONB,
            schedule_status JSONB,
            next_milestones TEXT[],
            report_data JSONB,
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        tables = [
            ("clients", clients_sql),
            ("projects", projects_sql),
            ("documents", documents_sql),
            ("tasks", tasks_sql),
            ("meetings", meetings_sql),
            ("project_reports", project_reports_sql)
        ]
        
        for table_name, sql in tables:
            try:
                await self._execute_sql(sql)
                logger.info(f"✅ Created table: {table_name}")
            except Exception as e:
                logger.error(f"❌ Error creating {table_name}: {e}")
    
    async def _create_indexes(self):
        """Create performance indexes"""
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_projects_client_id ON projects(client_id);",
            "CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);",
            "CREATE INDEX IF NOT EXISTS idx_projects_priority ON projects(priority);",
            "CREATE INDEX IF NOT EXISTS idx_documents_project_id ON documents(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);",
            "CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);",
            "CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);",
            "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);",
            "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);",
            "CREATE INDEX IF NOT EXISTS idx_meetings_project_id ON meetings(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(scheduled_date);",
            "CREATE INDEX IF NOT EXISTS idx_project_reports_project_id ON project_reports(project_id);",
            "CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);"
        ]
        
        for index in indexes:
            try:
                await self._execute_sql(index)
                logger.info(f"✅ Created index")
            except Exception as e:
                logger.warning(f"⚠️ Index warning: {e}")
    
    async def _create_views_and_functions(self):
        """Create views and database functions"""
        
        # Project dashboard summary view
        dashboard_view = """
        CREATE OR REPLACE VIEW project_dashboard_summary AS
        SELECT 
            p.id,
            p.name,
            p.status,
            p.priority,
            p.progress_percentage,
            c.name as client_name,
            c.company as client_company,
            COUNT(DISTINCT t.id) as total_tasks,
            COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) as completed_tasks,
            COUNT(DISTINCT CASE WHEN t.status = 'blocked' THEN t.id END) as blocked_tasks,
            COUNT(DISTINCT m.id) as total_meetings,
            MAX(m.actual_date) as last_meeting_date,
            COUNT(DISTINCT d.id) as total_documents,
            MAX(pr.created_at) as last_report_date,
            p.budget,
            p.actual_cost,
            CASE 
                WHEN p.budget > 0 THEN (p.actual_cost / p.budget) * 100 
                ELSE 0 
            END as budget_utilization_percentage
        FROM projects p
        LEFT JOIN clients c ON p.client_id = c.id
        LEFT JOIN tasks t ON p.id = t.project_id
        LEFT JOIN meetings m ON p.id = m.project_id
        LEFT JOIN documents d ON p.id = d.project_id
        LEFT JOIN project_reports pr ON p.id = pr.project_id
        GROUP BY p.id, c.name, c.company;
        """
        
        # Project context function
        context_function = """
        CREATE OR REPLACE FUNCTION get_project_context(entity_type TEXT, entity_id UUID)
        RETURNS TABLE(
            project_id UUID,
            project_name TEXT,
            client_name TEXT,
            project_status TEXT,
            context_data JSONB
        ) AS $
        BEGIN
            RETURN QUERY
            SELECT DISTINCT
                p.id,
                p.name,
                c.name,
                p.status,
                jsonb_build_object(
                    'priority', p.priority,
                    'progress', p.progress_percentage,
                    'budget_status', CASE 
                        WHEN p.budget > 0 THEN round((p.actual_cost / p.budget) * 100, 2)
                        ELSE 0 
                    END
                )
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.id
            WHERE 
                CASE entity_type
                    WHEN 'task' THEN p.id IN (SELECT project_id FROM tasks WHERE id = entity_id)
                    WHEN 'meeting' THEN p.id IN (SELECT project_id FROM meetings WHERE id = entity_id)
                    WHEN 'document' THEN p.id IN (SELECT project_id FROM documents WHERE id = entity_id)
                    WHEN 'report' THEN p.id IN (SELECT project_id FROM project_reports WHERE id = entity_id)
                    ELSE FALSE
                END;
        END;
        $ LANGUAGE plpgsql;
        """
        
        # Document search function
        search_function = """
        CREATE OR REPLACE FUNCTION search_documents_with_context(
            query_embedding VECTOR(384),
            project_filter UUID DEFAULT NULL,
            document_type_filter TEXT DEFAULT NULL,
            limit_count INTEGER DEFAULT 10
        )
        RETURNS TABLE(
            id UUID,
            title TEXT,
            content TEXT,
            document_type TEXT,
            project_name TEXT,
            client_name TEXT,
            similarity FLOAT
        ) AS $
        BEGIN
            RETURN QUERY
            SELECT 
                d.id,
                d.title,
                d.content,
                d.document_type,
                p.name as project_name,
                c.name as client_name,
                1 - (d.embedding <=> query_embedding) as similarity
            FROM documents d
            LEFT JOIN projects p ON d.project_id = p.id
            LEFT JOIN clients c ON p.client_id = c.id
            WHERE 
                (project_filter IS NULL OR d.project_id = project_filter)
                AND (document_type_filter IS NULL OR d.document_type = document_type_filter)
                AND d.embedding IS NOT NULL
            ORDER BY d.embedding <=> query_embedding
            LIMIT limit_count;
        END;
        $ LANGUAGE plpgsql;
        """
        
        functions = [
            ("dashboard view", dashboard_view),
            ("project context function", context_function),
            ("document search function", search_function)
        ]
        
        for name, sql in functions:
            try:
                await self._execute_sql(sql)
                logger.info(f"✅ Created {name}")
            except Exception as e:
                logger.warning(f"⚠️ Function warning for {name}: {e}")
    
    async def _setup_security(self):
        """Set up Row Level Security policies"""
        
        # Enable RLS on all tables
        rls_commands = [
            "ALTER TABLE clients ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE projects ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE documents ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE meetings ENABLE ROW LEVEL SECURITY;",
            "ALTER TABLE project_reports ENABLE ROW LEVEL SECURITY;"
        ]
        
        # Basic policies (adjust based on your authentication needs)
        policies = [
            """CREATE POLICY "Enable read access for authenticated users" ON clients
               FOR SELECT USING (auth.role() = 'authenticated');""",
            """CREATE POLICY "Enable read access for authenticated users" ON projects
               FOR SELECT USING (auth.role() = 'authenticated');""",
            """CREATE POLICY "Enable read access for authenticated users" ON documents
               FOR SELECT USING (auth.role() = 'authenticated');""",
            """CREATE POLICY "Enable read access for authenticated users" ON tasks
               FOR SELECT USING (auth.role() = 'authenticated');""",
            """CREATE POLICY "Enable read access for authenticated users" ON meetings
               FOR SELECT USING (auth.role() = 'authenticated');""",
            """CREATE POLICY "Enable read access for authenticated users" ON project_reports
               FOR SELECT USING (auth.role() = 'authenticated');"""
        ]
        
        all_security = rls_commands + policies
        
        for command in all_security:
            try:
                await self._execute_sql(command)
                logger.info("✅ Security policy applied")
            except Exception as e:
                logger.warning(f"⚠️ Security warning: {e}")
    
    async def _insert_sample_data(self):
        """Insert sample data for testing"""
        
        logger.info("📊 Inserting sample data...")
        
        # Sample clients
        clients_data = [
            {
                "name": "Paradise Isle Holdings",
                "company": "Paradise Isle Resort Group",
                "email": "contact@paradiseisle.com",
                "industry": "Hospitality",
                "tier": "enterprise"
            },
            {
                "name": "Goodwill Industries",
                "company": "Goodwill of Central Indiana",
                "email": "projects@goodwill.org",
                "industry": "Non-Profit",
                "tier": "standard"
            },
            {
                "name": "Alleato Group",
                "company": "Alleato Development",
                "email": "development@alleato.com",
                "industry": "Real Estate",
                "tier": "premium"
            }
        ]
        
        try:
            clients_result = self.supabase.table('clients').insert(clients_data).execute()
            client_ids = [client['id'] for client in clients_result.data]
            logger.info(f"✅ Inserted {len(client_ids)} sample clients")
            
            # Sample projects
            projects_data = [
                {
                    "client_id": client_ids[0],
                    "name": "Paradise Isle Resort Development",
                    "description": "Complete resort development project including architecture, construction management, and interior design",
                    "project_type": "resort_development",
                    "status": "active",
                    "priority": "high",
                    "budget": 2500000.00,
                    "actual_cost": 1875000.00,
                    "progress_percentage": 75,
                    "project_manager": "Sarah Johnson"
                },
                {
                    "client_id": client_ids[1],
                    "name": "Goodwill Bloomington Store Renovation",
                    "description": "Complete renovation of Bloomington retail location",
                    "project_type": "retail_renovation",
                    "status": "active",
                    "priority": "medium",
                    "budget": 850000.00,
                    "actual_cost": 680000.00,
                    "progress_percentage": 80,
                    "project_manager": "Mike Chen"
                },
                {
                    "client_id": client_ids[2],
                    "name": "PowerHIVE Mixed-Use Development",
                    "description": "Mixed-use commercial and residential development",
                    "project_type": "mixed_use",
                    "status": "planning",
                    "priority": "high",
                    "budget": 5200000.00,
                    "actual_cost": 312000.00,
                    "progress_percentage": 15,
                    "project_manager": "Lisa Rodriguez"
                }
            ]
            
            projects_result = self.supabase.table('projects').insert(projects_data).execute()
            project_ids = [project['id'] for project in projects_result.data]
            logger.info(f"✅ Inserted {len(project_ids)} sample projects")
            
            # Sample tasks
            sample_tasks = []
            for project_id in project_ids:
                sample_tasks.extend([
                    {
                        "project_id": project_id,
                        "title": "Review architectural drawings",
                        "status": "completed",
                        "priority": "high",
                        "assigned_to": "Design Team"
                    },
                    {
                        "project_id": project_id,
                        "title": "Schedule client presentation",
                        "status": "pending",
                        "priority": "medium",
                        "assigned_to": "Project Manager"
                    },
                    {
                        "project_id": project_id,
                        "title": "Update budget tracking",
                        "status": "in_progress",
                        "priority": "medium",
                        "assigned_to": "Finance Team"
                    }
                ])
            
            tasks_result = self.supabase.table('tasks').insert(sample_tasks).execute()
            logger.info(f"✅ Inserted {len(tasks_result.data)} sample tasks")
            
            # Sample meetings
            sample_meetings = []
            for project_id in project_ids:
                sample_meetings.append({
                    "project_id": project_id,
                    "title": "Weekly Project Review",
                    "meeting_type": "status_update",
                    "actual_date": "2025-07-12T10:00:00Z",
                    "duration_minutes": 60,
                    "sentiment": "positive",
                    "summary": "Project progressing well, all milestones on track",
                    "action_items_count": 3
                })
            
            meetings_result = self.supabase.table('meetings').insert(sample_meetings).execute()
            logger.info(f"✅ Inserted {len(meetings_result.data)} sample meetings")
            
            logger.info("🎯 Sample data insertion complete!")
            
        except Exception as e:
            logger.error(f"❌ Error inserting sample data: {e}")
    
    async def _execute_sql(self, sql: str):
        """Execute SQL using Supabase RPC"""
        try:
            result = self.supabase.rpc('exec_sql', {'sql': sql}).execute()
            return result
        except Exception as e:
            # Try alternative execution methods
            raise e
    
    async def verify_setup(self):
        """Verify the database setup is working correctly"""
        
        logger.info("🔍 Verifying database setup...")
        
        # Test basic queries
        tests = [
            ("clients table", lambda: self.supabase.table('clients').select('id').limit(1).execute()),
            ("projects table", lambda: self.supabase.table('projects').select('id').limit(1).execute()),
            ("documents table", lambda: self.supabase.table('documents').select('id').limit(1).execute()),
            ("tasks table", lambda: self.supabase.table('tasks').select('id').limit(1).execute()),
            ("meetings table", lambda: self.supabase.table('meetings').select('id').limit(1).execute()),
            ("project_reports table", lambda: self.supabase.table('project_reports').select('id').limit(1).execute()),
            ("dashboard view", lambda: self.supabase.table('project_dashboard_summary').select('id').limit(1).execute())
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
                logger.info(f"✅ {test_name} - OK")
            except Exception as e:
                logger.error(f"❌ {test_name} - Failed: {e}")
        
        logger.info("🎯 Database verification complete!")


async def main():
    """Main setup function"""
    
    print("""
🚀 ENHANCED PROJECT MANAGEMENT DATABASE SETUP
=============================================

This script will set up the enhanced database schema for your
contextual project management dashboard.

Requirements:
- Supabase project with database access
- SUPABASE_URL and SUPABASE_KEY in .env file
- PostgreSQL with vector extension support

""")
    
    confirm = input("Proceed with database setup? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Setup cancelled.")
        return
    
    try:
        setup = EnhancedDatabaseSetup()
        
        # Run complete setup
        await setup.setup_complete_schema()
        
        # Verify everything works
        await setup.verify_setup()
        
        print("""
✅ DATABASE SETUP COMPLETE!

🎯 Next Steps:
1. Run: python ai_chief_of_staff_enhanced.py
2. Your briefings will now include specific project context
3. Check the briefings/ folder for saved reports

📊 What's Different:
- Specific project and client details in alerts
- Contextual risk analysis with actionable insights  
- Meeting intelligence linked to projects
- Task management integrated with briefings

🚀 Your AI Chief of Staff is now 10x more intelligent!
""")
        
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        print(f"""
❌ Database setup failed: {e}

🔧 Troubleshooting:
1. Check your .env file
2. Verify Supabase project access
3. Ensure database has required permissions
4. Check Supabase project settings

📞 Contact support if issues persist.
""")


if __name__ == "__main__":
    asyncio.run(main())