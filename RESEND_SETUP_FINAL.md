# ✅ RESEND EMAIL - SETUP GUIDE

## 🎯 CODE UPDATED - NOW USING RESEND

I've switched the code back to use **Resend** email service. This is the simplest setup!

---

## 🔑 WHERE TO ADD YOUR RESEND API KEY:

### Step 1: Get Your Resend API Key

1. Go to: **https://resend.com/login**
2. Log in to your Resend account
3. Click **"API Keys"** in the left sidebar
4. You should see your API key(s)
5. **Copy your API key** (starts with `re_`)

**Example API key:**
```
re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9
```

**If you don't have an API key yet:**
1. Click **"Create API Key"**
2. Give it a name (e.g., "Production")
3. Click **"Create"**
4. Copy the key immediately (you won't see it again!)

---

## 📋 ADD TO VERCEL ENVIRONMENT VARIABLES:

### Step 2: Add to Vercel

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

### Delete Old Variables First:

If you have Mailtrap variables, **delete them**:
- ❌ `MAILTRAP_HOST`
- ❌ `MAILTRAP_PORT`
- ❌ `MAILTRAP_USER`
- ❌ `MAILTRAP_PASSWORD`

### Add These 2 Variables:

#### Variable 1: RESEND_API_KEY
```
Key:   RESEND_API_KEY
Value: [paste your Resend API key here]
```
**Example:** `re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9`

✅ Check ALL 3 boxes: Production, Preview, Development

#### Variable 2: RECIPIENT_EMAIL
```
Key:   RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
```
✅ Check ALL 3 boxes: Production, Preview, Development

---

## 🎯 THAT'S IT - ONLY 2 VARIABLES!

**Resend is simpler than Mailtrap:**
- ✅ Only 2 environment variables needed
- ✅ No domain verification required
- ✅ Works immediately after adding API key

---

## 🚀 DEPLOYMENT STEPS:

### Step 3: Redeploy

1. Go to Vercel → **Deployments** tab
2. Click **three dots (•••)** on latest deployment
3. Click **"Redeploy"**
4. **UNCHECK** "Use existing Build Cache" ⚠️
5. Click **"Redeploy"**
6. Wait 2-3 minutes

### Step 4: Test

1. Visit: **https://www.optimuscustomz.com/**
2. Fill out the booking form
3. Click **"Submit Request"**
4. You should see: ✅ "Your request has been sent successfully!"
5. Check email: **elyonolawale@gmail.com**

---

## 📊 VERCEL ENVIRONMENT VARIABLES SHOULD LOOK LIKE:

```
Environment Variables:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RESEND_API_KEY = re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9
   [Production ✓] [Preview ✓] [Development ✓]

✅ RECIPIENT_EMAIL = elyonolawale@gmail.com
   [Production ✓] [Preview ✓] [Development ✓]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔍 HOW TO VERIFY IT'S WORKING:

### Check Vercel Logs:

Vercel → Functions → `/api/send.js` → View Logs

**Success looks like:**
```
📧 Booking email request received
✅ All required fields present
🔑 Environment check:
   Resend API Key: Present
   Sender Email: onboarding@resend.dev
   Recipient Email: elyonolawale@gmail.com
📨 Sending email via Resend API...
✅ Email sent successfully!
   Email ID: abc-123-def-456
```

**Failure looks like:**
```
❌ RESEND_API_KEY not found in environment variables
```

### Check Your Email:

Check **elyonolawale@gmail.com** inbox (and spam folder)

You should receive a beautiful HTML email with:
- Subject: "New Booking Request from [Customer Name]"
- All booking details nicely formatted
- Blue header with Optimus Design & Customs branding

---

## 🧪 QUICK TEST (Optional):

After deployment, test directly in browser console:

1. Visit: https://www.optimuscustomz.com/
2. Press **F12** → Console tab
3. Paste this code:

```javascript
fetch('/api/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Test User',
    email: 'test@example.com',
    phone: '555-1234',
    serviceType: 'vehicle-wrap',
    preferredDate: '2025-12-31',
    message: 'Testing Resend'
  })
})
.then(r => r.json())
.then(data => {
  console.log('Response:', data);
  if (data.success) {
    alert('✅ EMAIL SENT! Check elyonolawale@gmail.com');
  } else {
    alert('❌ Error: ' + data.message);
  }
});
```

**Expected:** Alert "EMAIL SENT!" and email in your inbox

---

## ⚠️ COMMON ISSUES:

### Issue: "RESEND_API_KEY not found"

**Fix:**
1. Make sure variable name is exactly `RESEND_API_KEY` (all caps, with underscores)
2. Check all 3 boxes are checked
3. Redeploy without build cache

### Issue: "401 Unauthorized" or "Invalid API key"

**Fix:**
1. Go back to Resend dashboard
2. Verify your API key is correct
3. Copy it again and update in Vercel
4. Make sure the key starts with `re_`

### Issue: Emails not arriving

**Fix:**
1. Check spam folder
2. Resend's default sender `onboarding@resend.dev` might go to spam
3. Emails from Resend are usually fast (within seconds)
4. Check Resend dashboard for delivery logs

### Issue: "Failed to send email"

**Fix:**
1. Check Vercel function logs for specific error
2. Make sure API key is valid
3. Verify you have Resend credits (free tier: 100 emails/day)

---

## 💡 OPTIONAL: CUSTOM SENDER EMAIL

If you want to use your own domain instead of `onboarding@resend.dev`:

### Add 3rd Variable (Optional):

```
Key:   SENDER_EMAIL
Value: bookings@optimuscustomz.com
```

**But you'll need to:**
1. Verify your domain in Resend dashboard
2. Add DNS records (similar to Mailtrap)

**For now, just use the default** (onboarding@resend.dev) - it works fine!

---

## 📋 QUICK CHECKLIST:

- [ ] Got Resend API key (starts with `re_`)
- [ ] Deleted old Mailtrap variables from Vercel
- [ ] Added `RESEND_API_KEY` to Vercel
- [ ] Added `RECIPIENT_EMAIL` to Vercel
- [ ] Checked all 3 boxes for both variables
- [ ] Redeployed without build cache
- [ ] Waited for deployment to complete
- [ ] Tested booking form
- [ ] Email received at elyonolawale@gmail.com

---

## ✅ SUMMARY:

**What You Need:**
1. Resend API key (from https://resend.com)
2. 2 environment variables in Vercel

**Variables:**
- `RESEND_API_KEY` = your API key
- `RECIPIENT_EMAIL` = elyonolawale@gmail.com

**Steps:**
1. Get API key from Resend
2. Add 2 variables to Vercel
3. Redeploy
4. Test!

---

## 🎉 BENEFITS OF RESEND:

- ✅ Simplest setup (only 2 variables)
- ✅ No domain verification needed (for basic use)
- ✅ Works immediately
- ✅ 100 emails/day free tier
- ✅ Fast delivery
- ✅ Clean, simple API

---

**This is the easiest email solution! Just add those 2 variables and redeploy.** 🚀
