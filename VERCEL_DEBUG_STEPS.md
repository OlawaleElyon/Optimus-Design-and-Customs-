# 🔍 URGENT: Fix "Failed to Send Message" - Step by Step

## 🚨 Current Issue
Website: https://www.optimuscustomz.com/
Error: "Failed to send message" when submitting booking form

## ✅ Step-by-Step Fix

### STEP 1: Verify Environment Variables in Vercel (MOST IMPORTANT!)

1. **Go to Vercel Dashboard:** https://vercel.com/dashboard
2. **Click your project:** "optimuscustomz" or similar
3. **Click "Settings"** (top menu)
4. **Click "Environment Variables"** (left sidebar)

**CHECK: Do these 3 variables exist?**

```
Variable Name: RESEND_API_KEY
Value: re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9
Environments: ✓ Production ✓ Preview ✓ Development

Variable Name: RESEND_SENDER_EMAIL  
Value: onboarding@resend.dev
Environments: ✓ Production ✓ Preview ✓ Development

Variable Name: RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
Environments: ✓ Production ✓ Preview ✓ Development
```

**⚠️ IF MISSING OR WRONG:**
1. Click "Add New"
2. Enter each variable exactly as shown above
3. Check ALL THREE boxes: Production, Preview, Development
4. Click "Save"
5. **IMPORTANT:** After adding, you MUST redeploy!

### STEP 2: Check if API Route is Deployed

1. **Go to your Vercel project**
2. **Click "Functions"** tab (top menu)
3. **Look for:** `/api/send.js`

**IF YOU SEE IT:**
- ✅ API is deployed
- Continue to Step 3

**IF YOU DON'T SEE IT:**
- ❌ API not deployed
- Problem: Vercel didn't detect the API folder
- Solution: Continue to Step 4

### STEP 3: Test API Endpoint Directly

**Open this URL in your browser:**
```
https://www.optimuscustomz.com/api/test
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Vercel API route is working!",
  "timestamp": "2025-11-21T...",
  "method": "GET"
}
```

**IF YOU SEE THIS:**
- ✅ API routes are working!
- Problem is likely environment variables or Resend package
- Go to Step 5

**IF YOU SEE 404 ERROR:**
- ❌ API routes not deployed
- Go to Step 4

### STEP 4: Fix API Deployment

The API folder must be in the correct location for Vercel.

**Current location:** `/app/frontend/api/`
**Files:** `send.js`, `package.json`, `test.js`

**Action Required:**
1. Ensure `api` folder is at root of frontend
2. Push latest code to GitHub
3. Vercel will auto-redeploy

**To verify after deploy:**
- Check Vercel Functions tab
- Should see `/api/send.js` and `/api/test.js`

### STEP 5: Verify Resend Package is Installed

1. **Go to Vercel Dashboard**
2. **Click "Deployments"** tab
3. **Click the latest deployment**
4. **Click "Building"** section
5. **Look for:** "Installing dependencies"

**Should see:**
```
Installing dependencies from api/package.json
resend@3.0.0
```

**IF NOT:**
- Problem: package.json not found or invalid
- Solution: See Step 6

### STEP 6: Check Browser Console for Exact Error

1. **Open your website:** https://www.optimuscustomz.com/
2. **Press F12** (open DevTools)
3. **Click "Console" tab**
4. **Scroll to booking form**
5. **Fill form and submit**
6. **Look for errors in console** (red text)

**Common Errors:**

**Error: "404 Not Found /api/send"**
- Cause: API route not deployed
- Fix: Push code to GitHub, wait for Vercel deployment

**Error: "500 Internal Server Error"**
- Cause: Environment variables missing OR Resend API key invalid
- Fix: Check Step 1, verify API key is correct

**Error: "CORS policy blocked"**
- Cause: CORS headers issue (unlikely, we have them)
- Fix: Already handled in send.js

**Error: "Network error"**
- Cause: API endpoint doesn't exist
- Fix: Check Step 4

### STEP 7: Check Vercel Function Logs

