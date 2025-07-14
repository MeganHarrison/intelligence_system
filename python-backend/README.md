# Python Backend API Server

FastAPI backend server that connects the Next.js frontend to the Python intelligence agent system.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# From the intelligence_agent root directory
pip install -r requirements.txt
```

### 2. Start the Server
```bash
# Option 1: Using startup script
cd python-backend
python start_server.py

# Option 2: Direct start
python api_server.py
```

### 3. Verify Server
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs  
- **Health Check**: http://localhost:8000/api/health
- **WebSocket**: ws://localhost:8000/ws/{client_id}

## 📡 API Endpoints

### Core Endpoints
- `GET /api/health` - Server health and component status
- `GET /api/dashboard/analytics` - Dashboard metrics
- `GET /api/agents/status` - Strategic agent status

### Workflow Management
- `POST /api/workflows/execute` - Execute strategic workflow
- `GET /api/workflows/{workflow_id}` - Get workflow status

### Chat Interface
- `POST /api/chat/message` - Chat with AI strategist

### Document Search
- `POST /api/documents/search` - Search documents
- `GET /api/documents/stats` - Document statistics

### Real-time Communication
- `WS /ws/{client_id}` - WebSocket for live updates

## 🔧 Configuration

The server automatically loads configuration from the intelligence agent system:
- Uses `CONFIG_PROFILE` environment variable (defaults to 'development')
- Loads Supabase credentials from environment
- Integrates with existing Python intelligence components

## 🎯 Integration with Frontend

### CORS Configuration
```typescript
// Frontend can connect from:
http://localhost:3000          // Next.js dev server
https://your-domain.com        // Production
```

### WebSocket Usage
```typescript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/unique-client-id');

// Listen for workflow updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle real-time updates
};
```

### API Client Example
```typescript
// Execute workflow
const response = await fetch('http://localhost:8000/api/workflows/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "What are our strategic priorities?",
    user_intent: "strategic_analysis",
    client_id: "frontend-client"
  })
});
```

## 🔍 Development Features

### Auto-reload
Server automatically reloads when code changes (development mode).

### API Documentation
Interactive API docs available at `/api/docs` with:
- Request/response schemas
- Try-it-out functionality  
- WebSocket documentation

### Debug Endpoints
- `GET /api/dev/connections` - Active WebSocket connections

## 🛡️ Error Handling

The server includes comprehensive error handling:
- Graceful degradation when intelligence components unavailable
- WebSocket connection management
- Background task error recovery
- CORS and security headers

## 📊 Monitoring

### Health Check Response
```json
{
  "status": "healthy",
  "components": {
    "doc_extractor": true,
    "strategic_workflow": true,
    "business_system": true,
    "ai_chief": true
  },
  "active_connections": 2,
  "active_workflows": 1
}
```

### Real-time Metrics
- Active WebSocket connections
- Running workflows
- Component availability
- Performance metrics

## 🔗 Next Steps

1. **Test the API**: Use the interactive docs at `/api/docs`
2. **Connect Frontend**: Update Next.js to use `http://localhost:8000`
3. **Add Features**: Extend endpoints for specific business needs
4. **Deploy**: Configure for production environment

The API server is now ready to bridge your Next.js frontend with the powerful Python intelligence agent system!