# 🚀 MAILTRAP HTTP API SETUP (SIMPLIFIED)

## ✅ CODE UPDATED - NOW USING MAILTRAP HTTP API

I've updated the code to use Mailtrap's **HTTP API** instead of SMTP. This is **much simpler**!

---

## 🎯 WHAT CHANGED:

### Before (SMTP Method):
- Needed: Host, Port, Username, Password
- Used: nodemailer package
- 6 environment variables

### After (HTTP API Method):
- Needs: Just API Token
- Uses: Direct HTTP calls
- **Only 3 environment variables!** ✅

**This is MUCH easier!**

---

## 📋 HOW TO GET YOUR MAILTRAP API TOKEN:

### Step 1: Log into Mailtrap

Go to: **https://mailtrap.io/signin**

---

### Step 2: Get Your API Token

**Option A: From API Tokens Page**
1. Click your profile/avatar (top-right)
2. Click **"API Tokens"** or **"Settings"**
3. Look for **"API Tokens"** section
4. Click **"Generate New Token"** or copy existing token
5. Copy the token (long string like: `abc123def456...`)

**Option B: From Sending Domains**
1. Click **"Sending Domains"** (left sidebar)
2. Click your domain (e.g., `optimuscustomz.com`)
3. Look for **"API Token"** or **"Integration"** tab
4. Copy the API token

**The token looks like:**
```
1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

---

## 🔑 UPDATED ENVIRONMENT VARIABLES FOR VERCEL:

### You Now Need ONLY 3 Variables (instead of 6!):

Go to: **Vercel Dashboard** → **Your Project** → **Settings** → **Environment Variables**

### Variable 1: MAILTRAP_API_TOKEN
```
Key:   MAILTRAP_API_TOKEN
Value: [paste your API token here]
```
✅ Check: Production, Preview, Development

### Variable 2: SENDER_EMAIL
```
Key:   SENDER_EMAIL
Value: hello@optimuscustomz.com
```
(Must be from your verified domain in Mailtrap)
✅ Check: Production, Preview, Development

### Variable 3: RECIPIENT_EMAIL
```
Key:   RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
```
✅ Check: Production, Preview, Development

---

## 🗑️ REMOVE OLD VARIABLES:

If you added these earlier, **delete them** (not needed anymore):
- ❌ `MAILTRAP_HOST`
- ❌ `MAILTRAP_PORT`
- ❌ `MAILTRAP_USER`
- ❌ `MAILTRAP_PASS`

Keep only the 3 variables listed above!

---

## 📊 COMPARISON:

| Method | Variables Needed | Complexity |
|--------|-----------------|------------|
| SMTP (old) | 6 variables | Complex |
| HTTP API (new) | **3 variables** | **Simple** ✅ |

---

## 🚀 DEPLOYMENT STEPS:

### Step 1: Clean Up Environment Variables

1. Go to Vercel → Settings → Environment Variables
2. **Delete** old SMTP variables (if you added them):
   - `MAILTRAP_HOST`
   - `MAILTRAP_PORT`
   - `MAILTRAP_USER`
   - `MAILTRAP_PASS`

### Step 2: Add New Variables

Add these 3 variables:
1. `MAILTRAP_API_TOKEN` = [your API token]
2. `SENDER_EMAIL` = `hello@optimuscustomz.com`
3. `RECIPIENT_EMAIL` = `elyonolawale@gmail.com`

### Step 3: Redeploy

1. Vercel → Deployments → Click **•••**
2. Click **"Redeploy"**
3. **UNCHECK** "Use existing Build Cache"
4. Wait 2-3 minutes

### Step 4: Test

Visit your live site and submit a booking!

---

## 🧪 QUICK API TEST:

After deployment, test with browser console:

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
    message: 'Testing Mailtrap API'
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

---

## 🔍 HOW TO VERIFY:

### 1. Check Vercel Logs

Vercel → Functions → `/api/send.js` → View Logs

**Success looks like:**
```
📧 Booking email request received
✅ All required fields present
🔑 Environment check:
   API Token: Present
📨 Sending email via Mailtrap API...
✅ Email sent successfully!
```

### 2. Check Mailtrap Dashboard

Mailtrap → **Sending** → **Email Logs**

You should see your sent email with:
- Status: Delivered
- Subject: "New Booking Request from [name]"
- Recipient: elyonolawale@gmail.com

### 3. Check Your Email

Check **elyonolawale@gmail.com** inbox (and spam folder).

---

## ⚠️ IMPORTANT NOTES:

### 1. Domain Must Be Verified

Even with the HTTP API, you must verify your domain in Mailtrap:
- Go to Mailtrap → Sending Domains
- Add `optimuscustomz.com`
- Add DNS records (TXT, CNAME)
- Wait for verification (green ✓)

### 2. Sender Email Must Match Domain

Your `SENDER_EMAIL` must be from the verified domain:
- ✅ `hello@optimuscustomz.com`
- ✅ `bookings@optimuscustomz.com`
- ✅ `noreply@optimuscustomz.com`
- ❌ `test@gmail.com` (not your domain)

### 3. API Token vs SMTP Credentials

**API Token:**
- Used for HTTP API (what we're using now)
- Single token for authentication
- Simpler setup

**SMTP Credentials:**
- Used for SMTP email (old method)
- Needs host, port, username, password
- More complex

We're using the **API Token** method now! ✅

---

## 🆘 TROUBLESHOOTING:

### Error: "Mailtrap API token missing"

**Fix:**
1. Add `MAILTRAP_API_TOKEN` to Vercel
2. Check all 3 boxes (Production, Preview, Development)
3. Redeploy without build cache

### Error: "401 Unauthorized"

**Fix:**
1. Verify API token is correct (copy from Mailtrap dashboard)
2. Make sure domain is verified in Mailtrap
3. Check token hasn't expired

### Error: "422 Unprocessable Entity"

**Fix:**
1. Verify sender email matches verified domain
2. Check recipient email is valid
3. Make sure all required fields are present

### Email Not Arriving

**Check:**
1. Spam folder
2. Mailtrap Email Logs for delivery status
3. Recipient email address is correct
4. Domain is verified in Mailtrap

---

## 📋 FINAL CHECKLIST:

- [ ] Got Mailtrap API token
- [ ] Domain verified in Mailtrap (green ✓)
- [ ] Deleted old SMTP variables from Vercel
- [ ] Added 3 new variables to Vercel
- [ ] Checked all 3 boxes for each variable
- [ ] Redeployed without build cache
- [ ] Tested booking form on live site
- [ ] Email received at elyonolawale@gmail.com
- [ ] Checked Mailtrap Email Logs

---

## ✅ SUMMARY:

**What You Need:**
1. Mailtrap API Token (from Mailtrap dashboard)
2. Verified domain in Mailtrap
3. 3 environment variables in Vercel

**What Changed:**
- ✅ Simpler setup (3 variables instead of 6)
- ✅ Faster API calls
- ✅ Better error handling
- ✅ Same beautiful HTML emails

**Next Steps:**
1. Get your API token from Mailtrap
2. Add 3 environment variables to Vercel
3. Redeploy
4. Test!

---

**This is the EASIEST way to use Mailtrap!** 🎉
