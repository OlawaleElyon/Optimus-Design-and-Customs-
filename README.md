# Optimus Design & Customs - Booking System

**Production-ready appointment booking system for Vercel**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-repo)

---

## 🚀 Tech Stack

- **Frontend:** React + TailwindCSS
- **Backend:** Node.js Serverless Functions (Vercel)
- **Database:** Supabase (PostgreSQL)
- **Email:** Resend (with fallback system)
- **Deployment:** Vercel

---

## ✨ Features

✅ **Guaranteed Data Persistence** - Every booking saves to Supabase  
✅ **Email Notifications** - Instant alerts via Resend  
✅ **Email Fallback System** - Never miss a booking  
✅ **Production-Grade Error Handling**  
✅ **Comprehensive Logging**  
✅ **Mobile-Responsive Design**  
✅ **Animated UI Components**  
✅ **Form Validation**  
✅ **CORS Configured**  
✅ **Custom Domain Support**  

---

## 📁 Project Structure

```
/app/
├── api/                          # Vercel Serverless Functions
│   ├── appointment.js            # Main booking API
│   └── package.json              # Node.js dependencies
├── frontend/                     # React Application
│   ├── src/
│   │   ├── components/
│   │   │   └── Booking.jsx       # Booking form component
│   │   ├── pages/
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── .env
├── vercel.json                   # Vercel configuration
├── README.md                     # This file
├── VERCEL_DEPLOYMENT_GUIDE.md    # Deployment instructions
├── SUPABASE_EMAIL_FALLBACK_SETUP.md  # Email fallback setup
└── GITHUB_CLEANUP_GUIDE.md       # Repository cleanup guide
```

---

## 🔧 Environment Variables

### Required (Add in Vercel Dashboard)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
RESEND_API_KEY=your_resend_api_key
RESEND_SENDER_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=elyonolawale@gmail.com
NODE_ENV=production
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-username/optimus-booking
cd optimus-booking
```

### 2. Install Dependencies

```bash
# Frontend
cd frontend
yarn install

# API
cd ../api
yarn install
```

### 3. Set Up Environment Variables

Create `frontend/.env`:
```env
REACT_APP_BACKEND_URL=
```

### 4. Set Up Supabase

Run this SQL in Supabase SQL Editor:

```sql
-- Create appointments table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    service_type TEXT NOT NULL,
    preferred_date TEXT NOT NULL,
    project_details TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create email fallback table
CREATE TABLE email_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    attempts INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5. Local Development

```bash
# Frontend (port 3000)
cd frontend
yarn start

# Test API endpoint with Vercel CLI
vercel dev
```

### 6. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

See [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 📡 API Endpoint

### POST `/api/appointment`

Submit a new appointment request.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "(443) 477-1124",
  "serviceType": "Vehicle Wraps",
  "preferredDate": "2025-12-15",
  "message": "I need a full vehicle wrap"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Your request has been submitted successfully...",
  "appointment_id": "uuid-here",
  "email_sent": true
}
```

---

## 🎨 Services Offered

- **Vehicle Wraps** - Full or partial vehicle wrapping
- **Window Tint** - Professional window tinting
- **Custom Decals** - Custom decal design and application
- **Request a Quote** - Custom projects

---

## 📞 Contact Information

- **Email:** optimusxcustoms@gmail.com
- **Phone:** (443) 477-1124
- **Address:** Cherry Lane, Laurel MD, 20707
- **Instagram:** @optimusdesign

---

## 🔒 Security

- ✅ Environment variables for all secrets
- ✅ CORS properly configured
- ✅ Input validation
- ✅ SQL injection prevention (Supabase parameterized queries)
- ✅ XSS protection
- ✅ No sensitive data in client code

---

## 🧪 Testing

### Test Locally

```bash
# Start frontend
cd frontend && yarn start

# In another terminal, test API
curl -X POST http://localhost:3000/api/appointment \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@test.com",
    "phone": "1234567890",
    "serviceType": "Vehicle Wraps",
    "preferredDate": "2025-12-15",
    "message": "Test"
  }'
```

### Test Production

```bash
curl -X POST https://your-domain.com/api/appointment \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

---

## 📊 Monitoring

### Vercel Dashboard
- Function execution logs
- Error tracking
- Performance metrics

### Supabase Dashboard
- Database queries
- Table row counts
- Failed email notifications

---

## 🐛 Troubleshooting

**Build fails:**
- Check `vercel.json` configuration
- Verify all dependencies in `package.json`

**API not working:**
- Check environment variables in Vercel
- Check Supabase connection
- Review function logs

**Email not sending:**
- Verify RESEND_API_KEY
- Check Supabase `email_notifications` table for fallback

See [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md) for more troubleshooting.

---

## 📚 Documentation

- [Vercel Deployment Guide](./VERCEL_DEPLOYMENT_GUIDE.md)
- [Supabase Email Fallback Setup](./SUPABASE_EMAIL_FALLBACK_SETUP.md)
- [GitHub Cleanup Guide](./GITHUB_CLEANUP_GUIDE.md)

---

## 🤝 Contributing

This is a private project for Optimus Design & Customs.

---

## 📄 License

Proprietary - © 2025 Optimus Design & Customs. All rights reserved.

---

## 🎉 Deployment Status

**Production:** https://optimuscustomz.com  
**Status:** ✅ Live

---

## 💡 Support

For issues or questions:
1. Check [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)
2. Review Vercel function logs
3. Check Supabase dashboard
4. Contact development team

---

**Built with ❤️ for Optimus Design & Customs**
