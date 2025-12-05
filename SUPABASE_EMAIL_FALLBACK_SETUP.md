# Supabase Email Fallback System Setup

## Overview
This system ensures that even if Resend fails, you ALWAYS get notified of new bookings via Supabase.

## Architecture

```
Customer submits form
    ↓
Backend tries Resend (primary)
    ↓
If Resend fails:
    ↓
Save to Supabase → Trigger → Supabase Edge Function → Send email via Supabase SMTP
```

---

## Option 1: Database Trigger + Webhooks (Recommended)

### Step 1: Create Email Notification Table

Run this SQL in Supabase SQL Editor:

```sql
-- Table to store failed email notifications
CREATE TABLE IF NOT EXISTS email_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL REFERENCES appointments(id),
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sent_at TIMESTAMP WITH TIME ZONE
);

-- Index for quick lookups
CREATE INDEX idx_email_notifications_status ON email_notifications(status);
CREATE INDEX idx_email_notifications_created_at ON email_notifications(created_at DESC);
```

### Step 2: Create Database Function to Send Emails

```sql
-- Function to trigger email sending
CREATE OR REPLACE FUNCTION notify_new_appointment()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert email notification record
    INSERT INTO email_notifications (
        appointment_id,
        recipient_email,
        subject,
        body
    ) VALUES (
        NEW.id,
        'elyonolawale@gmail.com',
        'New Appointment Request - Optimus Design & Customs',
        format('
            New Appointment Received:
            
            Name: %s
            Email: %s
            Phone: %s
            Service: %s
            Date: %s
            Details: %s
            
            Appointment ID: %s
            Created: %s
        ', NEW.name, NEW.email, NEW.phone, NEW.service_type, 
           NEW.preferred_date, NEW.project_details, NEW.id, NEW.created_at)
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Step 3: Create Trigger

```sql
-- Trigger on appointments table
CREATE TRIGGER on_appointment_created
    AFTER INSERT ON appointments
    FOR EACH ROW
    EXECUTE FUNCTION notify_new_appointment();
```

### Step 4: Setup Webhook or Cron Job

Go to Supabase Dashboard → Database → Webhooks:

1. Create new webhook
2. Table: `email_notifications`
3. Events: `INSERT`
4. URL: Your backend endpoint `/api/process-email-queue`
5. HTTP Method: POST

---

## Option 2: Supabase Edge Function (Advanced)

### Create Edge Function

In your Supabase project:

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize
supabase init

# Create function
supabase functions new send-appointment-email
```

### Edge Function Code (`supabase/functions/send-appointment-email/index.ts`):

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY')

serve(async (req) => {
  try {
    const { record } = await req.json()
    
    // Send email via Resend
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'Optimus Design & Customs <onboarding@resend.dev>',
        to: ['elyonolawale@gmail.com'],
        subject: 'New Appointment Request - Optimus Design & Customs',
        html: `
          <h2>New Appointment</h2>
          <p><strong>Name:</strong> ${record.name}</p>
          <p><strong>Email:</strong> ${record.email}</p>
          <p><strong>Phone:</strong> ${record.phone}</p>
          <p><strong>Service:</strong> ${record.service_type}</p>
          <p><strong>Date:</strong> ${record.preferred_date}</p>
          <p><strong>Details:</strong> ${record.project_details}</p>
          <p><strong>ID:</strong> ${record.id}</p>
        `
      })
    })
    
    return new Response(
      JSON.stringify({ success: true }),
      { headers: { "Content-Type": "application/json" } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    )
  }
})
```

### Deploy Edge Function:

```bash
supabase functions deploy send-appointment-email --no-verify-jwt
```

### Create Database Trigger to Call Edge Function:

```sql
CREATE OR REPLACE FUNCTION call_edge_function_on_insert()
RETURNS TRIGGER AS $$
DECLARE
    request_id bigint;
BEGIN
    SELECT net.http_post(
        url:='https://YOUR_PROJECT.supabase.co/functions/v1/send-appointment-email',
        headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb,
        body:=jsonb_build_object('record', row_to_json(NEW))
    ) INTO request_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER appointment_email_trigger
    AFTER INSERT ON appointments
    FOR EACH ROW
    EXECUTE FUNCTION call_edge_function_on_insert();
```

---

## Option 3: Backend Polling (Simple)

Add a cron job in your backend to check for unsent emails:

```python
# In backend/email_queue_processor.py
import asyncio
from datetime import datetime, timedelta

async def process_email_queue():
    """Check email_notifications table and send pending emails"""
    supabase = get_supabase()
    
    # Get pending notifications
    result = supabase.table("email_notifications")\
        .select("*")\
        .eq("status", "pending")\
        .lt("attempts", 3)\
        .execute()
    
    for notification in result.data:
        try:
            # Try to send email via Resend
            resend.api_key = os.environ.get('RESEND_API_KEY')
            
            email_response = resend.Emails.send({
                "from": "Optimus Design & Customs <onboarding@resend.dev>",
                "to": [notification['recipient_email']],
                "subject": notification['subject'],
                "text": notification['body']
            })
            
            # Update status
            supabase.table("email_notifications")\
                .update({
                    "status": "sent",
                    "sent_at": datetime.utcnow().isoformat()
                })\
                .eq("id", notification['id'])\
                .execute()
                
        except Exception as e:
            # Increment attempt count
            supabase.table("email_notifications")\
                .update({
                    "attempts": notification['attempts'] + 1,
                    "last_attempt": datetime.utcnow().isoformat()
                })\
                .eq("id", notification['id'])\
                .execute()
```

Run this with cron:
```bash
# Add to crontab (every 5 minutes)
*/5 * * * * cd /app/backend && python email_queue_processor.py
```

---

## Recommended Approach

**Use Option 1 (Database Trigger + Webhook)** because:
- ✅ Simplest to implement
- ✅ No additional infrastructure
- ✅ Real-time notifications
- ✅ Automatic retries
- ✅ Works with existing backend

---

## Testing the Fallback

1. Temporarily disable Resend API key in backend
2. Submit a booking
3. Check Supabase `email_notifications` table
4. Verify record is created
5. Check if webhook/edge function was triggered
6. Verify email received

---

## Monitoring

Check Supabase dashboard regularly:
- `email_notifications` table for pending emails
- Webhook logs for failures
- Edge function logs for errors

Set up alerts if `attempts >= 3` to manually review failed emails.
