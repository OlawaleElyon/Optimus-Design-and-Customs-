# 🚂 Railway Deployment Troubleshooting & Fix

## ⚠️ Common Railway Issues & Solutions

### Issue 1: Build Fails - "ModuleNotFoundError"

**Symptom:** Railway build fails with missing Python packages

**Cause:** `requirements.txt` missing or incorrect

**Fix:**
```bash
cd /app/backend
pip freeze > requirements.txt
```

**Verify requirements.txt includes:**
- fastapi
- uvicorn
- resend
- motor (MongoDB)
- pydantic
- python-dotenv

---

### Issue 2: App Crashes - "Port Binding Error"

**Symptom:** App starts then crashes immediately

**Cause:** Not binding to Railway's $PORT variable

**Fix in Railway Settings:**
- **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`

⚠️ Must use `$PORT` (Railway's dynamic port), not `8001`

---

### Issue 3: "MONGO_URL Not Found"

**Symptom:** App crashes with MongoDB connection error

**Cause:** Environment variables not set in Railway

**Fix:**
1. Go to Railway Project → Variables tab
2. Add all environment variables:
```
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/db?retryWrites=true
DB_NAME=optimus_database
RESEND_API_KEY=re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9
RESEND_SENDER_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=elyonolawale@gmail.com
CORS_ORIGINS=*
```

---

### Issue 4: MongoDB Connection Fails

**Symptom:** "Connection refused" or "Timeout"

**Cause:** Using local MongoDB URL or wrong connection string

**Solution: Use MongoDB Atlas (Cloud)**

#### Step-by-Step MongoDB Atlas Setup:

1. **Create Account:**
   - Go to mongodb.com/cloud/atlas
   - Sign up (free)

2. **Create Cluster:**
   - Choose FREE M0 tier
   - Select AWS, closest region
   - Cluster name: `Cluster0`

3. **Create Database User:**
   - Username: `optimusadmin`
   - Password: (auto-generate) → **SAVE THIS!**

4. **Network Access:**
   - Add IP: `0.0.0.0/0` (allow all)

5. **Get Connection String:**
   - Click "Connect" → "Connect your application"
   - Copy string:
   ```
   mongodb+srv://optimusadmin:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   - Replace `PASSWORD` with your actual password
   - Add database name:
   ```
   mongodb+srv://optimusadmin:PASSWORD@cluster0.xxxxx.mongodb.net/optimus_database?retryWrites=true&w=majority
   ```

6. **Add to Railway:**
   - Variables tab → Add `MONGO_URL` with full connection string

---

### Issue 5: CORS Errors After Deployment

**Symptom:** Frontend can't connect to Railway backend

**Cause:** CORS not configured for Vercel domain

**Fix in `/app/backend/server.py`:**

Replace:
```python
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

With:
```python
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "https://www.optimuscustomz.com",
        "https://optimuscustomz.vercel.app",
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔧 Complete Railway Setup (Step-by-Step)

### Prerequisites:
- ✅ MongoDB Atlas account with cluster created
- ✅ MongoDB connection string ready
- ✅ Railway account connected to GitHub

### Step 1: Prepare Backend

1. **Simplify server.py** (remove payment features for now)
2. **Update requirements.txt:**
```bash
cd /app/backend
pip freeze > requirements.txt
```

### Step 2: Create Railway Project

1. Go to railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose: `Optimus-Design-and-Customs`
5. Railway starts building

### Step 3: Configure Railway

**In Railway Project Settings:**

1. **Root Directory:**
   - Set to: `/app/backend`

2. **Start Command:**
   - Set to: `uvicorn server:app --host 0.0.0.0 --port $PORT`

3. **Build Command (optional):**
   - Set to: `pip install -r requirements.txt`

### Step 4: Add Environment Variables

Click "Variables" tab, add each:

```
MONGO_URL=mongodb+srv://optimusadmin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/optimus_database?retryWrites=true&w=majority

DB_NAME=optimus_database

RESEND_API_KEY=re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9

RESEND_SENDER_EMAIL=onboarding@resend.dev

RECIPIENT_EMAIL=elyonolawale@gmail.com

CORS_ORIGINS=https://www.optimuscustomz.com,https://optimuscustomz.vercel.app

PORT=$PORT
```

⚠️ **Replace** `YOUR_PASSWORD` with your MongoDB Atlas password!

### Step 5: Deploy

1. Railway auto-deploys
2. Wait 3-5 minutes
3. Check "Deployments" tab for status
4. If successful, you'll see ✅

### Step 6: Get Railway URL

1. Click "Settings" → "Networking"
2. Click "Generate Domain"
3. Copy URL (e.g., `https://optimus-backend-production.up.railway.app`)

### Step 7: Update Vercel Frontend

1. Go to Vercel Dashboard
2. Settings → Environment Variables
3. Add/Update:
   ```
   REACT_APP_BACKEND_URL=https://your-railway-url.up.railway.app
   ```
4. Redeploy Vercel

### Step 8: Test

1. Visit https://www.optimuscustomz.com/
2. Submit booking form
3. Check Railway logs for activity
4. Verify email received

---

## 🔍 Debugging Railway

### View Logs:
1. Railway Dashboard → Your Project
2. Click "View Logs"
3. Look for errors

### Common Log Errors:

**"ModuleNotFoundError: No module named 'X'"**
- Fix: Add package to requirements.txt
- Redeploy

**"Address already in use"**
- Fix: Check Start Command uses `$PORT`

**"Connection refused [MongoDB]"**
- Fix: Check MONGO_URL is correct
- Verify MongoDB Atlas IP whitelist includes `0.0.0.0/0`

**"CORS policy error"**
- Fix: Update CORS_ORIGINS in server.py
- Add your Vercel domain

---

## 💡 Simplified Backend (Railway-Ready)

If your current backend is too complex, here's a minimal version:

```python
# server_simple.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Optimus Backend Running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

Deploy this first to verify Railway works, then add features.

---

## ⚡ Alternative: Use Render Instead

If Railway continues to fail, try **Render.com**:

1. Go to render.com
2. Sign up with GitHub
3. "New +" → "Web Service"
4. Select your repository
5. Configure:
   - **Root Directory:** `app/backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (same as Railway)
7. Deploy

**Render is often more reliable than Railway for Python apps!**

---

## 🎯 Quick Decision Guide

**Choose Vercel Only If:**
- ✅ You just need email notifications
- ✅ You don't need to store bookings
- ✅ You don't need payment processing
- ✅ You want zero costs
- ✅ You want simplest setup

**Choose Railway/Render If:**
- ✅ You need to store booking data
- ✅ You want payment processing
- ✅ You want admin dashboard
- ✅ You want booking management system

---

**My Recommendation: Start with Vercel-only. Add Railway later when you need database features!** 🚀
