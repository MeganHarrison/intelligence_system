# Strategic Intelligence Dashboard - Deployment Guide

## 🚀 Complete System Deployment

### **System Overview**
The Strategic Intelligence Dashboard is a full-stack application consisting of:
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: Python FastAPI with WebSocket support
- **Database**: Supabase with vector embeddings
- **Real-time**: WebSocket communication for live updates

## 📋 Prerequisites

### **System Requirements**
- Node.js 18+ and npm
- Python 3.8+
- Git
- 4GB+ RAM recommended

### **Environment Setup**
1. **Clone or navigate to project directory**
2. **Backend dependencies**: `pip install -r requirements.txt`
3. **Frontend dependencies**: `npm install` (in frontend directory)

## ⚙️ Configuration

### **Backend Configuration**
```bash
# Navigate to intelligence_agent root
cd /path/to/intelligence_agent

# Copy environment template
cp .env.example .env

# Configure .env with your settings:
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_key
CONFIG_PROFILE=development  # or production
```

### **Frontend Configuration**
```bash
# Navigate to frontend directory
cd frontend strategic-dashboard

# Copy environment template
cp .env.local.example .env.local

# Configure .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🔧 Development Deployment

### **Step 1: Start Backend Server**
```bash
# Terminal 1: Start Python backend
cd python-backend
python start_server.py

# Server will start at:
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
# WebSocket: ws://localhost:8000/ws/{client_id}
```

### **Step 2: Start Frontend Server**
```bash
# Terminal 2: Start Next.js frontend
cd "frontend strategic-dashboard"
npm run dev

# Frontend will start at:
# Dashboard: http://localhost:3000/dashboard
```

### **Step 3: Verify System**
1. **Backend Health**: Visit `http://localhost:8000/api/health`
2. **Frontend Access**: Visit `http://localhost:3000/dashboard`
3. **Connection Status**: Check green "Online" badges in dashboard
4. **Test Features**: Try executing a workflow or starting a chat

## 🌐 Production Deployment

### **Backend Deployment Options**

#### **Option 1: Railway/Heroku**
```bash
# Add to requirements.txt:
uvicorn[standard]>=0.24.0
gunicorn>=21.2.0

# Create Procfile:
web: uvicorn python-backend.api_server:app --host 0.0.0.0 --port $PORT

# Deploy:
git push railway main  # or heroku main
```

#### **Option 2: AWS/Azure/GCP**
```bash
# Use Docker container
FROM python:3.10-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "python-backend.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Frontend Deployment Options**

#### **Option 1: Vercel (Recommended)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd "frontend strategic-dashboard"
vercel

# Set environment variables in Vercel dashboard:
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_WS_URL=wss://your-backend-url.com
```

#### **Option 2: Netlify**
```bash
# Build for production
npm run build

# Deploy build folder to Netlify
# Set environment variables in Netlify dashboard
```

#### **Option 3: Self-hosted**
```bash
# Build application
npm run build
npm start

# Or use PM2 for process management
npm i -g pm2
pm2 start "npm start" --name strategic-dashboard
```

## 🔒 Security Configuration

### **Backend Security**
```python
# In api_server.py, update CORS for production:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### **Environment Variables**
```bash
# Production backend .env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
CONFIG_PROFILE=production
LOG_LEVEL=INFO
LOG_FILE_PATH=/var/log/strategic-dashboard.log

# Production frontend .env.local
NEXT_PUBLIC_API_URL=https://your-backend-api.com
NEXT_PUBLIC_WS_URL=wss://your-backend-api.com
NEXT_PUBLIC_APP_ENV=production
```

## 📊 Monitoring & Logging

### **Backend Monitoring**
```python
# Health check endpoint available at /api/health
# Returns system status and component health

# Logging configuration in config/settings.py
# Logs written to file in production mode
```

### **Frontend Monitoring**
```javascript
// Error tracking available via error boundaries
// Performance monitoring via React DevTools
// Real-time connection status in dashboard header
```

## 🔧 Maintenance

### **Regular Tasks**
1. **Monitor system health** via `/api/health` endpoint
2. **Check connection status** in dashboard header
3. **Review error logs** for backend and frontend
4. **Update dependencies** regularly for security
5. **Backup Supabase data** according to your backup strategy

### **Troubleshooting**

#### **Common Issues**
```bash
# Backend not starting
- Check Python dependencies: pip install -r requirements.txt
- Verify environment variables: python scripts/config_manager.py validate
- Check port availability: lsof -i :8000

# Frontend not connecting
- Verify API URL in .env.local
- Check CORS configuration in backend
- Test API directly: curl http://localhost:8000/api/health

# WebSocket connection failed
- Check WebSocket URL format (ws:// not http://)
- Verify firewall/proxy settings
- Test WebSocket manually with browser dev tools
```

#### **Debug Mode**
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Check connection status
python scripts/config_manager.py test

# View detailed logs
tail -f logs/strategic.log
```

## 📈 Performance Optimization

### **Backend Optimization**
- Use connection pooling for database
- Enable Redis caching for embeddings
- Configure proper worker processes for uvicorn
- Monitor memory usage with large document sets

### **Frontend Optimization**
- Enable Next.js static generation where possible
- Use React Query for efficient data caching
- Optimize bundle size with tree shaking
- Configure CDN for static assets

## 🎯 Success Metrics

### **System Health Indicators**
- ✅ Backend API responding < 500ms
- ✅ WebSocket connections stable
- ✅ Frontend loading < 3 seconds
- ✅ Error rate < 1%
- ✅ 99%+ uptime

### **User Experience Metrics**
- ✅ Dashboard navigation smooth
- ✅ Real-time updates working
- ✅ Chat responses < 2 seconds
- ✅ Analytics loading < 1 second
- ✅ Mobile experience responsive

## 📞 Support

### **Documentation**
- **API Documentation**: `http://localhost:8000/api/docs`
- **Frontend Components**: Built with shadcn/ui
- **Backend Architecture**: FastAPI + Supabase
- **Real-time Features**: WebSocket + Zustand state

### **Development Resources**
- **Backend Config**: `config/` directory
- **Frontend Stores**: `lib/stores/` directory
- **API Client**: `lib/utils/api.ts`
- **Component Library**: `components/` directory

---

## 🚀 Quick Start Commands

```bash
# Complete system startup
# Terminal 1 - Backend
cd python-backend && python start_server.py

# Terminal 2 - Frontend  
cd "frontend strategic-dashboard" && npm run dev

# Access dashboard
open http://localhost:3000/dashboard
```

**🎉 Your Strategic Intelligence Dashboard is now fully deployed and operational!**