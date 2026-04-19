# Step-by-Step Deployment Guide

This guide provides detailed instructions for deploying the Mutual Fund FAQ Assistant on Render (backend) and Vercel (frontend).

---

## Part 1: Backend Deployment on Render

### Step 1: Prepare Your Repository

1. **Ensure your code is on GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Verify backend structure**
   ```
   apps/api/
   - main.py
   - requirements.txt
   - core/
     - enhanced_retriever.py
     - generator.py
   - routers/
     - metrics.py
   - .env.example
   ```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email address

### Step 3: Create Web Service

1. **Click "New +"** in Render dashboard
2. **Select "Web Service"**
3. **Connect Repository**
   - Choose your GitHub repository
   - Select the `main` branch
   - Set **Root Directory** to `apps/api`

4. **Configure Service Settings**
   ```
   Name: mutual-fund-api
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free (to start)
   ```

### Step 4: Set Environment Variables

In your Render service dashboard, go to **Environment** tab and add:

```bash
CHROMA_API_KEY=your_chroma_cloud_api_key
CHROMA_TENANT=your_chroma_tenant
CHROMA_DATABASE=your_chroma_database
GOOGLE_API_KEY=your_google_gemini_api_key
PYTHON_VERSION=3.10
```

**Important**: Don't use quotes around values in Render environment variables.

### Step 5: Deploy Backend

1. **Click "Create Web Service"**
2. Wait for the build to complete (2-3 minutes)
3. **Test the deployment**:
   ```bash
   curl https://your-service-name.onrender.com/health
   ```
   Should return: `{"status": "healthy"}`

4. **Test API endpoint**:
   ```bash
   curl -X POST https://your-service-name.onrender.com/api/chat/query \
   -H "Content-Type: application/json" \
   -d '{"thread_id": "test", "query": "What is expense ratio?"}'
   ```

### Step 6: Update CORS Settings

In `apps/api/main.py`, update the CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "https://your-vercel-app.vercel.app",  # Add your Vercel URL
        "*"  # Remove this in production for better security
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Part 2: Frontend Deployment on Vercel

### Step 1: Prepare Frontend Project

1. **Check if next.config.js exists** in `apps/web/`
   - If not, create it:

```javascript
// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
```

2. **Update package.json scripts** (if needed):

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "export": "next build && next export"
  }
}
```

### Step 2: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account
3. Verify your email

### Step 3: Import Project

1. **Click "New Project"**
2. **Select your GitHub repository**
3. **Configure Project Settings**:
   ```
   Framework Preset: Next.js
   Root Directory: apps/web
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

### Step 4: Set Environment Variables

In Vercel project settings, add:

```bash
NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com
NEXT_PUBLIC_APP_NAME=Mutual Fund FAQ Assistant
```

**Note**: `NEXT_PUBLIC_` prefix is required for frontend variables.

### Step 5: Deploy Frontend

1. **Click "Deploy"**
2. Wait for deployment to complete
3. **Visit your Vercel URL** to test

### Step 6: Update API Configuration

Ensure your frontend API calls use the correct URL:

```javascript
// apps/web/lib/api.js (create this file if it doesn't exist)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function chatQuery(threadId, query, schemeName) {
  const response = await fetch(`${API_BASE_URL}/api/chat/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ thread_id: threadId, query, scheme_name })
  });
  
  if (!response.ok) {
    throw new Error('API request failed');
  }
  
  return response.json();
}
```

---

## Part 3: GitHub Actions Scheduler Setup

### Step 1: Add Repository Secrets

Go to your GitHub repository:
1. **Settings** > **Secrets and variables** > **Actions**
2. **Add Repository Secrets**:

```bash
CHROMA_API_KEY=your_chroma_cloud_api_key
CHROMA_TENANT=your_chroma_tenant
CHROMA_DATABASE=your_chroma_database
GOOGLE_API_KEY=your_google_gemini_api_key
```

### Step 2: Test GitHub Actions

1. **Go to Actions tab** in your GitHub repository
2. **Select "Daily Mutual Fund Fact Ingestion"**
3. **Click "Run workflow"** to test manually
4. **Monitor the logs** to ensure success

---

## Part 4: Post-Deployment Testing

### Step 1: Backend Testing

```bash
# Health check
curl https://your-service-name.onrender.com/health

