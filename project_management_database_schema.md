-- PROJECT MANAGEMENT DASHBOARD DATABASE SCHEMA
-- Interconnected tables for strategic intelligence

-- Enable UUID generation and vector extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. CLIENTS TABLE
CREATE TABLE clients (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    industry VARCHAR(100),
    tier VARCHAR(20) DEFAULT 'standard', -- premium, enterprise, standard
    status VARCHAR(20) DEFAULT 'active', -- active, inactive, prospect
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. PROJECTS TABLE - The strategic hub
CREATE TABLE projects (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(100), -- construction, design, consulting, etc.
    status VARCHAR(50) DEFAULT 'planning', -- planning, active, on_hold, completed, cancelled
    priority VARCHAR(20) DEFAULT 'medium', -- high, medium, low
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2),
    actual_cost DECIMAL(15,2) DEFAULT 0,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    project_manager VARCHAR(255),
    metadata JSONB DEFAULT '{}', -- Custom fields, tags, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. DOCUMENTS TABLE - Enhanced with project context
CREATE TABLE documents (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    document_type VARCHAR(100) NOT NULL, -- meeting_transcript, sop, project_file, contract, etc.
    file_path VARCHAR(500), -- Link to actual file
    file_size BIGINT,
    mime_type VARCHAR(100),
    source_meeting_id UUID, -- Reference to meetings table
    embedding VECTOR(384), -- For semantic search
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. TASKS TABLE - Granular execution tracking
CREATE TABLE tasks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    parent_task_id UUID REFERENCES tasks(id) ON DELETE CASCADE, -- For subtasks
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, blocked, cancelled
    priority VARCHAR(20) DEFAULT 'medium',
    assigned_to VARCHAR(255),
    assigned_by VARCHAR(255),
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    estimated_hours DECIMAL(5,2),
    actual_hours DECIMAL(5,2),
    source_meeting_id UUID, -- Which meeting generated this task
    source_document_id UUID REFERENCES documents(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. MEETINGS TABLE - Context for everything
CREATE TABLE meetings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    meeting_type VARCHAR(100), -- kickoff, status_update, review, client_meeting, etc.
    scheduled_date TIMESTAMP WITH TIME ZONE,
    actual_date TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER,
    attendees TEXT[], -- Array of attendee names/emails
    location VARCHAR(255),
    meeting_url VARCHAR(500),
    agenda TEXT,
    summary TEXT,
    sentiment VARCHAR(20), -- positive, neutral, negative
    action_items_count INTEGER DEFAULT 0,
    transcript_document_id UUID REFERENCES documents(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. PROJECT REPORTS TABLE - Strategic insights
CREATE TABLE project_reports (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    report_type VARCHAR(100), -- weekly, monthly, milestone, final, risk_assessment
    report_period_start DATE,
    report_period_end DATE,
    generated_by VARCHAR(255),
    executive_summary TEXT,
    key_achievements TEXT[],
    risks_identified TEXT[],
    issues_resolved TEXT[],
    budget_status JSONB, -- {planned: 100000, spent: 75000, remaining: 25000}
    schedule_status JSONB, -- {planned_completion: "2024-12-01", current_forecast: "2024-12-15"}
    next_milestones TEXT[],
    report_data JSONB, -- Structured data for charts/metrics
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- INDEXES for performance
CREATE INDEX idx_projects_client_id ON projects(client_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_priority ON projects(priority);
CREATE INDEX idx_documents_project_id ON documents(project_id);
CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_created_at ON documents(created_at);
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_meetings_project_id ON meetings(project_id);
CREATE INDEX idx_meetings_date ON meetings(scheduled_date);
CREATE INDEX idx_project_reports_project_id ON project_reports(project_id);
CREATE INDEX idx_project_reports_type ON project_reports(report_type);

-- Vector similarity index for semantic search
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);

-- VIEWS for dashboard queries
CREATE VIEW project_dashboard_summary AS
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

-- Function to get project context for any entity
CREATE OR REPLACE FUNCTION get_project_context(entity_type TEXT, entity_id UUID)
RETURNS TABLE(
    project_id UUID,
    project_name TEXT,
    client_name TEXT,
    project_status TEXT,
    context_data JSONB
) AS $$
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
$$ LANGUAGE plpgsql;

-- Function for semantic document search with project context
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
) AS $$
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
$$ LANGUAGE plpgsql;