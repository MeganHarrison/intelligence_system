# Strategic Dashboard Deployment Guide

## 🚀 Quick Deployment Options

### **Option 1: Vercel + Railway (Recommended)**
- **Frontend**: Deploy Next.js app on Vercel
- **Backend**: Deploy FastAPI on Railway
- **Database**: Already on Supabase (no changes needed)

### **Option 2: Full Stack on Railway**
- Deploy both frontend and backend on Railway
- Use Railway's monorepo support

### **Option 3: Docker Containers**
- Use provided Dockerfiles for containerized deployment
- Deploy to AWS, Google Cloud, or Azure

---

## 📋 Pre-Deployment Checklist

### **1. Environment Variables**
Create these environment variables in your deployment platform:

**Backend (.env):**
```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# OpenAI/Anthropic (if using AI features)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Environment
NODE_ENV=production
PORT=8000
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### **2. Update API URLs**
Update hardcoded localhost URLs in your frontend components:

**Files to update:**
- `src/components/projects-table.tsx`
- `src/app/projects/page.tsx`
- `src/app/documents/page.tsx`
- `src/app/chat/page.tsx`

**Replace:**
```typescript
const response = await fetch(`http://localhost:8000/api/projects?${params}`);
```

**With:**
```typescript
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/projects?${params}`);
```

---

## 🔧 Deployment Steps

### **Option 1: Vercel + Railway**

#### **Step 1: Deploy Backend to Railway**
1. Push your code to GitHub
2. Go to [Railway](https://railway.app)
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Choose the `python-backend` folder
6. Set environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SUPABASE_SERVICE_KEY`
   - `PORT=8000`
7. Deploy and get your backend URL

#### **Step 2: Deploy Frontend to Vercel**
1. Go to [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `frontend-strategic-dashboard`
4. Set environment variables:
   - `NEXT_PUBLIC_API_URL=https://your-railway-backend-url.com`
5. Deploy

### **Option 2: Full Stack on Railway**

#### **Step 1: Prepare Monorepo**
1. Create a `railway.json` in the root:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/api/health"
  }
}
```

#### **Step 2: Deploy to Railway**
1. Push to GitHub
2. Connect to Railway
3. Set environment variables
4. Deploy

### **Option 3: Docker Deployment**

#### **Step 1: Build Images**
```bash
# Build backend
cd python-backend
docker build -t strategic-dashboard-backend .

# Build frontend
cd ../frontend-strategic-dashboard
docker build -t strategic-dashboard-frontend .
```

#### **Step 2: Run with Docker Compose**
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./python-backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
  
  frontend:
    build: ./frontend-strategic-dashboard
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

---

## 🛠 Post-Deployment Tasks

### **1. Update CORS Settings**
In your backend `api_server.py`, update CORS origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.vercel.app",
        "https://your-custom-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **2. Set Up Custom Domain (Optional)**
- Configure custom domain in Vercel
- Update environment variables with new domain

### **3. Set Up Monitoring**
- Enable Vercel Analytics
- Set up Railway monitoring
- Configure Supabase monitoring

### **4. Document Storage**
For production, consider migrating documents to Supabase Storage:
- Upload documents to Supabase Storage bucket
- Update database with storage URLs
- Remove local file serving

---

## 🔍 Troubleshooting

### **Common Issues:**

1. **CORS Errors:**
   - Update CORS origins in backend
   - Check environment variables

2. **Database Connection:**
   - Verify Supabase credentials
   - Check network connectivity

3. **Build Failures:**
   - Check Node.js version compatibility
   - Verify all dependencies are installed

4. **API Errors:**
   - Check environment variables
   - Verify API endpoints

### **Health Check Endpoints:**
- Backend: `https://your-backend-url.com/api/health`
- Frontend: Should load without errors

---

## 📊 Performance Optimization

### **Frontend:**
- Enable Next.js ISR for static content
- Implement caching strategies
- Optimize images and assets

### **Backend:**
- Enable response caching
- Set up database connection pooling
- Implement rate limiting

### **Database:**
- Enable RLS (Row Level Security)
- Set up proper indexing
- Monitor query performance

---

## 🔐 Security Considerations

### **Environment Variables:**
- Never commit secrets to version control
- Use platform-specific secret management
- Rotate keys regularly

### **API Security:**
- Implement authentication
- Enable rate limiting
- Use HTTPS only

### **Database Security:**
- Enable RLS on Supabase
- Use service keys securely
- Monitor access logs

---

## 🚀 Next Steps

1. **Deploy backend to Railway**
2. **Deploy frontend to Vercel**
3. **Test all functionality**
4. **Set up monitoring**
5. **Configure custom domains**
6. **Implement security measures**

Your strategic dashboard will be live and accessible globally once deployed!