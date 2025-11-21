# ⚡ MAILTRAP QUICK START

## ✅ CODE IS UPDATED - NOW READY FOR MAILTRAP

---

## 🎯 WHAT TO DO (5 STEPS):

### 1️⃣ Sign Up for Mailtrap (5 minutes)

Go to: **https://mailtrap.io/register/signup**
- Create account (free tier available)
- Select **"Email Sending"** product (NOT Email Testing)

---

### 2️⃣ Verify Your Domain (30-60 minutes)

**If you own optimuscustomz.com:**

1. Mailtrap Dashboard → **Sending Domains** → **Add Domain**
2. Enter: `optimuscustomz.com`
3. Mailtrap shows DNS records to add
4. Go to your domain registrar (GoDaddy, Namecheap, etc.)
5. Add the DNS records:
   - TXT record (verification)
   - CNAME records (DKIM)
   - TXT record (SPF)
6. Wait 15 mins - 24 hours for verification

**Don't have domain access?**
- Use Mailtrap shared domain (emails may go to spam)
- Or contact your domain administrator

---

### 3️⃣ Get SMTP Credentials (2 minutes)

1. Mailtrap Dashboard → **Sending Domains**
2. Click your verified domain
3. Click **"SMTP Settings"**
4. Copy these values:

```
Host:     live.smtp.mailtrap.io
Port:     587
Username: api
Password: [long string - copy this!]
```

---

### 4️⃣ Add to Vercel (5 minutes)

**Vercel Dashboard** → **Your Project** → **Settings** → **Environment Variables**

Add these 6 variables (click "Add New" for each):

| Key | Value | Environments |
|-----|-------|-------------|
| `MAILTRAP_HOST` | `live.smtp.mailtrap.io` | ✅ All 3 boxes |
| `MAILTRAP_PORT` | `587` | ✅ All 3 boxes |
| `MAILTRAP_USER` | `api` | ✅ All 3 boxes |
| `MAILTRAP_PASS` | `[your password from step 3]` | ✅ All 3 boxes |
| `SENDER_EMAIL` | `bookings@optimuscustomz.com` | ✅ All 3 boxes |
| `RECIPIENT_EMAIL` | `elyonolawale@gmail.com` | ✅ All 3 boxes |

⚠️ **Must check ALL 3 boxes** (Production, Preview, Development) for each!

---

### 5️⃣ Redeploy (2 minutes)

1. Vercel → **Deployments** → Click **•••** → **Redeploy**
2. **UNCHECK** "Use existing Build Cache"
3. Wait 2-3 minutes
4. **Test**: Submit booking form on your live site
5. **Check**: Email arrives at elyonolawale@gmail.com

---

## 🧪 QUICK TEST

After deployment, test with browser console:

1. Visit: **https://www.optimuscustomz.com/**
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
    message: 'Testing Mailtrap'
  })
})
.then(r => r.json())
.then(data => {
  if (data.success) {
    alert('✅ EMAIL SENT! Check elyonolawale@gmail.com');
  } else {
    alert('❌ Error: ' + data.message);
  }
});
```

**Expected**: Alert "EMAIL SENT!" and email in inbox.

---

## ⚠️ COMMON ISSUES

### "Mailtrap credentials not found"
→ Add environment variables to Vercel, then redeploy

### "Authentication failed"  
→ Check domain is verified (green checkmark in Mailtrap)

### Emails not arriving
→ Check spam folder + Mailtrap Email Logs for delivery status

---

## 📋 CHECKLIST

- [ ] Signed up for Mailtrap (Email Sending product)
- [ ] Domain verified (green checkmark in Mailtrap)
- [ ] Got SMTP credentials (host, port, user, pass)
- [ ] Added 6 environment variables to Vercel
- [ ] Checked all 3 boxes for each variable
- [ ] Redeployed without build cache
- [ ] Tested booking form
- [ ] Email received at elyonolawale@gmail.com

---

## 📖 NEED MORE HELP?

See full guide: `/app/MAILTRAP_SETUP_GUIDE.md`

---

**Total Time: ~45 minutes** (mostly waiting for domain verification)

Your booking form will send emails via Mailtrap! 📧✨
