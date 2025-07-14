#!/usr/bin/env python3
"""
Strategic Intelligence Dashboard API Server - PRODUCTION VERSION
FastAPI backend with minimal dependencies for Railway deployment
"""

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Global state
active_connections: Dict[str, WebSocket] = {}
active_workflows: Dict[str, Dict] = {}

# Initialize components to None for production
doc_extractor = None
strategic_workflow = None
business_system = None
ai_chief = None
fallback_db = None

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    context: Optional[Dict] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    project_type: Optional[str] = None
    status: str = "active"
    priority: str = "medium"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    progress_percentage: int = 0
    project_manager: Optional[str] = None
    client_name: Optional[str] = None
    client_company: Optional[str] = None
    created_at: str
    updated_at: str

class ProjectsListResponse(BaseModel):
    projects: List[ProjectResponse]
    total_count: int
    status: str

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    document_type: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    source_file: Optional[str] = None
    source_meeting_id: Optional[str] = None
    project_id: Optional[str] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    project_name: Optional[str] = None
    file_url: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None

class DocumentsListResponse(BaseModel):
    documents: List[DocumentResponse]
    total_count: int
    status: str

# Initialize FastAPI app
app = FastAPI(title="Strategic Intelligence Dashboard API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://dashboard-frontend.vercel.app",
        "https://*.vercel.app",
        "https://*.netlify.app",
        "https://*.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving documents
documents_path = project_root / "documents"
if documents_path.exists():
    app.mount("/documents", StaticFiles(directory=str(documents_path)), name="documents")
    print(f"✅ Serving documents from: {documents_path}")
else:
    print(f"⚠️ Documents directory not found: {documents_path}")

# Production-safe initialization
async def initialize_components():
    """Initialize components in production-safe mode"""
    global fallback_db
    
    print("🚀 Initializing components in production mode...")
    
    # Only try to initialize fallback database connection
    try:
        # Try to initialize a basic database connection
        from scripts.database_direct_connection import DirectDatabaseConnection
        fallback_db = DirectDatabaseConnection()
        await fallback_db.initialize()
        print("✅ Database connection initialized")
    except Exception as e:
        print(f"⚠️ Database connection error: {e}")
        fallback_db = None
    
    print("✅ Production initialization complete")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await initialize_components()
    yield
    # Shutdown
    print("🔄 Shutting down...")

app.router.lifespan_context = lifespan

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": "production",
        "database": "connected" if fallback_db else "disconnected"
    }

# Projects API
@app.get("/api/projects")
async def get_projects(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    sort_by: str = "updated_at",
    limit: int = 50,
    offset: int = 0
):
    """Get projects from database"""
    try:
        if fallback_db:
            return await _get_projects_from_db(status, priority, sort_by, limit, offset)
        else:
            return await _get_projects_fallback(status, priority, sort_by, limit, offset)
    except Exception as e:
        print(f"❌ Projects API error: {e}")
        return await _get_projects_fallback(status, priority, sort_by, limit, offset)

async def _get_projects_from_db(status, priority, sort_by, limit, offset):
    """Get projects from database"""
    try:
        # Build query
        query = fallback_db.supabase.table('project').select('*')
        
        # Apply filters
        if status:
            query = query.eq('status', status)
        if priority:
            query = query.eq('priority', priority)
        
        # Apply sorting
        if sort_by == 'name':
            query = query.order('name')
        elif sort_by == 'status':
            query = query.order('status')
        elif sort_by == 'priority':
            query = query.order('priority')
        else:
            query = query.order('updated_at', desc=True)
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        # Execute query
        result = query.execute()
        
        # Transform data
        projects = []
        for row in result.data:
            project = ProjectResponse(
                id=row['project_number'],
                name=row['name'] or '',
                description=row.get('description'),
                project_type=row.get('project_type'),
                status=row.get('status', 'active'),
                priority=row.get('priority', 'medium'),
                start_date=row.get('start_date'),
                end_date=row.get('est_completion'),
                budget=row.get('est_revenue'),
                actual_cost=row.get('actual_cost'),
                progress_percentage=row.get('progress_percentage', 0),
                project_manager=row.get('project_manager'),
                created_at=row['created_at'],
                updated_at=row.get('updated_at', row['created_at'])
            )
            projects.append(project)
        
        return ProjectsListResponse(
            projects=projects,
            total_count=len(projects),
            status="success"
        )
        
    except Exception as e:
        print(f"❌ Database query error: {e}")
        return await _get_projects_fallback(status, priority, sort_by, limit, offset)

