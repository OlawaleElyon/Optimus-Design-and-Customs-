# 🔑 ENVIRONMENT VARIABLES - COMPLETE GUIDE

## 📋 WHAT YOU NEED TO ADD TO VERCEL

---

## ✅ SUMMARY: 4 VARIABLES NEEDED

Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

```
1. RESEND_API_KEY = re_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db
2. RECIPIENT_EMAIL = elyonolawale@gmail.com
3. MONGO_URL = [your MongoDB Atlas connection string]
4. DB_NAME = bookings_db
```

---

## 1️⃣ RESEND_API_KEY

**What is it?** Your Resend email service API key

**Value:**
```
re_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db
```

**Where to add:**
```
Key:   RESEND_API_KEY
Value: re_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db
```
✅ Check: Production, Preview, Development

---

## 2️⃣ RECIPIENT_EMAIL

**What is it?** The email address that receives booking notifications

**Value:**
```
elyonolawale@gmail.com
```

**Where to add:**
```
Key:   RECIPIENT_EMAIL
Value: elyonolawale@gmail.com
```
✅ Check: Production, Preview, Development

---

## 3️⃣ MONGO_URL

**What is it?** MongoDB database connection string

**Value:** You need to get this from MongoDB Atlas

### How to Get It:

**Step 1:** Sign up for MongoDB Atlas (FREE)
- Go to: https://www.mongodb.com/cloud/atlas/register
- Sign up (no credit card needed)

**Step 2:** Create FREE cluster
- Click "Build a Database"
- Choose "M0 FREE"
- Wait 1-3 minutes

**Step 3:** Create database user
- Username: `optimususer` (or any name)
- Password: Click "Autogenerate" or create your own
- **SAVE THIS PASSWORD!**

**Step 4:** Allow network access
- Click "Network Access"
- Add IP Address: `0.0.0.0/0`
- Description: "Allow all"

**Step 5:** Get connection string
1. Click your cluster
2. Click "Connect" button
3. Click "Drivers"
4. Select "Node.js"
5. Copy the connection string
6. Replace `<password>` with your actual password

**Your connection string will look like:**
```
mongodb+srv://optimususer:YourPassword123@cluster0.abc12.mongodb.net/?retryWrites=true&w=majority
```

**Example (with fake values):**
```
mongodb+srv://myuser:SecurePass456@cluster0.xyz45.mongodb.net/?retryWrites=true&w=majority
```

**Where to add:**
```
Key:   MONGO_URL
Value: mongodb+srv://optimususer:YourPassword123@cluster0.abc12.mongodb.net/?retryWrites=true&w=majority
```
✅ Check: Production, Preview, Development

**See full guide:** `/app/MONGODB_ATLAS_GUIDE.md`

---

## 4️⃣ DB_NAME

**What is it?** The name of the database inside MongoDB

**Value:**
```
bookings_db
```

**Where to add:**
```
Key:   DB_NAME
Value: bookings_db
```
✅ Check: Production, Preview, Development

**Note:** This is NOT "test_database" - that was the old backend database. The new booking system uses `bookings_db`.

---

## 🎯 FINAL VERCEL SETUP:

Your Vercel environment variables should look exactly like this:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENVIRONMENT VARIABLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ RESEND_API_KEY
   Value: re_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db
   [✓] Production  [✓] Preview  [✓] Development

✅ RECIPIENT_EMAIL
   Value: elyonolawale@gmail.com
   [✓] Production  [✓] Preview  [✓] Development

✅ MONGO_URL
   Value: mongodb+srv://user:pass@cluster0.abc.mongodb.net/?retryWrites=true&w=majority
   [✓] Production  [✓] Preview  [✓] Development

✅ DB_NAME
   Value: bookings_db
   [✓] Production  [✓] Preview  [✓] Development

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📊 WHAT EACH VARIABLE DOES:

