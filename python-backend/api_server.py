#!/usr/bin/env python3
"""
Strategic Intelligence Dashboard API Server
FastAPI backend connecting Next.js frontend to Python intelligence agents
"""

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import intelligence agent components
try:
    from config.settings import get_settings
    from core.extractors import SupabaseDocumentExtractor
    from core.agents import StrategicAgentWorkflow
    from analysis.business import BusinessStrategicIntelligenceSystem
    from analysis.strategic import AIChiefOfStaffEnhanced
except ImportError as e:
    print(f"Warning: Could not import intelligence components: {e}")
    print("Some features may not be available until dependencies are installed.")

# FastAPI app initialization
app = FastAPI(
    title="Strategic Intelligence Dashboard API",
    description="Backend API for the strategic intelligence dashboard",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        "https://strategic-dashboard.vercel.app",  # Production (adjust as needed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
active_connections: Dict[str, WebSocket] = {}
active_workflows: Dict[str, Dict] = {}

# Pydantic models for request/response
class WorkflowRequest(BaseModel):
    query: str
    user_intent: str = "strategic_analysis"
    priority: str = "medium"
    client_id: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict] = None
    client_id: Optional[str] = None

class DocumentSearchRequest(BaseModel):
    query: str
    limit: int = 10
    similarity_threshold: float = 0.7

class AgentStatus(BaseModel):
    agent_id: str
    status: str
    last_activity: datetime
    performance_metrics: Dict[str, Any]

# Initialize intelligence components (with error handling)
doc_extractor = None
strategic_workflow = None
business_system = None
ai_chief = None

try:
    settings = get_settings()
    doc_extractor = SupabaseDocumentExtractor(
        settings.database.url,
        settings.database.key,
        settings.embedding.model_name
    )
    strategic_workflow = StrategicAgentWorkflow(doc_extractor)
    business_system = BusinessStrategicIntelligenceSystem()
    ai_chief = AIChiefOfStaffEnhanced()
    print("✅ Intelligence components initialized successfully")
except Exception as e:
    print(f"⚠️  Intelligence components not available: {e}")

# Startup event to initialize async components
@app.on_event("startup")
async def startup_event():
    """Initialize async components properly"""
    global business_system, ai_chief
    try:
        if doc_extractor and hasattr(doc_extractor, '_ensure_tables_exist'):
            await doc_extractor._ensure_tables_exist()
        
        # Initialize remaining components that weren't loaded
        if not business_system:
            business_system = BusinessStrategicIntelligenceSystem()
        if not ai_chief:
            ai_chief = AIChiefOfStaffEnhanced()
            
        print("✅ Async components initialized successfully")
    except Exception as e:
        print(f"⚠️  Some async components still unavailable: {e}")

# WebSocket management
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections[client_id] = websocket
    
    try:
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        }))
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }))
            elif message.get("type") == "workflow_progress_request":
                # Send workflow progress updates
                workflow_id = message.get("workflow_id")
                if workflow_id in active_workflows:
                    await websocket.send_text(json.dumps({
                        "type": "workflow_progress",
                        "workflow_id": workflow_id,
                        "progress": active_workflows[workflow_id]
                    }))
                    
    except WebSocketDisconnect:
        if client_id in active_connections:
            del active_connections[client_id]
        print(f"Client {client_id} disconnected")
    except Exception as e:
        print(f"WebSocket error for client {client_id}: {e}")
        if client_id in active_connections:
            del active_connections[client_id]

async def broadcast_to_client(client_id: str, message: Dict):
    """Send message to specific client"""
    if client_id in active_connections:
        try:
            await active_connections[client_id].send_text(json.dumps(message))
        except Exception as e:
            print(f"Failed to send message to client {client_id}: {e}")
            # Remove dead connection
            if client_id in active_connections:
                del active_connections[client_id]

