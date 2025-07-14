# Vercel Deployment Fix

## 🔧 **Problem Fixed**
The `vercel.json` file was referencing a secret `@next_public_api_url` that doesn't exist.

## ✅ **Solution Applied**
1. **Removed secret reference** from `vercel.json`
2. **Environment variable** should be set directly in Vercel dashboard

## 🚀 **Deploy to Vercel Steps**

### **Step 1: Create Frontend Repository**
You need to create a separate GitHub repository for the frontend:

1. Go to GitHub and create a new repository: `dashboard-frontend`
2. Push your frontend code:
   ```bash
   git remote remove origin
   git remote add origin https://github.com/MeganHarrison/dashboard-frontend.git
   git push -u origin main
   ```

### **Step 2: Connect to Vercel**
1. Go to [Vercel](https://vercel.com)
2. Click "Import Project"
3. Select your `dashboard-frontend` repository
4. **Framework**: Next.js (auto-detected)
5. **Root Directory**: Leave as default (root)

### **Step 3: Set Environment Variable**
In Vercel dashboard:
1. Go to **Settings** → **Environment Variables**
2. Add:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-railway-backend-url.railway.app`
   - **Environment**: Production (or All)
3. Click **Save**

### **Step 4: Deploy**
1. Click **Deploy**
2. Vercel will build and deploy automatically
3. You'll get a URL like: `https://dashboard-frontend.vercel.app`

## 📋 **After Deployment**

### **Update Backend CORS**
Add your Vercel URL to the backend CORS settings:

1. **Get your Railway backend URL** from Railway dashboard
2. **Get your Vercel frontend URL** from Vercel dashboard
3. **Update backend CORS** in `python-backend/api_server.py`:
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
1. **Frontend**: Visit your Vercel URL
2. **Backend**: Visit your Railway URL + `/api/health`
3. **Integration**: Test that frontend can call backend APIs

## 🌐 **Expected Result**
- **Frontend**: `https://dashboard-frontend.vercel.app`
- **Backend**: `https://your-app.railway.app`
- **Full functionality**: Projects, documents, dashboard working

Your strategic dashboard will be live and fully functional!