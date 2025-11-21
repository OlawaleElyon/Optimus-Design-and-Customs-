# 🚀 Vercel Deployment - Booking Form Setup Guide

## ✅ Issue Fixed!

I've identified and fixed a bug in the `/api/send.js` serverless function. The Resend API response structure was not being handled correctly.

**What was fixed:**
- The Resend API returns `{ data: { id }, error }` but the code was trying to access `data.id` directly
- Added proper error handling for Resend API errors
- Now correctly extracts the email ID from `result.data.id`

## 📋 Next Steps: Configure Vercel Environment Variables

Since the code is now working locally, the issue on your live site is that **Vercel doesn't have the required environment variables**. Here's how to fix it:

### Step 1: Add Environment Variables in Vercel

1. **Go to your Vercel Dashboard**: https://vercel.com/dashboard
2. **Select your project**: "optimuscustomz" (or whatever your project is named)
3. **Click "Settings"** in the top navigation
4. **Click "Environment Variables"** in the left sidebar
5. **Add these 3 variables** (click "Add New" for each):

#### Variable 1: RESEND_API_KEY
```
Name: RESEND_API_KEY
Value: re_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9
Environments: ✓ Production ✓ Preview ✓ Development
```

#### Variable 2: RESEND_SENDER_EMAIL
```
Name: RESEND_SENDER_EMAIL
Value: onboarding@resend.dev
Environments: ✓ Production ✓ Preview ✓ Development
```

#### Variable 3: RECIPIENT_EMAIL
```
Name: RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
Environments: ✓ Production ✓ Preview ✓ Development
```

**Important:** Make sure to check **ALL THREE boxes** for each variable:
- ✅ Production
- ✅ Preview  
- ✅ Development

### Step 2: Redeploy Your Site

After adding the environment variables, you MUST redeploy for changes to take effect:

1. Go to **"Deployments"** tab in Vercel
2. Click on the **latest deployment**
3. Click the **three dots (•••)** menu
4. Click **"Redeploy"**
5. **IMPORTANT:** Make sure **"Use existing Build Cache"** is **UNCHECKED**
6. Click **"Redeploy"**
7. Wait 2-3 minutes for deployment to complete

### Step 3: Test Your Booking Form

1. Visit your live site: https://www.optimuscustomz.com/
2. Scroll to the booking form
3. Fill out all required fields
4. Click "Submit Request"
5. You should see: ✅ "Your request has been sent successfully!"
6. Check your email: elyonolawale@gmail.com

## 🧪 Verify the Fix is Deployed

You can verify the API is working by opening your browser console (F12) and running:

```javascript
fetch('https://www.optimuscustomz.com/api/send', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Test User',
    email: 'test@example.com',
    phone: '555-0000',
    serviceType: 'vehicle-wrap',
    preferredDate: '2025-12-25',
    message: 'Testing from console'
  })
})
.then(r => r.json())
.then(data => {
  console.log('✅ Response:', data);
  if (data.success && data.email_id) {
    console.log('✅ EMAIL SENT! ID:', data.email_id);
  }
})
.catch(err => console.error('❌ Error:', err));
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Booking email sent successfully",
  "email_id": "some-uuid-here"
}
```

## 📊 What Changed in the Code

### Before (Buggy):
```javascript
const data = await resend.emails.send({...});
console.log('Email sent successfully:', data.id); // ❌ data.id was undefined
return res.status(200).json({
  success: true,
  email_id: data.id // ❌ Always undefined
});
```

### After (Fixed):
```javascript
const result = await resend.emails.send({...});

// ✅ Check for errors from Resend API
if (result.error) {
  throw new Error(result.error.message || 'Failed to send email');
}

// ✅ Correctly access the ID from result.data.id
console.log('Email sent successfully:', result.data);
return res.status(200).json({
  success: true,
  email_id: result.data?.id // ✅ Now returns the actual email ID
});
```

## 🔍 How to Check Vercel Function Logs (Optional)

If you want to see the real-time logs:

1. Go to your Vercel Dashboard
2. Click **"Functions"** tab
3. Look for `/api/send.js`
4. Click **"View Logs"** or **"Real-time Logs"**
5. Submit a form on your website
6. You should see: "Email sent successfully: { id: 'xxx-xxx-xxx' }"

## ⚠️ Common Issues

### Issue: Still getting "failed to send message"
**Solution:** 
- Double-check that you added ALL 3 environment variables
- Make sure you redeployed AFTER adding them
- Verify you unchecked "Use existing Build Cache" when redeploying

### Issue: "Email service not configured" error
**Solution:**
- The `RESEND_API_KEY` environment variable is missing or incorrect
- Go back to Step 1 and verify it's set correctly

### Issue: No error, but emails not arriving
**Solution:**
- Check your spam/junk folder
- The default sender is `onboarding@resend.dev` which might trigger spam filters
- Emails may take a few minutes to arrive

## ✅ Summary

1. **Code bug fixed** ✅ (Resend API response handling)
2. **Local testing passed** ✅ (Email sending works)
3. **Next:** Add environment variables in Vercel
4. **Then:** Redeploy your site
5. **Finally:** Test the booking form on your live site

Your booking form should work perfectly after you complete Step 1 and Step 2! 🎉

---

**Questions?** If the form still doesn't work after following these steps, please:
1. Screenshot the browser console (F12 → Console) when submitting the form
2. Screenshot the Vercel environment variables page
3. Let me know what error message you see