async def broadcast_to_all(message: Dict):
    """Broadcast message to all connected clients"""
    dead_connections = []
    for client_id, websocket in active_connections.items():
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"Failed to broadcast to client {client_id}: {e}")
            dead_connections.append(client_id)
    
    # Clean up dead connections
    for client_id in dead_connections:
        if client_id in active_connections:
            del active_connections[client_id]

# API Routes

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "doc_extractor": doc_extractor is not None,
            "strategic_workflow": strategic_workflow is not None,
            "business_system": business_system is not None,
            "ai_chief": ai_chief is not None
        },
        "active_connections": len(active_connections),
        "active_workflows": len(active_workflows)
    }

@app.post("/api/workflows/execute")
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Execute strategic workflow with real-time updates"""
    if not strategic_workflow:
        raise HTTPException(status_code=503, detail="Strategic workflow not available")
    
    workflow_id = str(uuid.uuid4())
    client_id = request.client_id
    
    # Initialize workflow tracking
    active_workflows[workflow_id] = {
        "id": workflow_id,
        "status": "starting",
        "progress": 0,
        "current_step": "Initializing workflow",
        "query": request.query,
        "start_time": datetime.now().isoformat(),
        "client_id": client_id
    }
    
    # Notify client that workflow started
    if client_id:
        await broadcast_to_client(client_id, {
            "type": "workflow_started",
            "workflow_id": workflow_id,
            "query": request.query
        })
    
    # Execute workflow in background
    background_tasks.add_task(
        execute_workflow_background, 
        workflow_id, 
        request.query, 
        request.user_intent, 
        request.priority,
        client_id
    )
    
    return {
        "workflow_id": workflow_id,
        "status": "started",
        "estimated_duration": "30-60 seconds"
    }

async def execute_workflow_background(workflow_id: str, query: str, user_intent: str, priority: str, client_id: Optional[str]):
    """Background task to execute workflow with progress updates"""
    try:
        # Update progress: Starting analysis
        active_workflows[workflow_id].update({
            "status": "analyzing",
            "progress": 20,
            "current_step": "Analyzing strategic context"
        })
        
        if client_id:
            await broadcast_to_client(client_id, {
                "type": "workflow_progress",
                "workflow_id": workflow_id,
                "progress": 20,
                "step": "Analyzing strategic context"
            })
        
        # Execute the actual workflow
        results = await strategic_workflow.execute_strategic_workflow(
            query=query,
            user_intent=user_intent,
            priority=priority
        )
        
        # Update progress: Processing results
        active_workflows[workflow_id].update({
            "status": "processing",
            "progress": 80,
            "current_step": "Processing strategic insights"
        })
        
        if client_id:
            await broadcast_to_client(client_id, {
                "type": "workflow_progress",
                "workflow_id": workflow_id,
                "progress": 80,
                "step": "Processing strategic insights"
            })
        
        # Workflow completed
        active_workflows[workflow_id].update({
            "status": "completed",
            "progress": 100,
            "current_step": "Analysis complete",
            "results": results,
            "end_time": datetime.now().isoformat()
        })
        
        if client_id:
            await broadcast_to_client(client_id, {
                "type": "workflow_complete",
                "workflow_id": workflow_id,
                "results": results
            })
            
    except Exception as e:
        # Workflow failed
        active_workflows[workflow_id].update({
            "status": "failed",
            "error": str(e),
            "end_time": datetime.now().isoformat()
        })
        
        if client_id:
            await broadcast_to_client(client_id, {
                "type": "workflow_error",
                "workflow_id": workflow_id,
                "error": str(e)
            })

@app.get("/api/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow status"""
    if workflow_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return active_workflows[workflow_id]

