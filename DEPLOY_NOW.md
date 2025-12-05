# 🚀 Deploy to Vercel - Complete Guide

## ✅ Configuration Status: READY

Your build configuration is now **100% correct** and ready for Vercel deployment.

---

## 📋 Pre-Deployment Checklist

Run verification:
```bash
./verify-build-config.sh
```

**Expected:** ✅ All checks passed!

---

## 🔧 Your Current Structure

```
/app/ (git repository root - this becomes / in GitHub)
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json  ✅ Has vercel-build script
│   └── build/        (created during build)
├── api/
│   ├── appointment.js
│   └── package.json
├── vercel.json       ✅ Correct paths
├── package.json      ✅ Root package.json
└── .vercelignore     ✅ Optimized
```

---

## 🚀 Step 1: Push to GitHub

```bash
# Make sure you're in /app directory
cd /app

# Check git status
git status

# Add all files
git add .

# Commit
git commit -m "fix: Vercel build configuration with correct paths"

# Push to GitHub
git push origin main
```

**If you don't have a GitHub repository yet:**

```bash
# Create new repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy on Vercel

### A. Connect GitHub to Vercel

1. Go to **https://vercel.com/dashboard**
2. Click **"Add New"** → **"Project"**
3. Click **"Import Git Repository"**
4. **Authorize Vercel** to access your GitHub
5. **Select your repository** from the list

### B. Configure Build Settings

Vercel will auto-detect settings, but verify:

**Framework Preset:**
- Select: **Create React App** or **Other**

**Root Directory:**
- Leave as: **`./`** (default - do NOT change!)

**Build Settings:**
- Build Command: `cd frontend && yarn build`
- Output Directory: `frontend/build`
- Install Command: `cd frontend && yarn install && cd ../api && yarn install`

**Note:** These are already in `vercel.json`, so you can leave them on "Override: No"

### C. Add Environment Variables

Click **"Environment Variables"** and add these **7 variables**:

```
SUPABASE_URL
https://ogoamklrsfxtapeqngta.supabase.co

SUPABASE_ANON_KEY
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9nb2Fta2xyc2Z4dGFwZXFuZ3RhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4MDQzNTMsImV4cCI6MjA3OTM4MDM1M30.ihBUh0ReyAHVEu5DuRwRvIRITmJDFEcDkTPD_ieVW5s

SUPABASE_SERVICE_ROLE_KEY
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9nb2Fta2xyc2Z4dGFwZXFuZ3RhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODk3MTE5MCwiZXhwIjoyMDU0NTQ3MTkwfQ.q3_7PzNw1tTjGDlT1z_DmnODKIU3dY4hESyDyO3EBQs

RESEND_API_KEY
re_jk3kFpBa_K3RKpjpMp3RGKBvMdepmjTYA

RESEND_SENDER_EMAIL
onboarding@resend.dev

RECIPIENT_EMAIL
elyonolawale@gmail.com

NODE_ENV
production
```

**Important:** Add them **one by one**, not all at once.

### D. Deploy!

1. Click **"Deploy"**
2. Wait **2-3 minutes** for build to complete
3. Watch the build logs for any errors

---

## 📊 What Vercel Will Do

```
1. Clone your repository from GitHub
   └─ Root is at / (which is your /app/ locally)

2. Install dependencies
   └─ cd frontend && yarn install
   └─ cd api && yarn install

3. Build frontend
   └─ cd frontend && yarn build
   └─ Creates frontend/build/ directory

4. Deploy static files
   └─ From frontend/build/ to CDN

5. Deploy serverless functions
   └─ From api/*.js as /api/* endpoints

6. Make live at:
   └─ https://your-project.vercel.app
```

---

## ✅ After Deployment

### Test Your Site

**1. Visit your live URL:**
```
https://your-project.vercel.app
```

**2. Test booking form:**
- Fill out the form
- Submit
- Check for success message

**3. Verify backend:**
```bash
curl -X POST https://your-project.vercel.app/api/appointment \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "4434771124",
    "serviceType": "Vehicle Wraps",
    "preferredDate": "2025-12-20",
    "message": "Test booking"
  }'
```

**Expected response:**
```json
{
  "status": "success",
  "message": "Your request has been submitted successfully...",
  "appointment_id": "uuid-here",
  "email_sent": true
}
```

**4. Check Supabase:**
- Go to Supabase Dashboard
- Table Editor → `appointments`
- Verify test record exists

**5. Check Email:**
- Check `elyonolawale@gmail.com`
- Verify notification email received

---

## 🌐 Step 3: Add Custom Domain (Optional)

### In Vercel Dashboard:

1. Go to **Project** → **Settings** → **Domains**
2. Click **"Add"**
3. Enter: `optimuscustomz.com`
4. Vercel will show DNS records to add

### In Wix DNS:

**Remove old Emergent IPs:**
- Delete: 162.159.142.117
- Delete: 172.66.2.113

**Add Vercel records:**
```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME  
Name: www
Value: cname.vercel-dns.com
```

**Wait 5-15 minutes for DNS propagation**

---

## 🐛 Troubleshooting

### Build Fails

**Check Vercel build logs:**
1. Go to Vercel Dashboard
2. Click your project
3. Click "Deployments"
4. Click latest deployment
5. Click "Building" tab
6. Read error messages

**Common issues:**

**Error: "Cannot find module"**
```bash
# Solution: Dependencies missing
# Check api/package.json has @supabase/supabase-js and resend
```

**Error: "Build command failed"**
```bash
# Solution: Test locally first
cd frontend
yarn install
yarn build
```

### API Returns 404

**Check function logs:**
1. Vercel Dashboard → Functions
2. Click `/api/appointment`
3. Check logs for errors

**Verify:**
- Environment variables are set
- api/appointment.js exists
- Supabase credentials are correct

### Frontend Shows Blank Page

**Check browser console:**
- Right-click → Inspect → Console
- Look for errors

**Common fix:**
- Clear browser cache
- Try incognito window
- Check if build output is correct

---

## 🔄 Future Deployments

After initial setup, deployments are automatic:

```bash
# Make changes locally
git add .
git commit -m "update: booking form improvements"
git push origin main

# Vercel automatically deploys!
```

**Branches:**
- `main` → Production deployment
- Other branches → Preview deployments
- Pull requests → Preview deployments

---

## 📞 Need Help?

**Vercel build failing?**
1. Check build logs in Vercel Dashboard
2. Run `./verify-build-config.sh` locally
3. Test build locally: `cd frontend && yarn build`

**API not working?**
1. Check environment variables in Vercel
2. Check Vercel function logs
3. Test Supabase connection

**Still stuck?**
- Review: `VERCEL_BUILD_CONFIGURATION.md`
- Check: Vercel documentation
- Verify: All 7 environment variables are set

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] GitHub repository connected to Vercel
- [ ] All 7 environment variables added
- [ ] Deployment successful (green checkmark)
- [ ] Site loads at https://your-project.vercel.app
- [ ] Booking form works
- [ ] Data appears in Supabase
- [ ] Email received
- [ ] Custom domain configured (optional)

---

## 🎉 You're Live!

**Your booking system is now deployed!**

- 🌐 Live Site: `https://your-project.vercel.app`
- 📧 Emails: Sent to `elyonolawale@gmail.com`
- 💾 Data: Stored in Supabase
- 🚀 Auto-deploys: On every push to main

**Congratulations! 🎊**
