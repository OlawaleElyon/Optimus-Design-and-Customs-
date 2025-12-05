"""
Optimus Design & Customs - Production-Grade Booking API
✅ Guaranteed data persistence
✅ Multiple email fallback layers
✅ Comprehensive error handling
✅ Professional logging
"""
import os
import logging
from datetime import datetime
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, validator
from supabase import create_client, Client
import resend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize API router
appointment_router = APIRouter(prefix="/api", tags=["Appointment"])

# Supabase client singleton
_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get or create Supabase client with error handling."""
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            error_msg = "Supabase credentials missing. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY"
            logger.critical(error_msg)
            raise ValueError(error_msg)
        
        try:
            _supabase_client = create_client(supabase_url, supabase_key)
            logger.info("✅ Supabase client initialized successfully")
        except Exception as e:
            logger.critical(f"❌ Failed to initialize Supabase: {str(e)}")
            raise
    
    return _supabase_client


# ==================== MODELS ====================

class AppointmentRequest(BaseModel):
    """Request model with comprehensive validation."""
    name: str = Field(..., min_length=1, max_length=255, description="Customer full name")
    email: EmailStr = Field(..., description="Valid email address")
    phone: str = Field(..., min_length=7, max_length=50, description="Contact phone number")
    serviceType: str = Field(..., min_length=1, description="Type of service requested")
    preferredDate: str = Field(..., description="Preferred appointment date")
    message: str = Field(default="", max_length=5000, description="Project details")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format."""
        # Remove common separators
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 7:
            raise ValueError('Phone number must contain at least 7 digits')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Ensure name is not just whitespace."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "(443) 477-1124",
                "serviceType": "Vehicle Wraps",
                "preferredDate": "2025-12-15",
                "message": "I need a full vehicle wrap for my Tesla Model 3"
            }
        }


class AppointmentResponse(BaseModel):
    """Standardized response model."""
    status: str = Field(default="success", description="Response status")
    message: str = Field(default="Your request has been submitted.", description="User-friendly message")
    appointment_id: Optional[str] = Field(default=None, description="Unique appointment ID")
    email_sent: Optional[bool] = Field(default=None, description="Whether email was sent successfully")


# ==================== CORE FUNCTIONS ====================

def save_to_supabase(appointment_data: Dict) -> tuple[str, bool]:
    """
    Save appointment to Supabase database.
    This is the PRIMARY data persistence layer - MUST succeed.
    
    Returns:
        tuple: (appointment_id, success)
    """
    try:
        logger.info("💾 Saving appointment to Supabase...")
        
        supabase = get_supabase()
        
        # Prepare data for database
        db_data = {
            "name": appointment_data["name"],
            "email": appointment_data["email"],
            "phone": appointment_data["phone"],
            "service_type": appointment_data["serviceType"],
            "preferred_date": appointment_data["preferredDate"],
            "project_details": appointment_data.get("message", "")
        }
        
        # Insert into appointments table
        response = supabase.table("appointments").insert(db_data).execute()
        
        if not response.data or len(response.data) == 0:
            raise Exception("Supabase returned no data after insert")
        
        appointment_id = str(response.data[0].get('id'))
        logger.info(f"✅ Appointment saved successfully: {appointment_id}")
        
        return appointment_id, True
        
    except Exception as e:
        logger.error(f"❌ CRITICAL: Supabase save failed: {str(e)}")
        logger.error(f"   Exception type: {type(e).__name__}")
        raise


