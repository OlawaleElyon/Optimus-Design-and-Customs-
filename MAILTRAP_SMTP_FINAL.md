# ✅ MAILTRAP SMTP - FINAL SETUP GUIDE

## 🎯 CODE UPDATED - NOW USING SMTP (MATCHING YOUR SCREENSHOT)

I've switched the code to use **SMTP** credentials exactly as shown in your Mailtrap dashboard.

---

## 🔑 WHERE TO GET YOUR PASSWORD/API TOKEN:

### In Your Mailtrap Dashboard:

1. You're already on the right page (SMTP Credentials)
2. Look at the **"Password"** field
3. It shows: `<YOUR_API_TOKEN>`
4. **Click "Show"** or **"Copy"** button next to it
5. This will reveal your actual API token (long string)

**Your actual token looks like:**
```
1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
```

---

## 📋 ENVIRONMENT VARIABLES TO ADD IN VERCEL:

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

### Delete These First (if you have them):
- ❌ `MAILTRAP_Api`
- ❌ Any old variables with wrong names

### Add These 4 Variables:

#### Variable 1: MAILTRAP_HOST
```
Key:   MAILTRAP_HOST
Value: live.smtp.mailtrap.io
```
✅ Check: Production, Preview, Development

#### Variable 2: MAILTRAP_PORT
```
Key:   MAILTRAP_PORT
Value: 587
```
✅ Check: Production, Preview, Development

#### Variable 3: MAILTRAP_USER
```
Key:   MAILTRAP_USER
Value: api
```
✅ Check: Production, Preview, Development

#### Variable 4: MAILTRAP_PASSWORD
```
Key:   MAILTRAP_PASSWORD
Value: [paste your API token from Mailtrap]
```
**Important:** This is the password/token from the "Password" field in your screenshot
✅ Check: Production, Preview, Development

#### Variable 5: RECIPIENT_EMAIL
```
Key:   RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
```
✅ Check: Production, Preview, Development

---

## 🎯 EXACT MAPPING FROM YOUR SCREENSHOT:

| Mailtrap Field | Vercel Variable | Value |
|----------------|-----------------|-------|
| Host | `MAILTRAP_HOST` | `live.smtp.mailtrap.io` |
| Port | `MAILTRAP_PORT` | `587` |
| Username | `MAILTRAP_USER` | `api` |
| Password | `MAILTRAP_PASSWORD` | Your actual token |
| (recipient) | `RECIPIENT_EMAIL` | `elyonolawale@gmail.com` |

---

## 📸 HOW TO GET YOUR ACTUAL PASSWORD:

Looking at your screenshot, the Password field shows `<YOUR_API_TOKEN>`. This is a placeholder!

**To get the real password:**

### Option 1: Click "Show" Button
Look for an eye icon (👁️) or "Show" button next to the password field and click it.

### Option 2: Click "Copy" Button  
Look for a copy icon (📋) next to the password field and click it. This copies your actual token.

### Option 3: Regenerate Token
If you can't see the password:
1. Look for "Generate New Token" or "Reset Password" button
2. Click it to generate a new token
3. Copy the new token immediately

---

## 🚀 DEPLOYMENT STEPS:

### Step 1: Add All 5 Variables to Vercel
Make sure each variable has ALL 3 boxes checked!

### Step 2: Verify Your Variables Look Like This:

```
✅ MAILTRAP_HOST = live.smtp.mailtrap.io
   [Production ✓] [Preview ✓] [Development ✓]

✅ MAILTRAP_PORT = 587
   [Production ✓] [Preview ✓] [Development ✓]

✅ MAILTRAP_USER = api
   [Production ✓] [Preview ✓] [Development ✓]

✅ MAILTRAP_PASSWORD = [your long token string]
   [Production ✓] [Preview ✓] [Development ✓]

✅ RECIPIENT_EMAIL = elyonolawale@gmail.com
   [Production ✓] [Preview ✓] [Development ✓]
```

### Step 3: Redeploy

1. Vercel → **Deployments** tab
2. Click **three dots (•••)** on latest deployment
3. Click **"Redeploy"**
4. **UNCHECK** "Use existing Build Cache" ⚠️
5. Click **"Redeploy"**
6. Wait 2-3 minutes

### Step 4: Test

1. Visit: https://www.optimuscustomz.com/
2. Fill booking form
3. Submit
4. Check: elyonolawale@gmail.com

---

## 🔍 HOW TO VERIFY IT'S WORKING:

### Check Vercel Logs:
Vercel → Functions → `/api/send.js` → View Logs

**Success looks like:**
```
📧 Booking email request received
✅ All required fields present
🔑 Environment check:
   SMTP Host: live.smtp.mailtrap.io
   SMTP Port: 587
   SMTP User: api
   SMTP Password: Present
📨 Sending email via Mailtrap SMTP...
✅ Email sent successfully!
```

**Failure looks like:**
```
❌ MAILTRAP_PASSWORD not found in environment variables
```

### Check Mailtrap Dashboard:
Mailtrap → Sending → Email Logs
- You should see your sent email
- Status: Delivered

---

## ⚠️ COMMON MISTAKES:

### ❌ Mistake 1: Using "<YOUR_API_TOKEN>" as the password
**Fix:** That's a placeholder! Click "Show" or "Copy" to get the REAL token

### ❌ Mistake 2: Not checking all 3 environment boxes
**Fix:** Must check Production, Preview, AND Development for each variable

### ❌ Mistake 3: Not redeploying after adding variables
**Fix:** Always redeploy (without build cache) after changing variables

### ❌ Mistake 4: Wrong variable names
**Fix:** Use EXACT names:
- `MAILTRAP_PASSWORD` (not `MAILTRAP_Pass` or `MAILTRAP_Api`)
- `MAILTRAP_HOST` (not `MAILTRAP_Host`)
- `MAILTRAP_PORT` (not `MAILTRAP_Port`)
- `MAILTRAP_USER` (not `MAILTRAP_Username`)

---

## 🎯 QUICK CHECKLIST:

- [ ] Found actual API token in Mailtrap (not the placeholder)
- [ ] Added 5 variables to Vercel with EXACT names
- [ ] Checked all 3 boxes for each variable
- [ ] Redeployed without build cache
- [ ] Waited for deployment to complete
- [ ] Tested booking form
- [ ] Email received at elyonolawale@gmail.com

---

## 📞 STILL NOT WORKING?

### If you see "MAILTRAP_PASSWORD not found":
- Double-check the variable name is exactly `MAILTRAP_PASSWORD`
- Make sure Production box is checked
- Redeploy without build cache

### If you see "Authentication failed":
- Your API token might be wrong
- Go back to Mailtrap and copy it again
- Make sure you copied the actual token (not `<YOUR_API_TOKEN>`)

### If emails not arriving:
- Check spam folder
- Check Mailtrap Email Logs for delivery status
- Verify domain is verified in Mailtrap

---

## ✅ SUMMARY:

**Variables Needed: 5 total**
1. MAILTRAP_HOST
2. MAILTRAP_PORT  
3. MAILTRAP_USER
4. MAILTRAP_PASSWORD (your actual API token)
5. RECIPIENT_EMAIL

**Critical Steps:**
1. Get REAL API token from Mailtrap (not placeholder)
2. Add all 5 variables with exact names
3. Check all 3 boxes for each
4. Redeploy without build cache
5. Test!

---

**The code is ready - just add those 5 variables and redeploy!** 🚀
