"""
Optimus Design & Customs - Appointment Booking API
Clean implementation with ONLY Resend + Supabase
"""
import os
import logging
from datetime import datetime
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client, Client
import resend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize API router
appointment_router = APIRouter(prefix="/api", tags=["Appointment"])

# Supabase client singleton
_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get or create Supabase client."""
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            logger.error("❌ SUPABASE_URL and SUPABASE_ANON_KEY must be set")
            raise ValueError("Supabase configuration missing")
        
        _supabase_client = create_client(supabase_url, supabase_key)
        logger.info("✅ Supabase client initialized")
    
    return _supabase_client


# ==================== MODELS ====================

class AppointmentRequest(BaseModel):
    """Request model for booking form submission."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=50)
    serviceType: str = Field(..., min_length=1)
    preferredDate: str
    message: str = Field(default="")


class AppointmentResponse(BaseModel):
    """Response model for booking submission."""
    status: str = "success"
    message: str = "Your request has been submitted."
    appointment_id: Optional[str] = None


# ==================== CORE FUNCTIONS ====================

def save_to_supabase(appointment_data: Dict) -> str:
    """
    Save appointment to Supabase.
    This ALWAYS happens first - guaranteed data persistence.
    
    Returns:
        str: Appointment ID
    """
    try:
        supabase = get_supabase()
        
        db_data = {
            "name": appointment_data["name"],
            "email": appointment_data["email"],
            "phone": appointment_data["phone"],
            "service_type": appointment_data["serviceType"],
            "preferred_date": appointment_data["preferredDate"],
            "project_details": appointment_data.get("message", "")
        }
        
        logger.info("💾 Saving to Supabase...")
        response = supabase.table("appointments").insert(db_data).execute()
        
        if response.data and len(response.data) > 0:
            appointment_id = response.data[0].get('id')
            logger.info(f"✅ Saved to Supabase: {appointment_id}")
            return str(appointment_id)
        else:
            raise Exception("No data returned from Supabase")
            
    except Exception as e:
        logger.error(f"❌ Supabase save failed: {str(e)}")
        raise


def send_email_notification(appointment_data: Dict, appointment_id: str) -> bool:
    """
    Send email notification via Resend.
    This is secondary - failure doesn't affect the booking.
    
    Returns:
        bool: True if sent, False if failed
    """
    try:
        api_key = os.environ.get('RESEND_API_KEY')
        
        if not api_key or api_key.strip() == '':
            logger.warning("⚠️  RESEND_API_KEY not configured")
            return False
        
        resend.api_key = api_key
        
        sender_email = os.environ.get('RESEND_SENDER_EMAIL', 'onboarding@resend.dev')
        recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
        
        # Build HTML email
        email_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                        <h1 style="margin: 0;">New Appointment Request</h1>
                        <p style="margin: 10px 0 0 0;">Optimus Design & Customs</p>
                    </div>
                    <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px;">
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Name:</strong><br/>
                            <span style="font-size: 16px;">{appointment_data['name']}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Email:</strong><br/>
                            <span style="font-size: 16px;">{appointment_data['email']}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Phone:</strong><br/>
                            <span style="font-size: 16px;">{appointment_data['phone']}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Service Type:</strong><br/>
                            <span style="font-size: 16px;">{appointment_data['serviceType']}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Preferred Date:</strong><br/>
                            <span style="font-size: 16px;">{appointment_data['preferredDate']}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Project Details:</strong><br/>
                            <span style="font-size: 16px;">{appointment_data.get('message', 'No additional details provided')}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Appointment ID:</strong><br/>
                            <span style="font-size: 14px; color: #666;">{appointment_id}</span>
                        </div>
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px;">
                            <strong style="color: #0891b2;">Submitted:</strong><br/>
                            <span style="font-size: 14px;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</span>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        
        logger.info(f"📧 Sending email to {recipient_email}...")
        
        params = {
            "from": f"Optimus Design & Customs <{sender_email}>",
            "to": [recipient_email],
            "subject": "New Appointment Request – Optimus Design & Customs",
            "html": email_html,
            "reply_to": appointment_data['email'],
        }
        
        email_response = resend.Emails.send(params)
        email_id = email_response.get('id')
        
        logger.info(f"✅ Email sent successfully: {email_id}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Email failed: {str(e)}")
        return False


# ==================== API ENDPOINT ====================

@appointment_router.post(
    "/appointment",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit appointment request",
    description="Submit a new appointment. Always saves to Supabase, attempts email via Resend."
)
async def submit_appointment(appointment: AppointmentRequest):
    """
    Submit a new appointment request.
    
    Process:
    1. ALWAYS save to Supabase first (guaranteed persistence)
    2. THEN try to send email (non-critical)
    3. ALWAYS return success if Supabase save worked
    
    This ensures no bookings are ever lost.
    """
    try:
        logger.info("="*80)
        logger.info("NEW APPOINTMENT REQUEST")
        logger.info("="*80)
        
        appointment_data = appointment.model_dump()
        logger.info(f"📝 Data: {appointment_data}")
        
        # STEP 1: Save to Supabase (MUST succeed)
        try:
            appointment_id = save_to_supabase(appointment_data)
        except Exception as db_error:
            logger.error(f"❌ Critical: Supabase save failed: {str(db_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save appointment. Please try again."
            )
        
        # STEP 2: Send email (best effort, non-critical)
        email_sent = send_email_notification(appointment_data, appointment_id)
        
        if not email_sent:
            logger.warning("⚠️  Email failed BUT appointment saved")
            logger.warning(f"⚠️  Check Supabase for ID: {appointment_id}")
        
        logger.info("="*80)
        logger.info(f"✅ SUCCESS: {appointment_id}")
        logger.info("="*80)
        
        # ALWAYS return success if saved to Supabase
        return AppointmentResponse(
            status="success",
            message="Your request has been submitted.",
            appointment_id=appointment_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred. Please try again."
        )
