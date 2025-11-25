# Backup Notification System - Never Miss an Appointment!

## How It Works Now:

### ✅ Primary System (When Email Works):
1. Customer submits booking form
2. **Appointment saved to Supabase** ✅ (Always happens)
3. **Email sent to elyonolawale@gmail.com** ✅ (Via Resend)
4. You get notified instantly

### 🔄 Backup System (When Email Fails):
1. Customer submits booking form
2. **Appointment saved to Supabase** ✅ (Always happens)
3. System tries to send email **3 times** with delays (2s, 4s, 6s)
4. If all 3 attempts fail:
   - Logs failure to `failed_notifications` table in Supabase
   - Records all appointment details for manual review
   - You can check Supabase dashboard to see missed notifications

---

## What You Need to Do:

### Step 1: Create the Backup Table (One-Time Setup)

1. Go to https://supabase.com/dashboard
2. Select your project (`ogoamklrsfxtapeqngta`)
3. Click "SQL Editor" → "New Query"
4. Copy the SQL from `/app/backend/CREATE_FAILED_NOTIFICATIONS_TABLE.sql`
5. Paste and click "Run"

This creates a `failed_notifications` table to catch any missed emails.

---

### Step 2: Check for New Appointments

You have **two ways** to see new appointments:

#### Option A: Email Notifications (Automatic)
- When Resend is working, you get instant emails
- No action needed on your part

#### Option B: Supabase Dashboard (Manual Backup)
If you haven't received emails in a while, check:

1. Go to https://supabase.com/dashboard
2. Select your project
3. Click "Table Editor"
4. Open the `appointments` table
5. Sort by `created_at` (newest first)
6. You'll see ALL appointments, even if emails failed

---

## How the Retry System Works:

When a customer submits a booking:

```
Attempt 1: Send email → If fails, wait 2 seconds
Attempt 2: Send email → If fails, wait 4 seconds  
Attempt 3: Send email → If fails, log to failed_notifications table
```

This gives Resend multiple chances to succeed, even if there's a temporary issue.

---

## Viewing Failed Notifications:

### In Supabase Dashboard:

1. Go to Table Editor
2. Open `failed_notifications` table
3. You'll see:
   - `appointment_id`: Link to the actual appointment
   - `recipient_email`: Your email (elyonolawale@gmail.com)
   - `appointment_details`: Full customer info (name, email, phone, service, date, message)
   - `error_message`: Why the email failed
   - `created_at`: When it failed
   - `status`: 'failed' or 'resolved'

### Example Query (SQL Editor):

```sql
-- See all unresolved failed notifications
SELECT * FROM failed_notifications 
WHERE status = 'failed' 
ORDER BY created_at DESC;
```

---

## What Data Gets Saved (Even When Email Fails):

Every appointment saves to Supabase with:
- ✅ Customer name
- ✅ Customer email
- ✅ Customer phone
- ✅ Service type requested
- ✅ Preferred date
- ✅ Project details/message
- ✅ Timestamp of submission
- ✅ Unique appointment ID

**Nothing is lost!** You can always contact the customer from the Supabase data.

---

## Best Practices:

### Daily Routine:
1. Check your email for new appointment notifications (primary)
2. If no emails received, check Supabase `appointments` table (backup)
3. Review `failed_notifications` table if you suspect missed emails

### Weekly:
1. Review all appointments in Supabase
2. Mark resolved failed notifications as 'resolved'
3. Verify Resend API key is working

---

## Marking Notifications as Resolved:

Once you've contacted a customer from a failed notification:

```sql
UPDATE failed_notifications 
SET status = 'resolved', resolved_at = NOW() 
WHERE id = 'notification-id-here';
```

---

## Troubleshooting:

**Q: Why would emails fail?**
A: Common reasons:
- Invalid/expired Resend API key
- Resend service temporary outage
- Rate limits exceeded
- Email quota reached

**Q: How do I know if emails are failing?**
A: Check backend logs in Emergent deployment - you'll see:
- "✅ Email sent successfully" (working)
- "❌ All 3 email attempts failed" (not working)

**Q: Can I set up email alerts for failed notifications?**
A: Yes! In Supabase:
1. Go to Database → Webhooks
2. Create webhook on `failed_notifications` INSERT
3. Point it to a service like Zapier or Make.com
4. Configure it to email you when new row added

---

## Summary:

✅ **Appointments ALWAYS save to Supabase** (guaranteed)
✅ **Email tries 3 times before giving up** (automatic retry)
✅ **Failed emails logged to backup table** (manual review)
✅ **You can always check Supabase dashboard** (nothing is lost)

**You will never miss an appointment!** Even if Resend fails completely, all customer data is safely stored in Supabase.