| Variable | Purpose | Example |
|----------|---------|---------|
| `RESEND_API_KEY` | Send emails via Resend | `re_7nbWqu...` |
| `RECIPIENT_EMAIL` | Where bookings are sent | `elyonolawale@gmail.com` |
| `MONGO_URL` | Database connection | `mongodb+srv://...` |
| `DB_NAME` | Database name | `bookings_db` |

---

## ⚠️ IMPORTANT NOTES:

### 1. Database Name is `bookings_db`

**NOT `test_database`** - that's the old backend database.

The booking form uses a NEW database: `bookings_db`

### 2. Connection String Must Include Password

Your MONGO_URL must have the actual password, not `<password>`:

❌ Wrong:
```
mongodb+srv://user:<password>@cluster.net/
```

✅ Correct:
```
mongodb+srv://user:ActualPassword123@cluster.net/
```

### 3. Must Check All 3 Boxes

For each variable, you MUST check:
- ✅ Production
- ✅ Preview
- ✅ Development

If you only check Production, it won't work on preview deployments!

### 4. Must Redeploy After Adding

After adding/changing environment variables:
1. Go to Deployments tab
2. Click ••• menu
3. Click "Redeploy"
4. **UNCHECK** "Use existing Build Cache"
5. Wait 2-3 minutes

Environment variables only take effect AFTER redeployment!

---

## 🧪 HOW TO TEST:

### Test on Emergent (Local):
Already configured! Just test the booking form:
- https://luxury-auto-book.preview.emergentagent.com/

### Test on Vercel:
1. Add all 4 variables
2. Redeploy
3. Visit: https://www.optimuscustomz.com/
4. Submit booking form
5. Check:
   - ✅ Email at elyonolawale@gmail.com
   - ✅ Booking in MongoDB Atlas

---

## 🔍 WHERE TO FIND THINGS:

### Resend API Key:
- Already provided: `re_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db`
- Or get from: https://resend.com/api-keys

### MongoDB Atlas Connection String:
- See guide: `/app/MONGODB_ATLAS_GUIDE.md`
- Or follow steps above

### Recipient Email:
- Already set: `elyonolawale@gmail.com`
- This is where you'll receive booking notifications

### Database Name:
- Already set: `bookings_db`
- Don't change this!

---

## 🆘 TROUBLESHOOTING:

### "RESEND_API_KEY not found"
- Make sure variable name is exactly `RESEND_API_KEY` (all caps)
- Check Production box is checked
- Redeploy without build cache

### "Failed to connect to MongoDB"
- Check MONGO_URL is correct
- Make sure password is replaced (not `<password>`)
- Check 0.0.0.0/0 is in IP whitelist
- Wait 5 minutes after creating cluster

### "Email not sent but booking saved"
- Email failed but booking is in MongoDB (good!)
- Check RESEND_API_KEY is correct
- Check Resend dashboard for errors

### "Both failed"
- Check all 4 variables are added
- Check all have 3 boxes checked
- Check MONGO_URL format is correct
- Redeploy without build cache

---

## ✅ CHECKLIST:

Before redeploying, verify:

- [ ] `RESEND_API_KEY` added with correct value
- [ ] `RECIPIENT_EMAIL` = elyonolawale@gmail.com
- [ ] `MONGO_URL` = your MongoDB Atlas connection string (with password!)
- [ ] `DB_NAME` = bookings_db (not test_database!)
- [ ] All 4 variables have Production ✓ Preview ✓ Development ✓
- [ ] Ready to redeploy!

---

## 🎯 QUICK START:

**If you just want to test email first (skip MongoDB):**

Add only these 2:
```
RESEND_API_KEY = re_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db
RECIPIENT_EMAIL = elyonolawale@gmail.com
```

Redeploy and test. If email doesn't work, bookings will still be saved (you'll get a warning message).

**For full production setup (recommended):**

Add all 4 variables including MongoDB Atlas connection.

---

**That's everything you need to know about environment variables!** 🔑