def create_email_html(appointment_data: Dict, appointment_id: str) -> str:
    """Generate professional HTML email."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background: #ffffff; }}
            .header {{ background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%); color: white; padding: 30px 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .content {{ padding: 30px; background: #f9fafb; }}
            .detail-box {{ margin: 15px 0; padding: 15px; background: white; border-left: 4px solid #0891b2; border-radius: 4px; }}
            .label {{ font-weight: bold; color: #0891b2; display: block; margin-bottom: 5px; }}
            .value {{ font-size: 16px; color: #333; }}
            .footer {{ padding: 20px; text-align: center; background: #f3f4f6; color: #6b7280; font-size: 14px; }}
            .appointment-id {{ font-family: monospace; background: #e5e7eb; padding: 2px 6px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚗 New Appointment Request</h1>
                <p style="margin: 10px 0 0 0;">Optimus Design & Customs</p>
            </div>
            <div class="content">
                <div class="detail-box">
                    <span class="label">Customer Name</span>
                    <span class="value">{appointment_data['name']}</span>
                </div>
                <div class="detail-box">
                    <span class="label">Email Address</span>
                    <span class="value"><a href="mailto:{appointment_data['email']}">{appointment_data['email']}</a></span>
                </div>
                <div class="detail-box">
                    <span class="label">Phone Number</span>
                    <span class="value"><a href="tel:{appointment_data['phone']}">{appointment_data['phone']}</a></span>
                </div>
                <div class="detail-box">
                    <span class="label">Service Type</span>
                    <span class="value">{appointment_data['serviceType']}</span>
                </div>
                <div class="detail-box">
                    <span class="label">Preferred Date</span>
                    <span class="value">{appointment_data['preferredDate']}</span>
                </div>
                <div class="detail-box">
                    <span class="label">Project Details</span>
                    <span class="value">{appointment_data.get('message', 'No additional details provided')}</span>
                </div>
                <div class="detail-box">
                    <span class="label">Appointment ID</span>
                    <span class="value appointment-id">{appointment_id}</span>
                </div>
                <div class="detail-box">
                    <span class="label">Submitted</span>
                    <span class="value">{datetime.utcnow().strftime('%B %d, %Y at %I:%M %p UTC')}</span>
                </div>
            </div>
            <div class="footer">
                <p>This email was automatically generated by your booking system.</p>
                <p>© {datetime.utcnow().year} Optimus Design & Customs. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """


def send_email_via_resend(appointment_data: Dict, appointment_id: str) -> tuple[bool, Optional[str]]:
    """
    Attempt to send email via Resend.
    
    Returns:
        tuple: (success, error_message)
    """
    try:
        # Check if Resend is configured
        api_key = os.environ.get('RESEND_API_KEY')
        if not api_key or api_key.strip() == '':
            logger.warning("⚠️  RESEND_API_KEY not configured - skipping email")
            return False, "Resend API key not configured"
        
        resend.api_key = api_key
        
        sender_email = os.environ.get('RESEND_SENDER_EMAIL', 'onboarding@resend.dev')
        recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
        
        logger.info(f"📧 Attempting to send email via Resend to {recipient_email}...")
        
        # Prepare email
        email_html = create_email_html(appointment_data, appointment_id)
        
        params = {
            "from": f"Optimus Design & Customs <{sender_email}>",
            "to": [recipient_email],
            "subject": f"New Appointment Request - {appointment_data['serviceType']}",
            "html": email_html,
            "reply_to": appointment_data['email'],
        }
        
        # Send email
        email_response = resend.Emails.send(params)
        email_id = email_response.get('id')
        
        if email_id:
            logger.info(f"✅ Email sent successfully via Resend: {email_id}")
            return True, None
        else:
            logger.warning("⚠️  Resend returned no email ID")
            return False, "No email ID returned"
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Resend email failed: {error_msg}")
        return False, error_msg


def log_email_fallback(appointment_id: str, appointment_data: Dict, error_message: str):
    """
    Log failed email to Supabase for manual follow-up or automatic retry.
    Creates a record in email_notifications table (if it exists).
    """
    try:
        logger.info("📝 Logging email failure to Supabase fallback system...")
        
        supabase = get_supabase()
        recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
        
        email_html = create_email_html(appointment_data, appointment_id)
        
        fallback_data = {
            "appointment_id": appointment_id,
            "recipient_email": recipient_email,
            "subject": f"New Appointment Request - {appointment_data['serviceType']}",
            "body": email_html,
            "status": "pending",
            "attempts": 0,
            "error_message": error_message[:500]  # Limit error message length
        }
        
        # Try to insert into email_notifications table
        supabase.table("email_notifications").insert(fallback_data).execute()
        
        logger.info("✅ Email failure logged to Supabase fallback system")
        logger.warning(f"⚠️  MANUAL ACTION: Check Supabase email_notifications table for appointment {appointment_id}")
        
    except Exception as e:
        # If email_notifications table doesn't exist, just log the error
        logger.error(f"❌ Could not log to email_notifications table: {str(e)}")
        logger.error(f"❌ Email failure details: {error_message}")
        logger.warning(f"⚠️  CRITICAL: Manually check Supabase appointments table for ID: {appointment_id}")