async def _get_projects_fallback(status, priority, sort_by, limit, offset):
    """Fallback projects data"""
    sample_projects = [
        ProjectResponse(
            id="25-106",
            name="Seminole Collective",
            description="Strategic development project",
            project_type="commercial",
            status="active",
            priority="high",
            start_date="2024-01-15",
            end_date="2024-12-31",
            budget=250000,
            actual_cost=125000,
            progress_percentage=50,
            project_manager="John Smith",
            created_at="2024-01-15T10:00:00Z",
            updated_at="2024-07-14T10:00:00Z"
        ),
        ProjectResponse(
            id="24-203",
            name="Downtown Development",
            description="Urban development initiative",
            project_type="residential",
            status="planning",
            priority="medium",
            start_date="2024-03-01",
            end_date="2025-06-30",
            budget=500000,
            actual_cost=0,
            progress_percentage=25,
            project_manager="Sarah Johnson",
            created_at="2024-03-01T10:00:00Z",
            updated_at="2024-07-14T10:00:00Z"
        )
    ]
    
    # Apply filters
    filtered_projects = sample_projects
    if status:
        filtered_projects = [p for p in filtered_projects if p.status == status]
    if priority:
        filtered_projects = [p for p in filtered_projects if p.priority == priority]
    
    # Apply pagination
    start = offset
    end = offset + limit
    paginated_projects = filtered_projects[start:end]
    
    return ProjectsListResponse(
        projects=paginated_projects,
        total_count=len(filtered_projects),
        status="success"
    )

# Documents API
@app.get("/api/documents")
async def get_documents(
    document_type: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    limit: int = 100,
    offset: int = 0
):
    """Get documents from database"""
    try:
        if fallback_db:
            return await _get_documents_from_db(document_type, search, sort_by, limit, offset)
        else:
            return await _get_documents_fallback(document_type, search, sort_by, limit, offset)
    except Exception as e:
        print(f"❌ Documents API error: {e}")
        return await _get_documents_fallback(document_type, search, sort_by, limit, offset)

async def _get_documents_from_db(document_type, search, sort_by, limit, offset):
    """Get documents from database"""
    try:
        # Build query
        query = fallback_db.supabase.table('strategic_documents').select('*')
        
        # Apply filters
        if document_type:
            query = query.eq('document_type', document_type)
        if search:
            query = query.ilike('title', f'%{search}%')
        
        # Apply sorting
        if sort_by == 'title':
            query = query.order('title')
        elif sort_by == 'document_type':
            query = query.order('document_type')
        else:
            query = query.order('created_at', desc=True)
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        # Execute query
        result = query.execute()
        
        # Transform data
        documents = []
        for row in result.data:
            # Generate file URL if source_file exists
            file_url = None
            if row.get('source_file'):
                from urllib.parse import quote
                source_file = row['source_file']
                if source_file.startswith('documents/'):
                    source_file = source_file[len('documents/'):]
                encoded_filename = quote(source_file)
                file_url = f"http://localhost:8000/documents/{encoded_filename}"
            
            document = DocumentResponse(
                id=str(row['id']),
                title=row['title'],
                content=row.get('content'),
                document_type=row.get('document_type'),
                file_path=row.get('file_path'),
                file_size=row.get('file_size'),
                mime_type=row.get('mime_type'),
                source_file=row.get('source_file'),
                source_meeting_id=row.get('source_meeting_id'),
                project_id=row.get('project_id'),
                client_id=row.get('client_id'),
                file_url=file_url,
                created_at=row['created_at'],
                updated_at=row.get('updated_at')
            )
            documents.append(document)
        
        return DocumentsListResponse(
            documents=documents,
            total_count=len(documents),
            status="success"
        )
        
    except Exception as e:
        print(f"❌ Database query error: {e}")
        return await _get_documents_fallback(document_type, search, sort_by, limit, offset)

async def _get_documents_fallback(document_type, search, sort_by, limit, offset):
    """Fallback documents data"""
    sample_documents = [
        DocumentResponse(
            id="1",
            title="Strategic Planning Document",
            content="Sample strategic planning content...",
            document_type="strategic",
            file_path="/documents/strategic-plan.md",
            file_size=1024,
            mime_type="text/markdown",
            source_file="strategic-plan.md",
            file_url="http://localhost:8000/documents/strategic-plan.md",
            created_at="2024-07-14T10:00:00Z",
            updated_at="2024-07-14T10:00:00Z"
        )
    ]
    
    # Apply filters
    filtered_documents = sample_documents
    if document_type:
        filtered_documents = [d for d in filtered_documents if d.document_type == document_type]
    if search:
        filtered_documents = [d for d in filtered_documents if search.lower() in d.title.lower()]
    
    # Apply pagination
    start = offset
    end = offset + limit
    paginated_documents = filtered_documents[start:end]
    
    return DocumentsListResponse(
        documents=paginated_documents,
        total_count=len(filtered_documents),
        status="success"
    )

# Chat API
@app.post("/api/chat/message")
async def chat_message(request: ChatMessage):
    """Handle chat messages"""
    try:
        # Simple fallback response for production
        response_text = f"I received your message: '{request.message}'. In production mode, advanced AI features are disabled, but I can help with basic queries about your projects and documents."
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            context={"mode": "production", "ai_enabled": False}
        )
    except Exception as e:
        print(f"❌ Chat API error: {e}")
        return ChatResponse(
            response="I'm sorry, I encountered an error processing your message.",
            timestamp=datetime.now().isoformat(),
            context={"error": str(e)}
        )

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections[client_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Echo message back in production mode
            await websocket.send_text(json.dumps({
                "type": "response",
                "message": f"Received: {message}",
                "timestamp": datetime.now().isoformat()
            }))
            
    except WebSocketDisconnect:
        if client_id in active_connections:
            del active_connections[client_id]
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        if client_id in active_connections:
            del active_connections[client_id]

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)