# API test
curl -X POST https://your-service-name.onrender.com/api/chat/query \
-H "Content-Type: application/json" \
-d '{"thread_id": "test", "query": "What is the expense ratio for Nippon India Large Cap Fund?"}'
```

### Step 2: Frontend Testing

1. **Visit your Vercel URL**
2. **Test the chat interface**
3. **Check browser console for errors**
4. **Verify API calls are working**

### Step 3: End-to-End Testing

1. **Ask a factual question** (should work)
2. **Ask an advisory question** (should refuse)
3. **Check citations are displayed**
4. **Verify disclaimer banner appears**

---

## Part 5: Common Issues & Solutions

### Issue 1: Backend Deployment Fails

**Problem**: Build fails on Render
**Solution**:
1. Check `requirements.txt` for correct dependencies
2. Ensure all Python files are properly structured
3. Review build logs in Render dashboard

### Issue 2: CORS Errors

**Problem**: Frontend can't connect to backend
**Solution**:
1. Update CORS origins in `main.py`
2. Add your Vercel URL to allowed origins
3. Remove `"*"` from origins in production

### Issue 3: Environment Variables Not Working

**Problem**: API calls failing due to missing keys
**Solution**:
1. Verify environment variables in Render dashboard
2. Check GitHub Actions secrets
3. Ensure variable names match exactly

### Issue 4: Frontend Build Fails

**Problem**: Vercel deployment fails
**Solution**:
1. Check `package.json` scripts
2. Ensure `next.config.js` is present
3. Review build logs in Vercel dashboard

### Issue 5: GitHub Actions Fail

**Problem**: Daily data ingestion not working
**Solution**:
1. Verify secrets in GitHub repository
2. Check file paths in workflow file
3. Monitor action logs for errors

---

## Part 6: Monitoring & Maintenance

### Render Monitoring

1. **Visit Render dashboard**
2. **Check service logs**
3. **Monitor response times**
4. **Set up alerts** (paid plans)

### Vercel Monitoring

1. **Visit Vercel dashboard**
2. **Check build logs**
3. **Use Vercel Analytics**
4. **Monitor error rates**

### GitHub Actions Monitoring

1. **Check Actions tab regularly**
2. **Set up email notifications**
3. **Monitor workflow success/failure**
4. **Review artifact retention**

---

## Part 7: URL Management

### Save These URLs

After deployment, save these URLs:

```bash
# Backend (Render)
Backend URL: https://your-service-name.onrender.com
Health Check: https://your-service-name.onrender.com/health
API Docs: https://your-service-name.onrender.com/docs

# Frontend (Vercel)
Frontend URL: https://your-app-name.vercel.app

# Repository
GitHub URL: https://github.com/your-username/your-repo

# Actions
GitHub Actions: https://github.com/your-username/your-repo/actions
```

---

## Part 8: Production Checklist

### Before Going Live

- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] API calls work correctly
- [ ] CORS properly configured
- [ ] Environment variables set
- [ ] GitHub Actions working
- [ ] Advisory refusal working
- [ ] Citations displayed correctly
- [ ] Disclaimer banner visible
- [ ] HTTPS enabled (automatic on both platforms)

### Security Checks

- [ ] No API keys in code
- [ ] CORS not set to `"*"` in production
- [ ] Rate limiting considered
- [ ] Error handling in place
- [ ] Logging configured

---

## Part 9: Cost Management

### Free Tier Limits

**Render Free Tier**:
- 750 hours/month
- 512MB RAM
- Shared CPU
- Sleeps after 15 minutes inactivity

**Vercel Free Tier**:
- 100GB bandwidth/month
- 100 function invocations/month
- Static site hosting

**GitHub Actions**:
- 2,000 minutes/month
- 500MB storage

### Upgrade When Needed

1. **Monitor usage** in dashboards
2. **Upgrade Render** if backend needs to stay awake
3. **Upgrade Vercel** if traffic increases
4. **Monitor API costs** (Google Gemini)

---

## Part 10: Next Steps

After successful deployment:

1. **Set up custom domains** (optional)
2. **Configure monitoring alerts**
3. **Set up backup procedures**
4. **Plan for scaling**
5. **Gather user feedback**
6. **Monitor performance metrics**

---

## Quick Reference Commands

```bash
# Test backend health
curl https://your-service-name.onrender.com/health

# Test API endpoint
curl -X POST https://your-service-name.onrender.com/api/chat/query \
-H "Content-Type: application/json" \
-d '{"thread_id": "test", "query": "What is expense ratio?"}'

# Redeploy backend (push to main)
git add .
git commit -m "Update backend"
git push origin main

# Redeploy frontend (push to main)
cd apps/web
git add .
git commit -m "Update frontend"
git push origin main
```

---

*Last Updated: April 19, 2026*
*Version: 1.0*