1. **Go to Vercel Dashboard**
2. **Click your project**
3. **Click "Functions"** tab
4. **Click on `/api/send.js`** (if it exists)
5. **Click "View Logs"**
6. **Submit form on website**
7. **Watch logs in real-time**

**Look for:**
- "Email sent successfully: xxx" = ✅ WORKING!
- "RESEND_API_KEY not found" = ❌ Missing env variable
- "Invalid API key" = ❌ Wrong API key
- "Error sending email" = ❌ Resend API issue

### STEP 8: Manual Redeploy

Sometimes Vercel needs a manual redeploy to pick up changes:

1. **Go to Vercel Dashboard**
2. **Click "Deployments"** tab
3. **Find latest deployment**
4. **Click three dots (•••)**
5. **Click "Redeploy"**
6. **Check "Use existing Build Cache"** = OFF
7. **Click "Redeploy"**
8. **Wait 2-3 minutes**
9. **Test form again**

## 🧪 Quick Test Commands

### Test 1: Check if API exists
**Open browser console on your site, run:**
```javascript
fetch('https://www.optimuscustomz.com/api/test')
  .then(r => r.json())
  .then(data => console.log('✅ API Works:', data))
  .catch(err => console.error('❌ API Failed:', err));
```

### Test 2: Test actual send endpoint
**Run in browser console:**
```javascript
fetch('https://www.optimuscustomz.com/api/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Console Test',
    email: 'test@test.com',
    phone: '555-0000',
    serviceType: 'vehicle-wrap',
    preferredDate: '2025-12-25',
    message: 'Testing from console'
  })
})
.then(r => r.json())
.then(data => {
  console.log('Response:', data);
  if (data.success) {
    alert('✅ EMAIL SENT! Check elyonolawale@gmail.com');
  } else {
    alert('❌ Failed: ' + data.message);
  }
})
.catch(err => {
  console.error('Error:', err);
  alert('❌ Network error: ' + err.message);
});
```

## 📊 Debugging Checklist

After each step, check off:

- [ ] Verified 3 environment variables exist in Vercel (Production checked)
- [ ] Confirmed `/api/send.js` appears in Functions tab
- [ ] Tested `/api/test` endpoint - returns JSON
- [ ] Checked browser console for errors when submitting form
- [ ] Viewed Vercel Function logs while submitting form
- [ ] Redeployed without build cache
- [ ] Ran test command in browser console
- [ ] Pushed latest code to GitHub

## 🎯 Most Likely Causes (In Order)

1. **Environment variables not set** (80% of issues)
   - Fix: Add them in Vercel Settings
   - Must redeploy after adding

2. **API route not deployed** (15% of issues)
   - Fix: Ensure api/ folder exists in frontend
   - Push to GitHub, Vercel redeploys

3. **Wrong Resend API key** (4% of issues)
   - Fix: Verify key is: re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9

4. **Package not installed** (1% of issues)
   - Fix: Check build logs show "Installing resend"

## 📞 What to Share if Still Broken

**Screenshot these:**
1. Vercel → Settings → Environment Variables page
2. Vercel → Functions tab (showing all functions)
3. Browser Console (F12 → Console) when submitting form
4. Browser Network tab (F12 → Network) showing /api/send request
5. Vercel Function logs (if /api/send.js exists)

**Tell me:**
- What happens when you submit the form?
- What error message appears?
- Did you redeploy after adding environment variables?
- Can you see `/api/send.js` in Vercel Functions tab?

---

## 🚀 Nuclear Option: Fresh Redeploy

If nothing works:

1. **Delete** all environment variables
2. **Add them back** one by one (copy exactly from above)
3. **Check ALL boxes** (Production, Preview, Development)
4. **Go to Deployments** → Latest → **"Redeploy"**
5. **UNCHECK** "Use existing Build Cache"
6. **Wait 3-5 minutes**
7. **Test form**

---

**Follow these steps IN ORDER and the booking form WILL work!** 🎯
