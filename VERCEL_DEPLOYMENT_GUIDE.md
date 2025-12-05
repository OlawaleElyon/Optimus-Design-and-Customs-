# Complete Vercel Deployment Guide

## 🎯 Overview

Your app is now configured for Vercel with:
- ✅ React frontend (static build)
- ✅ Node.js serverless functions (`/api`)
- ✅ Supabase for database
- ✅ Resend for email
- ✅ Email fallback system

---

## 📋 Pre-Deployment Checklist

### 1. Verify File Structure

```
/app/
├── api/
│   ├── appointment.js       # Serverless function
│   └── package.json         # Dependencies
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
├── vercel.json             # Vercel configuration
└── README.md
```

### 2. Verify Supabase Setup

Run this SQL in Supabase SQL Editor:

```sql
-- Verify appointments table exists
SELECT * FROM appointments LIMIT 1;

-- Create email_notifications table for fallback
CREATE TABLE IF NOT EXISTS email_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_email_notifications_status 
ON email_notifications(status);
```

---

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to https://vercel.com/dashboard**

2. **Click "Add New" → "Project"**

3. **Import your Git repository**
   - Connect GitHub/GitLab/Bitbucket
   - Select your repository
   - Click "Import"

4. **Configure Project**
   - Framework Preset: **Create React App**
   - Root Directory: `./`
   - Build Command: `cd frontend && yarn build`
   - Output Directory: `frontend/build`
   - Install Command: `cd frontend && yarn install && cd ../api && yarn install`

5. **Add Environment Variables**

   Click "Environment Variables" and add:

   ```
   SUPABASE_URL=https://ogoamklrsfxtapeqngta.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
   RESEND_API_KEY=re_jk3kFpBa_K3RKpjpMp3RGKBvMdepmjTYA
   RESEND_SENDER_EMAIL=onboarding@resend.dev
   RECIPIENT_EMAIL=elyonolawale@gmail.com
   NODE_ENV=production
   ```

6. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your live URL: `https://your-project.vercel.app`

---

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Navigate to project
cd /app

# Deploy
vercel

# Follow prompts:
# - Link to existing project or create new
# - Confirm settings
# - Deploy

# Deploy to production
vercel --prod
```

---

## 🔧 Environment Variables Setup

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Your Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anon key | `eyJ...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | `eyJ...` |
| `RESEND_API_KEY` | Resend API key | `re_...` |
| `RESEND_SENDER_EMAIL` | Email sender address | `onboarding@resend.dev` |
| `RECIPIENT_EMAIL` | Your notification email | `elyonolawale@gmail.com` |

### Where to Find These Keys

**Supabase:**
1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to Settings → API
4. Copy `URL`, `anon/public key`, and `service_role key`

**Resend:**
1. Go to https://resend.com/api-keys
2. Copy your API key (starts with `re_`)

---

## 🔍 Testing Deployment

### 1. Test API Endpoint

```bash
curl -X POST https://your-project.vercel.app/api/appointment \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Customer",
    "email": "test@example.com",
    "phone": "443-477-1124",
    "serviceType": "Vehicle Wraps",
    "preferredDate": "2025-12-15",
    "message": "Test booking"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Your request has been submitted successfully...",
  "appointment_id": "uuid-here",
  "email_sent": true
}
```

### 2. Check Vercel Logs

- Go to Vercel Dashboard → Your Project → Functions
- Click on `/api/appointment`
- Check "Logs" tab
- Look for:
  ```
  ✅ Saved to Supabase: uuid
  ✅ Email sent successfully: email-id
  ```

### 3. Verify Supabase

- Go to Supabase → Table Editor → `appointments`
- Check for new test record

### 4. Check Email

- Check `elyonolawale@gmail.com` for notification email

---

## 🌐 Custom Domain Setup

### 1. Add Domain in Vercel

1. Go to Project → Settings → Domains
2. Add your domain: `optimuscustomz.com`
3. Copy the provided DNS records

### 2. Update DNS Provider (Wix)

Add these records in Wix DNS:

**For Vercel (not Emergent):**