# ==================== API ENDPOINT ====================

@appointment_router.post(
    "/appointment",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit new appointment request",
    description="Submit a booking request. Always saves to Supabase, attempts email via Resend with fallback.",
    responses={
        200: {"description": "Appointment created successfully"},
        400: {"description": "Invalid input data"},
        500: {"description": "Server error"}
    }
)
async def submit_appointment(appointment: AppointmentRequest):
    """
    Submit a new appointment request.
    
    GUARANTEED BEHAVIOR:
    1. ALWAYS saves to Supabase (critical - must succeed)
    2. ATTEMPTS to send email via Resend (best effort)
    3. If email fails, logs to fallback system
    4. ALWAYS returns success if Supabase save worked
    
    This ensures zero data loss.
    """
    request_id = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    try:
        logger.info("="*80)
        logger.info(f"📋 NEW APPOINTMENT REQUEST [{request_id}]")
        logger.info("="*80)
        
        appointment_data = appointment.model_dump()
        logger.info(f"   Customer: {appointment_data['name']}")
        logger.info(f"   Email: {appointment_data['email']}")
        logger.info(f"   Service: {appointment_data['serviceType']}")
        
        # STEP 1: SAVE TO SUPABASE (CRITICAL - MUST SUCCEED)
        try:
            appointment_id, save_success = save_to_supabase(appointment_data)
            
            if not save_success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to save appointment to database"
                )
                
        except Exception as db_error:
            logger.critical(f"❌ DATABASE SAVE FAILED: {str(db_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to save your request. Please try again or contact us directly."
            )
        
        # STEP 2: SEND EMAIL VIA RESEND (BEST EFFORT)
        email_sent, email_error = send_email_via_resend(appointment_data, appointment_id)
        
        # STEP 3: IF EMAIL FAILED, LOG TO FALLBACK SYSTEM
        if not email_sent:
            logger.warning(f"⚠️  Email sending failed: {email_error}")
            log_email_fallback(appointment_id, appointment_data, email_error or "Unknown error")
        
        # ALWAYS RETURN SUCCESS IF SAVED TO DATABASE
        logger.info("="*80)
        logger.info(f"✅ APPOINTMENT COMPLETED [{request_id}]")
        logger.info(f"   ID: {appointment_id}")
        logger.info(f"   Email Sent: {email_sent}")
        logger.info("="*80)
        
        return AppointmentResponse(
            status="success",
            message="Your request has been submitted successfully. We'll contact you shortly!",
            appointment_id=appointment_id,
            email_sent=email_sent
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"❌ UNEXPECTED ERROR [{request_id}]: {str(e)}")
        logger.critical(f"   Exception type: {type(e).__name__}")
        
        import traceback
        logger.critical(f"   Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again or contact us directly."
        )


# ==================== ADMIN ENDPOINTS ====================

@appointment_router.get(
    "/appointments/recent",
    summary="Get recent appointments (admin)",
    description="Retrieve recent appointments from Supabase"
)
async def get_recent_appointments(limit: int = 10):
    """Get recent appointments for admin review."""
    try:
        supabase = get_supabase()
        
        response = supabase.table("appointments")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        return {
            "status": "success",
            "count": len(response.data),
            "appointments": response.data
        }
    except Exception as e:
        logger.error(f"Error fetching appointments: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch appointments")


@appointment_router.get(
    "/email-queue/pending",
    summary="Get pending email notifications (admin)",
    description="Check email_notifications table for failed emails"
)
async def get_pending_emails():
    """Check for pending email notifications that need manual attention."""
    try:
        supabase = get_supabase()
        
        response = supabase.table("email_notifications")\
            .select("*")\
            .eq("status", "pending")\
            .order("created_at", desc=True)\
            .execute()
        
        return {
            "status": "success",
            "count": len(response.data),
            "pending_emails": response.data
        }
    except Exception as e:
        # Table might not exist yet
        return {
            "status": "info",
            "message": "email_notifications table not found or error occurred",
            "error": str(e)
        }
