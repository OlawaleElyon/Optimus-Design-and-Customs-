# Optimus Design & Customs - Booking System

Clean, production-ready appointment booking system powered by **Supabase** and **Resend**.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Supabase** - PostgreSQL database for storing appointments
- **Resend** - Email notifications

### Frontend
- **React** - UI framework
- **TailwindCSS** - Styling
- **Axios** - HTTP client

## Architecture

```
Customer → React Form → FastAPI API → Supabase (Save) → Resend (Email)
                                          ↓
                                    Always Succeeds
                                          ↓
                                     (Email Optional)
```

### Key Design Principles

1. **Guaranteed Data Persistence**: Every appointment ALWAYS saves to Supabase first
2. **Non-Blocking Email**: Email failures don't prevent bookings
3. **Clean Separation**: Only Supabase + Resend, no other dependencies

## Environment Variables

### Backend (`/app/backend/.env`)

```env
# Resend Email Configuration
RESEND_API_KEY=your_resend_api_key
RESEND_SENDER_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=elyonolawale@gmail.com

# Supabase Configuration  
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# CORS Configuration
CORS_ORIGINS=*
```

### Frontend (`/app/frontend/.env`)

```env
REACT_APP_BACKEND_URL=https://luxury-auto-book.emergent.host
```

## Project Structure

```
/app
├── backend/
│   ├── server.py               # FastAPI application
│   ├── appointment_api.py      # Booking API endpoint
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
├── frontend/
│   ├── src/
│   │   └── components/
│   │       └── Booking.jsx     # Booking form component
│   ├── package.json
│   └── .env
└── README.md
```

## API Endpoint

### POST `/api/appointment`

Submit a new appointment request.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "443-477-1124",
  "serviceType": "Vehicle Wraps",
  "preferredDate": "2025-12-01",
  "message": "Optional project details"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Your request has been submitted.",
  "appointment_id": "uuid-here"
}
```

## Supabase Database Schema

### `appointments` table

```sql
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
```

## Deployment

### Emergent Native Deployment

1. Click **Deploy** in Emergent
2. Add environment variables in deployment settings:
   - All variables from backend `.env`
   - `REACT_APP_BACKEND_URL` from frontend `.env`
3. Wait ~10 minutes for deployment
4. Get your live URL

### Custom Domain Setup

1. In Emergent: **Deployments** → **Custom Domain** → Add your domain
2. In your DNS provider: Add A Records
   - `@` → `162.159.142.117`
   - `@` → `172.66.2.113`
   - `www` → `162.159.142.117`
   - `www` → `172.66.2.113`
3. Wait 5-15 minutes for DNS propagation

## Development

### Backend

```bash
cd /app/backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8001
```

### Frontend

```bash
cd /app/frontend
yarn install
yarn start
```

## Contact Information

- **Email**: optimusxcustoms@gmail.com
- **Phone**: (443) 477-1124
- **Address**: Cherry Lane, Laurel MD, 20707
- **Recipient Email**: elyonolawale@gmail.com

## Features

✅ Appointment booking form with validation  
✅ Real-time email notifications via Resend  
✅ Persistent storage in Supabase  
✅ Responsive design with animations  
✅ Clickable contact information  
✅ Service dropdown (Vehicle Wraps, Window Tint, Custom Decals, Request a quote)  
✅ Production-ready error handling  
✅ CORS configured for cross-origin requests  

## License

Proprietary - Optimus Design & Customs
