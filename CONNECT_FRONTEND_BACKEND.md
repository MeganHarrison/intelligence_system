# Connect Frontend and Backend

## 🔧 **Step 1: Get Your Backend URL**

From your Railway dashboard, copy your backend URL. It should look like:
`https://intelligence-system-production-xxxx.up.railway.app`

## 🔧 **Step 2: Update Vercel Environment Variable**

1. Go to your Vercel dashboard
2. Select your frontend project
3. Go to **Settings** → **Environment Variables**
4. Add or update:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-railway-backend-url.railway.app`
   - **Environment**: Production (or All)
5. Click **Save**

## 🔧 **Step 3: Redeploy Frontend**

After setting the environment variable:
1. Go to **Deployments** tab in Vercel
2. Click on the latest deployment
3. Click **Redeploy**

## 🔧 **Step 4: Update Backend CORS**

The backend needs to allow requests from your frontend. Update the CORS settings:

1. In your backend code, find the CORS configuration
2. Add your Vercel URL to the allowed origins
3. Redeploy backend

## 🔧 **Step 5: Test the Connection**

1. **Test backend directly**:
   ```bash
   curl https://your-railway-backend-url.railway.app/api/health
   ```

2. **Test frontend**:
   - Visit your Vercel URL
   - Check browser console for errors
   - Try accessing the projects page

## 🚨 **Common Issues**

### **CORS Errors**
If you see CORS errors in browser console:
- Backend needs to allow your frontend domain
- Check the CORS middleware configuration

### **Network Errors**
If requests are failing:
- Verify the backend URL is correct
- Check if backend is actually running
- Test backend endpoints directly

### **Environment Variable Issues**
If `NEXT_PUBLIC_API_URL` isn't working:
- Make sure it starts with `NEXT_PUBLIC_`
- Redeploy frontend after setting variable
- Check browser's Network tab for actual URLs being called

## 🎯 **Quick Fix Commands**

```bash
# Test backend health
curl https://your-railway-backend-url.railway.app/api/health

# Test backend projects
curl https://your-railway-backend-url.railway.app/api/projects

# Test backend documents
curl https://your-railway-backend-url.railway.app/api/documents
```

## 🔄 **Expected Flow**

1. **Frontend** (Vercel) → **Backend** (Railway) → **Database** (Supabase)
2. Frontend uses `NEXT_PUBLIC_API_URL` to call backend
3. Backend processes request and queries Supabase
4. Backend returns data to frontend
5. Frontend displays data

Your connection should work after these steps!