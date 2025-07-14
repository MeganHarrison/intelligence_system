# Project Restructuring Guide

## 🎯 **Recommended Structure**

```
strategic-dashboard/                    ← New parent folder
├── backend/                           ← Intelligence agent backend
│   ├── config/
│   ├── core/
│   ├── analysis/
│   ├── scripts/
│   ├── python-backend/
│   ├── documents/
│   ├── requirements.txt
│   ├── railway.json
│   ├── Dockerfile.backend
│   └── README.md
├── frontend/                          ← Strategic dashboard frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vercel.json
│   ├── Dockerfile.frontend
│   └── README.md
└── docs/                             ← Shared documentation
    ├── DEPLOYMENT.md
    ├── API.md
    └── SETUP.md
```

## 🚀 **Steps to Restructure**

1. **Create new parent directory:**
   ```bash
   cd /Users/meganharrison/Documents
   mkdir strategic-dashboard
   cd strategic-dashboard
   ```

2. **Move and rename backend:**
   ```bash
   mv ../intelligence_agent backend
   cd backend
   ```

3. **Move frontend to separate folder:**
   ```bash
   cd ..
   mv backend/frontend-strategic-dashboard frontend
   ```

4. **Create shared docs folder:**
   ```bash
   mkdir docs
   mv backend/documentation/* docs/
   mv backend/RAILWAY_DEPLOYMENT.md docs/
   ```

5. **Update deployment files:**
   - Update railway.json paths
   - Update Dockerfile.backend paths
   - Update deploy.sh script

## 🔧 **Benefits of This Structure**

- **Separate Git repos**: Each project can have its own repo
- **Independent deployments**: Deploy frontend to Vercel, backend to Railway
- **Team organization**: Different teams can work independently
- **Cleaner CI/CD**: Separate build pipelines
- **Better scaling**: Scale frontend/backend independently

## 📋 **After Restructuring**

1. **Backend deployment (Railway):**
   ```bash
   cd backend
   git init
   git remote add origin https://github.com/username/dashboard-backend.git
   git add .
   git commit -m "Initial backend commit"
   git push -u origin main
   ```

2. **Frontend deployment (Vercel):**
   ```bash
   cd frontend
   git init
   git remote add origin https://github.com/username/dashboard-frontend.git
   git add .
   git commit -m "Initial frontend commit"
   git push -u origin main
   ```

3. **Update environment variables:**
   - Backend: Keep Supabase config
   - Frontend: Update NEXT_PUBLIC_API_URL to Railway backend URL

## 🌐 **Deployment Flow**

1. **Deploy backend to Railway** → Get backend URL
2. **Update frontend environment** → Set NEXT_PUBLIC_API_URL
3. **Deploy frontend to Vercel** → Get frontend URL
4. **Update backend CORS** → Add frontend URL to allowed origins

This structure makes deployment much cleaner and more maintainable!