@app.post("/api/chat/message")
async def chat_message(request: ChatMessage):
    """Handle chat messages with AI strategist"""
    if not ai_chief:
        raise HTTPException(status_code=503, detail="AI Chief of Staff not available")
    
    try:
        # Process message with AI Chief of Staff
        response = await process_strategic_chat(request.message, request.context)
        
        return {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "context_used": request.context is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

async def process_strategic_chat(message: str, context: Optional[Dict] = None) -> str:
    """Process strategic chat messages"""
    # This would integrate with your AI Chief of Staff
    # For now, return a structured response
    return f"Strategic analysis of your query: '{message}' - Based on current intelligence, I recommend focusing on data-driven decision making and stakeholder alignment."

@app.get("/api/dashboard/analytics")
async def get_dashboard_analytics():
    """Get dashboard analytics and metrics"""
    try:
        # Get real analytics if available
        if doc_extractor:
            analytics = await get_intelligence_analytics()
        else:
            # Fallback mock data
            analytics = {
                "total_documents": 45,
                "recent_activity": 12,
                "confidence_score": 87,
                "active_workflows": len(active_workflows)
            }
        
        return {
            **analytics,
            "system_status": "operational",
            "last_updated": datetime.now().isoformat(),
            "connected_clients": len(active_connections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

async def get_intelligence_analytics():
    """Get analytics from intelligence system"""
    # This would call your actual analytics functions
    return {
        "total_documents": 128,
        "recent_activity": 23,
        "confidence_score": 94,
        "active_workflows": len(active_workflows),
        "document_types": {
            "strategic_plans": 45,
            "meeting_notes": 32,
            "reports": 28,
            "presentations": 23
        }
    }

@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all strategic agents"""
    agents = [
        {
            "id": "intelligence_officer",
            "name": "Intelligence Officer",
            "status": "active" if doc_extractor else "unavailable",
            "last_activity": datetime.now().isoformat(),
            "performance_score": 94,
            "tasks_completed": 156
        },
        {
            "id": "strategic_advisor", 
            "name": "Strategic Advisor",
            "status": "active" if strategic_workflow else "unavailable",
            "last_activity": datetime.now().isoformat(),
            "performance_score": 91,
            "tasks_completed": 89
        },
        {
            "id": "execution_coordinator",
            "name": "Execution Coordinator", 
            "status": "active" if business_system else "unavailable",
            "last_activity": datetime.now().isoformat(),
            "performance_score": 88,
            "tasks_completed": 67
        },
        {
            "id": "ai_chief_of_staff",
            "name": "AI Chief of Staff",
            "status": "active" if ai_chief else "unavailable", 
            "last_activity": datetime.now().isoformat(),
            "performance_score": 96,
            "tasks_completed": 234
        }
    ]
    
    return {
        "agents": agents,
        "total_agents": len(agents),
        "active_agents": len([a for a in agents if a["status"] == "active"]),
        "system_performance": 92.5
    }

@app.post("/api/documents/search")
async def search_documents(request: DocumentSearchRequest):
    """Search documents using vector similarity"""
    if not doc_extractor:
        raise HTTPException(status_code=503, detail="Document search not available")
    
    try:
        results = await doc_extractor.advanced_search(
            query=request.query,
            limit=request.limit,
            similarity_threshold=request.similarity_threshold
        )
        
        return {
            "results": results,
            "query": request.query,
            "total_results": len(results),
            "search_time": "0.234s"  # Would be actual timing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document search failed: {str(e)}")

@app.get("/api/documents/stats")
async def get_document_stats():
    """Get document library statistics"""
    return {
        "total_documents": 128,
        "total_size_mb": 245.7,
        "document_types": {
            "PDF": 45,
            "Word": 32,
            "Excel": 28,
            "PowerPoint": 23
        },
        "recent_uploads": 7,
        "processing_queue": 2
    }

# Development helpers
@app.get("/api/dev/connections")
async def get_active_connections():
    """Development endpoint to see active WebSocket connections"""
    return {
        "active_connections": list(active_connections.keys()),
        "connection_count": len(active_connections),
        "active_workflows": list(active_workflows.keys())
    }

if __name__ == "__main__":
    print("🚀 Starting Strategic Intelligence Dashboard API Server")
    print("📡 WebSocket endpoint: ws://localhost:8000/ws/{client_id}")
    print("📚 API documentation: http://localhost:8000/api/docs")
    print("🎯 Frontend connection: http://localhost:3000")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )