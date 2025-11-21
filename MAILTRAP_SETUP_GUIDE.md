# 📧 MAILTRAP SETUP GUIDE

## ✅ CODE UPDATED - NOW USING MAILTRAP

I've successfully switched your booking form from Resend to Mailtrap!

---

## 🔧 WHAT I CHANGED:

### 1. Updated Dependencies
**Before**: Used `resend` package  
**After**: Uses `nodemailer` package (industry standard for email)

### 2. Updated `/frontend/api/send.js`
- ✅ Replaced Resend API with Mailtrap SMTP
- ✅ Uses nodemailer to send emails
- ✅ Same beautiful HTML email template
- ✅ Enhanced logging for debugging

---

## 🎯 HOW TO GET MAILTRAP CREDENTIALS

### Step 1: Sign Up for Mailtrap

1. Go to: **https://mailtrap.io/**
2. Click **"Sign Up"** or **"Start Free Trial"**
3. Create your account (free tier available)

### Step 2: Choose the RIGHT Product

⚠️ **IMPORTANT**: Mailtrap has TWO products:

1. **Email Testing** (for development/testing only) ❌
2. **Email Sending** (for production - THIS IS WHAT YOU NEED) ✅

**Select "Email Sending" or "Sending Domains"**

### Step 3: Set Up Your Sending Domain

Mailtrap requires you to verify a domain to send emails. You have 2 options:

#### Option A: Use Your Own Domain (Recommended)

If you own **optimuscustomz.com**:

1. Go to **Mailtrap Dashboard** → **Sending Domains**
2. Click **"Add Domain"**
3. Enter your domain: `optimuscustomz.com`
4. Mailtrap will provide DNS records to add
5. Add these DNS records to your domain (at your domain registrar):
   - **TXT record** for verification
   - **CNAME records** for DKIM
   - **TXT record** for SPF
6. Wait for verification (can take 15 minutes to 24 hours)
7. Once verified, you can send from emails like:
   - `bookings@optimuscustomz.com`
   - `noreply@optimuscustomz.com`

#### Option B: Use Mailtrap Shared Domain (Quick Start)

If you don't have domain access:

1. Mailtrap provides a shared domain for testing
2. You can send from: `your-username@sending.mailtrap.live`
3. **Note**: Emails might go to spam with shared domains

### Step 4: Get SMTP Credentials

1. In Mailtrap Dashboard, go to **Sending Domains**
2. Click on your verified domain
3. Click **"SMTP Settings"** or **"Integration"**
4. You'll see credentials like this:

```
Host: live.smtp.mailtrap.io
Port: 587 (or 2525)
Username: api
Password: [long random string]
```

**Copy these credentials** - you'll need them for Vercel!

---

## 🔑 ENVIRONMENT VARIABLES FOR VERCEL

### Variables You Need to Add:

Go to **Vercel Dashboard** → **Your Project** → **Settings** → **Environment Variables**

Add these **5 variables**:

### Variable 1: MAILTRAP_HOST
```
Key:   MAILTRAP_HOST
Value: live.smtp.mailtrap.io
```
✅ Check all 3 boxes: Production, Preview, Development

### Variable 2: MAILTRAP_PORT
```
Key:   MAILTRAP_PORT
Value: 587
```
✅ Check all 3 boxes: Production, Preview, Development

### Variable 3: MAILTRAP_USER
```
Key:   MAILTRAP_USER
Value: [Your Mailtrap username - usually "api"]
```
✅ Check all 3 boxes: Production, Preview, Development

### Variable 4: MAILTRAP_PASS
```
Key:   MAILTRAP_PASS
Value: [Your Mailtrap password - long random string]
```
✅ Check all 3 boxes: Production, Preview, Development

### Variable 5: SENDER_EMAIL
```
Key:   SENDER_EMAIL
Value: bookings@optimuscustomz.com
```
(Or whatever email you verified in Mailtrap)
✅ Check all 3 boxes: Production, Preview, Development

### Variable 6: RECIPIENT_EMAIL (Same as Before)
```
Key:   RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
```
✅ Check all 3 boxes: Production, Preview, Development

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Remove Old Resend Variables (Optional but Recommended)

1. Go to Vercel → Settings → Environment Variables
2. Find and **delete** these old variables:
   - `RESEND_API_KEY`
   - `RESEND_SENDER_EMAIL`

### Step 2: Add New Mailtrap Variables

Add all 6 variables listed above.

### Step 3: Push Updated Code to GitHub

```bash
cd /app/frontend
git add .
git commit -m "Switch from Resend to Mailtrap"
git push
```

Or if you're deploying from Emergent, the code is already updated!

### Step 4: Redeploy on Vercel

1. Go to **Vercel Dashboard** → **Deployments**
2. Click **three dots (•••)** on latest deployment
3. Click **"Redeploy"**
4. **UNCHECK** "Use existing Build Cache"
5. Click **Redeploy**
6. Wait 2-3 minutes

---

## 🧪 HOW TO TEST

### Test 1: Submit Booking Form