| Type | Name | Value |
|------|------|-------|
| A | @ | `76.76.21.21` |
| CNAME | www | `cname.vercel-dns.com` |

Or Vercel will provide specific instructions for your domain.

### 3. Wait for DNS Propagation

- Usually takes 5-15 minutes
- Check status at: https://dnschecker.org

---

## 🐛 Troubleshooting

### Build Fails

**Error: "Cannot find module"**
```bash
# Solution: Check package.json dependencies
cd frontend && yarn install
cd ../api && yarn install
```

**Error: "Build command failed"**
```bash
# Check vercel.json build configuration
# Make sure paths are correct
```

### API Not Working

**Error: "405 Method Not Allowed"**
- Check `vercel.json` routes configuration
- Ensure `/api/*` routes to serverless functions

**Error: "Supabase connection failed"**
- Verify environment variables in Vercel Dashboard
- Check Supabase credentials are correct
- Check Supabase project is not paused

**Error: "Email not sending"**
- Check RESEND_API_KEY is valid
- Check Resend account is active
- Look for emails in Supabase `email_notifications` fallback table

### Frontend Not Loading

**Blank page:**
- Check browser console for errors
- Verify build output directory is `frontend/build`
- Check public path in package.json

**API calls failing:**
- Check CORS headers in `api/appointment.js`
- Verify frontend is calling `/api/appointment` (not full URL)

---

## 📊 Monitoring

### Vercel Analytics

- Go to Project → Analytics
- Monitor:
  - Function execution time
  - Error rates
  - Request counts

### Supabase Monitoring

- Go to Project → Database
- Monitor:
  - Table row counts
  - Failed email notifications
  - Database performance

### Set Up Alerts

```javascript
// Add to api/appointment.js for critical failures
if (!appointmentId) {
  // Send alert to monitoring service
  // e.g., Sentry, LogRocket, etc.
}
```

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

Vercel automatically deploys when you push to:
- **Production:** `main` or `master` branch
- **Preview:** Any other branch or PR

### Disable Auto-Deploy

In Vercel Dashboard:
- Project → Settings → Git
- Uncheck "Automatically deploy commits"

---

## 🚨 Emergency Rollback

If deployment breaks:

1. **Go to Vercel Dashboard**
2. **Click "Deployments"**
3. **Find last working deployment**
4. **Click "..." → "Promote to Production"**

Or via CLI:
```bash
vercel rollback
```

---

## 📝 Post-Deployment Checklist

- [ ] Website loads at `your-project.vercel.app`
- [ ] Booking form submits successfully
- [ ] Data appears in Supabase `appointments` table
- [ ] Email received at `elyonolawale@gmail.com`
- [ ] Custom domain working (if configured)
- [ ] HTTPS certificate active
- [ ] Logs show no errors
- [ ] Test from mobile device
- [ ] Test from different browsers
- [ ] Monitoring/analytics configured

---

## 🎓 Best Practices

### Security

1. **Never commit `.env` files**
2. **Use environment variables for all secrets**
3. **Enable Vercel password protection during development**
4. **Use Supabase Row Level Security (RLS)**

### Performance

1. **Enable Vercel Analytics**
2. **Monitor function execution time**
3. **Optimize database queries**
4. **Use CDN for static assets**

### Reliability

1. **Test email fallback system**
2. **Monitor Supabase `email_notifications` table**
3. **Set up uptime monitoring (UptimeRobot, Pingdom)**
4. **Keep dependencies updated**

---

## 📞 Support

**Vercel Issues:**
- https://vercel.com/support
- https://vercel.com/docs

**Supabase Issues:**
- https://supabase.com/docs
- https://github.com/supabase/supabase/discussions

**Resend Issues:**
- https://resend.com/docs
- support@resend.com

---

## 🎉 Success!

Your booking system is now live on Vercel with:
- ✅ React frontend
- ✅ Node.js serverless backend
- ✅ Supabase database
- ✅ Resend email
- ✅ Email fallback system
- ✅ Production-ready error handling
- ✅ Comprehensive logging
- ✅ Custom domain (optional)

**Live URL:** `https://your-project.vercel.app`

Test it thoroughly and you're good to go! 🚀
