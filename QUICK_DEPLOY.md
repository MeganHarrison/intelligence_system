# Quick Deployment Guide

## 🚀 **Deploy Backend to Railway**

### **Step 1: Connect to Railway**
1. Go to [Railway](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your repository: `intelligence_system`
4. **Deploy the ENTIRE repository** (not a subfolder)

### **Step 2: Set Environment Variables in Railway**
```bash
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
PORT=8000
```

### **Step 3: Railway will automatically:**
- Use the `railway.json` configuration
- Build with `Dockerfile.backend`
- Start with: `cd python-backend && uvicorn api_server:app --host 0.0.0.0 --port $PORT`

### **Step 4: Get your backend URL**
- After deployment, you'll get a URL like: `https://your-app-production.up.railway.app`
- Test it: `https://your-app-production.up.railway.app/api/health`

---

## 🌐 **Deploy Frontend to Vercel**

### **Step 1: Create a new GitHub repository for frontend**
1. Go to GitHub and create a new repository: `dashboard-frontend`
2. Push your frontend code:
   ```bash
   cd frontend-strategic-dashboard
   git remote add origin https://github.com/MeganHarrison/dashboard-frontend.git
   git push -u origin main
   ```

### **Step 2: Connect to Vercel**
1. Go to [Vercel](https://vercel.com)
2. Click "Import Project"
3. Select your `dashboard-frontend` repository
4. **No need to change root directory** - it will deploy correctly

### **Step 3: Set Environment Variables in Vercel**
```bash
NEXT_PUBLIC_API_URL=https://your-railway-backend-url.railway.app
```

### **Step 4: Deploy**
- Vercel will automatically build and deploy
- You'll get a URL like: `https://dashboard-frontend.vercel.app`

---

## 🔧 **After Deployment**

### **Update Backend CORS**
Once you have your Vercel URL, update the backend CORS settings in `python-backend/api_server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dashboard-frontend.vercel.app",  # Your Vercel URL
        "https://your-custom-domain.com",         # Any custom domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Test Your Deployment**
1. **Backend Health Check**: `https://your-railway-url.railway.app/api/health`
2. **Frontend**: `https://dashboard-frontend.vercel.app`
3. **API Integration**: Check that frontend can call backend APIs

---

## 📋 **Deployment Summary**

### **Backend (Railway)**
- **Repository**: `intelligence_system` (entire repo)
- **Build**: Uses `Dockerfile.backend`
- **Environment**: Supabase credentials + PORT=8000
- **Health Check**: `/api/health`

### **Frontend (Vercel)**
- **Repository**: `dashboard-frontend` (frontend folder only)
- **Build**: Next.js automatic
- **Environment**: `NEXT_PUBLIC_API_URL`
- **Framework**: Next.js 15.3.5

### **Expected URLs**
- **Backend**: `https://your-app-production.up.railway.app`
- **Frontend**: `https://dashboard-frontend.vercel.app`

🎉 **Your strategic dashboard will be live and fully functional!**