1. Go to: **https://www.optimuscustomz.com/**
2. Fill out the booking form
3. Click **"Submit Request"**
4. You should see: ✅ "Your request has been sent successfully!"
5. Check: **elyonolawale@gmail.com** for the email

### Test 2: Check Mailtrap Dashboard

1. Go to **Mailtrap Dashboard**
2. Click **"Sending"** → **"Email Logs"**
3. You should see your sent email listed
4. Click on it to see delivery status

### Test 3: Check Vercel Logs

1. Vercel Dashboard → Functions → `/api/send.js` → View Logs
2. Submit a booking
3. Look for:

**Success:**
```
📧 Booking email request received
✅ All required fields present
🔑 Environment check:
   Mailtrap Host: live.smtp.mailtrap.io
   Mailtrap Port: 587
   Mailtrap User: Present
   Mailtrap Pass: Present
📨 Sending email via Mailtrap...
✅ Email sent successfully!
```

**Failure:**
```
❌ Mailtrap credentials not found in environment variables
```

---

## 📊 COMPARISON: RESEND vs MAILTRAP

| Feature | Resend | Mailtrap |
|---------|--------|----------|
| **Setup** | API key only | Domain verification required |
| **Free Tier** | 100 emails/day | 1,000 emails/month |
| **Delivery** | Fast | Fast |
| **Email Testing** | No built-in testing | Built-in email testing sandbox |
| **Analytics** | Yes | Yes |
| **SMTP** | No (API only) | Yes |
| **Domain Required** | Optional | Required for production |

---

## ⚠️ IMPORTANT NOTES

### 1. Domain Verification is REQUIRED

You **must** verify a domain in Mailtrap to send production emails. Without verification:
- Emails will fail to send
- You'll see authentication errors in logs

### 2. DNS Records Take Time

After adding DNS records for domain verification:
- Can take 15 minutes to 24 hours
- Check verification status in Mailtrap dashboard
- Don't deploy until domain is verified

### 3. Sender Email Must Match Verified Domain

If you verified `optimuscustomz.com`, your sender email MUST be:
- ✅ `bookings@optimuscustomz.com`
- ✅ `noreply@optimuscustomz.com`
- ❌ NOT `onboarding@resend.dev` (old Resend email)

### 4. Port Options

Mailtrap supports multiple ports:
- **587** (recommended - TLS)
- **2525** (alternative)
- **465** (SSL - not recommended for Vercel)

Use **587** unless you have issues.

---

## 🔍 TROUBLESHOOTING

### Issue: "Mailtrap credentials not found"

**Cause**: Environment variables not set in Vercel

**Solution**:
1. Add all 6 environment variables
2. Check ALL 3 boxes for each
3. Redeploy without build cache

### Issue: "Authentication failed"

**Cause**: Wrong username/password or domain not verified

**Solution**:
1. Double-check Mailtrap credentials
2. Make sure domain is verified (green checkmark in Mailtrap)
3. Wait if DNS records were just added

### Issue: Emails not arriving

**Cause**: Multiple possibilities

**Solution**:
1. Check spam folder
2. Check Mailtrap Email Logs for delivery status
3. Verify sender email matches verified domain
4. Check Vercel logs for errors

### Issue: "ECONNECTION timeout"

**Cause**: Vercel can't connect to Mailtrap SMTP server

**Solution**:
1. Verify `MAILTRAP_HOST` is: `live.smtp.mailtrap.io`
2. Verify `MAILTRAP_PORT` is: `587`
3. Check if Mailtrap service is operational

---

## 📋 QUICK CHECKLIST

- [ ] Signed up for Mailtrap account
- [ ] Selected "Email Sending" product (not Email Testing)
- [ ] Added and verified domain in Mailtrap
- [ ] Got SMTP credentials (host, port, username, password)
- [ ] Added 6 environment variables to Vercel
- [ ] Checked all 3 boxes for each variable
- [ ] Removed old Resend variables (optional)
- [ ] Pushed updated code to GitHub
- [ ] Redeployed on Vercel (without build cache)
- [ ] Tested booking form on live site
- [ ] Confirmed email received at elyonolawale@gmail.com
- [ ] Checked Mailtrap dashboard for delivery status

---

## ✅ SUMMARY

**What Changed:**
- ❌ Removed Resend API
- ✅ Added Mailtrap SMTP with nodemailer
- ✅ Same email functionality
- ✅ Same beautiful HTML email

**What You Need to Do:**
1. Sign up for Mailtrap
2. Verify your domain
3. Get SMTP credentials
4. Add 6 environment variables to Vercel
5. Redeploy

**Total Setup Time:** 30-60 minutes (mostly waiting for domain verification)

---

## 🎯 NEXT STEPS

1. **Now**: Sign up for Mailtrap → https://mailtrap.io/
2. **Verify domain**: Add DNS records (wait for verification)
3. **Get credentials**: Copy SMTP username and password
4. **Add to Vercel**: 6 environment variables
5. **Redeploy**: Push code and redeploy on Vercel
6. **Test**: Submit booking form

Your booking emails will work perfectly with Mailtrap! 🎉

---

**Need help with domain verification or DNS records? Let me know!**
