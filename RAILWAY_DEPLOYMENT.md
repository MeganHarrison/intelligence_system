# Railway Deployment Guide

## 🚨 Important: Deploy the Entire Repository

**You MUST deploy the entire repository, not just the `python-backend` folder!**

The backend depends on these modules from the root directory:
- `config/` - Application settings
- `core/` - Database extractors and agents
- `analysis/` - Business intelligence systems
- `scripts/` - Database connection utilities
- `documents/` - Document files to serve

## 🚀 Railway Deployment Steps

### **Option 1: Deploy Backend (Recommended)**

1. **Push entire repository to GitHub**
2. **Connect Railway to your GitHub repo**
3. **Deploy the ENTIRE repository** (not just python-backend folder)
4. **Railway will automatically detect the `railway.json` config**

### **Option 2: Manual Configuration**

If Railway doesn't detect the config:

1. **Build Settings:**
   - Builder: `DOCKERFILE`
   - Dockerfile Path: `Dockerfile.backend`

2. **Deploy Settings:**
   - Start Command: `cd python-backend && uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/api/health`

3. **Environment Variables:**
   ```bash
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_KEY=your_supabase_service_key
   PORT=8000
   ```

## 📁 File Structure for Railway

```
intelligence_agent/                    ← Deploy this entire folder
├── railway.json                      ← Railway configuration
├── Dockerfile.backend                ← Backend container
├── Dockerfile.frontend               ← Frontend container
├── python-backend/                   ← Backend code
│   ├── api_server.py
│   ├── requirements.txt
│   └── ...
├── frontend-strategic-dashboard/     ← Frontend code
│   ├── src/
│   ├── package.json
│   └── ...
├── config/                          ← Required by backend
├── core/                            ← Required by backend
├── analysis/                        ← Required by backend
├── scripts/                         ← Required by backend
├── documents/                       ← Document files
└── ...
```

## 🔧 Alternative: Create a Production Backend

If you prefer to have a standalone backend, create a production version:

```bash
# Create a standalone backend folder
mkdir strategic-dashboard-backend
cd strategic-dashboard-backend

# Copy backend files
cp -r ../python-backend/* .

# Copy required modules
cp -r ../config .
cp -r ../core .
cp -r ../analysis .
cp -r ../scripts .
cp -r ../documents .

# Update imports in api_server.py to use relative paths
```

## 🌐 Deployment URLs

After deployment, you'll get:
- **Backend**: `https://your-app-production.up.railway.app`
- **Health Check**: `https://your-app-production.up.railway.app/api/health`

## 🔗 Frontend Connection

Update your frontend environment variable:
```bash
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.railway.app
```

## 🐛 Troubleshooting

### **Import Errors**
If you get import errors like `ModuleNotFoundError: No module named 'config'`:
- Make sure you deployed the entire repository
- Check that PYTHONPATH is set correctly in the Docker container

### **File Not Found**
If documents can't be served:
- Ensure the `documents/` folder is included in deployment
- Check file permissions in the container

### **Database Connection Issues**
- Verify environment variables are set correctly
- Check Supabase URL and keys
- Test connection with: `https://your-app.railway.app/api/health`

## ✅ Success Checklist

- [ ] Entire repository deployed (not just python-backend)
- [ ] Environment variables set
- [ ] Health check endpoint returns 200
- [ ] API endpoints accessible
- [ ] Document files served correctly
- [ ] Database connection working

## 🚀 Quick Commands

```bash
# Test your deployment
curl https://your-app.railway.app/api/health
curl https://your-app.railway.app/api/projects
curl https://your-app.railway.app/api/documents
```

The key is deploying the **entire repository** because the backend needs access to all the supporting modules!