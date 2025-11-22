# Emergent Deployment Configuration Guide

## Environment Variables Required for Production

After deploying to Emergent, you MUST configure these environment variables in your deployment settings:

### Backend Environment Variables (Required):

```
SUPABASE_URL=https://ogoamklrsfxtapeqngta.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9nb2Fta2xyc2Z4dGFwZXFuZ3RhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4MDQzNTMsImV4cCI6MjA3OTM4MDM1M30.ihBUh0ReyAHVEu5DuRwRvIRITmJDFEcDkTPD_ieVW5s
RESEND_API_KEY=re_jk3kFpBa_K3RKpjpMp3RGKBvMdepmjTYA
RESEND_SENDER_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=elyonolawale@gmail.com
CORS_ORIGINS=https://luxury-auto-book.emergent.host,https://optimuscustomz.com
```

### Frontend Environment Variables (Required):

```
REACT_APP_BACKEND_URL=https://luxury-auto-book.emergent.host
```

## How to Configure in Emergent:

1. Go to your **Deployed App** in Emergent
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable listed above with its value
4. **Save** and **Restart** the deployment

## Important Notes:

- **SUPABASE_URL** and **SUPABASE_SERVICE_ROLE_KEY** are REQUIRED - app will not work without them
- **RESEND_API_KEY** is optional - if not configured, appointments will still save but email notifications will be disabled
- **CORS_ORIGINS** should include your production domain and any custom domains
- **REACT_APP_BACKEND_URL** tells the frontend where to find the backend API

## Testing After Configuration:

1. Visit your deployed URL: `https://luxury-auto-book.emergent.host`
2. Go to the booking form
3. Submit a test appointment
4. Check backend logs to verify:
   - ✅ "Supabase configured"
   - ✅ "Resend email configured"
   - ✅ "Appointment saved to Supabase"
   - ✅ "Email sent successfully"

## Troubleshooting:

**If appointments don't save:**
- Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set correctly
- Verify Supabase table "appointments" exists

**If emails don't send:**
- Check RESEND_API_KEY is set correctly
- Verify the API key is valid in your Resend dashboard
- Check backend logs for "Resend email configured" message

**If frontend can't reach backend:**
- Verify REACT_APP_BACKEND_URL is set correctly
- Check CORS_ORIGINS includes your domain
- Open browser console for error messages
