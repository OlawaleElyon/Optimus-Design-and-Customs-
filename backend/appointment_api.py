"""
Brand new clean appointment API endpoint.
Handles booking form submissions with Supabase storage and Resend email.
"""
import os
import logging
from datetime import datetime
from typing import Dict
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client, Client
import resend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize API router
appointment_router = APIRouter(prefix="/api", tags=["Appointment"])

# Initialize Resend - API key will be set when needed

# Supabase client singleton
_supabase_client: Client = None

def get_supabase() -> Client:
    """Get or create Supabase client."""
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        
        _supabase_client = create_client(supabase_url, supabase_key)
        logger.info("✓ Supabase client initialized")
    
    return _supabase_client


# ==================== MODELS ====================

class AppointmentRequest(BaseModel):
    """Request model for booking form submission."""
    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    email: EmailStr = Field(..., description="Customer email")
    phone: str = Field(..., min_length=1, max_length=50, description="Customer phone")
    serviceType: str = Field(..., description="Service type selected")
    preferredDate: str = Field(..., description="Preferred appointment date")
    message: str = Field(default="", description="Additional project details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "serviceType": "Vehicle Wraps",
                "preferredDate": "2025-01-15",
                "message": "I need a full vehicle wrap for my Tesla Model 3"
            }
        }


class AppointmentResponse(BaseModel):
    """Response model for successful submission."""
    success: bool
    message: str = "Appointment request received successfully"
    appointment_id: str = None


# ==================== HELPER FUNCTIONS ====================

def send_appointment_email(appointment_data: Dict) -> bool:
    """
    Send appointment notification email using Resend.
    
    Args:
        appointment_data: Dictionary containing appointment details
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Set API key here to ensure environment variables are loaded
        resend.api_key = os.environ.get('RESEND_API_KEY')
        
        sender_email = os.environ.get('RESEND_SENDER_EMAIL', 'onboarding@resend.dev')
        recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
        
        # Format email body
        email_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
                    .detail {{ margin: 15px 0; padding: 15px; background: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    .label {{ font-weight: bold; color: #0891b2; display: block; margin-bottom: 5px; }}
                    .value {{ color: #333; font-size: 16px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>New Appointment Request</h1>
                        <p>Optimus Design & Customs</p>
                    </div>
                    <div class="content">
                        <div class="detail">
                            <span class="label">Name:</span>
                            <span class="value">{appointment_data['name']}</span>
                        </div>
                        <div class="detail">
                            <span class="label">Email:</span>
                            <span class="value">{appointment_data['email']}</span>
                        </div>
                        <div class="detail">
                            <span class="label">Phone:</span>
                            <span class="value">{appointment_data['phone']}</span>
                        </div>
                        <div class="detail">
                            <span class="label">Service Type:</span>
                            <span class="value">{appointment_data['serviceType']}</span>
                        </div>
                        <div class="detail">
                            <span class="label">Preferred Date:</span>
                            <span class="value">{appointment_data['preferredDate']}</span>
                        </div>
                        <div class="detail">
                            <span class="label">Project Details:</span>
                            <span class="value">{appointment_data.get('message', 'No additional details provided')}</span>
                        </div>
                        <div class="detail">
                            <span class="label">Sent on:</span>
                            <span class="value">{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</span>
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
            "subject": f"New Appointment Request – Optimus Design & Customs",
            "html": email_body,
            "reply_to": appointment_data['email'],
        }
        
        email_response = resend.Emails.send(params)
        
        logger.info(f"✅ Email sent successfully. ID: {email_response.get('id')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Email sending failed: {str(e)}")
        return False


def save_to_supabase(appointment_data: Dict) -> Dict:
    """
    Save appointment data to Supabase.
    
    Args:
        appointment_data: Dictionary containing appointment details
        
    Returns:
        Dict: Supabase response with inserted record
    """
    try:
        supabase = get_supabase()
        
        # Prepare data for insertion (match table schema)
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
            logger.info(f"✅ Saved to Supabase with ID: {response.data[0].get('id')}")
            return response.data[0]
        else:
            raise Exception("No data returned from Supabase")
        
    except Exception as e:
        logger.error(f"❌ Supabase save failed: {str(e)}")
        raise


# ==================== API ENDPOINT ====================

@appointment_router.post(
    "/appointment",
    response_model=AppointmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit appointment request",
    description="Submit a new appointment request. Saves to Supabase and sends email notification."
)
async def submit_appointment(appointment: AppointmentRequest):
    """
    Submit a new appointment request.
    
    Process:
    1. Validate all input fields
    2. Save to Supabase database
    3. Send email notification via Resend
    4. Return success response
    """
    try:
        logger.info("=" * 80)
        logger.info("NEW APPOINTMENT REQUEST")
        logger.info("=" * 80)
        logger.info(f"📝 Received data: {appointment.model_dump()}")
        
        # Convert to dict
        appointment_data = appointment.model_dump()
        
        # Step 1: Save to Supabase (primary storage)
        try:
            db_record = save_to_supabase(appointment_data)
            appointment_id = db_record.get('id')
        except Exception as db_error:
            logger.error(f"❌ Database error: {str(db_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save appointment: {str(db_error)}"
            )
        
        # Step 2: Send email notification (non-blocking failure)
        email_sent = send_appointment_email(appointment_data)
        if not email_sent:
            logger.warning("⚠️  Email notification failed, but appointment was saved")
        
        logger.info("=" * 80)
        logger.info(f"✅ APPOINTMENT CREATED SUCCESSFULLY: {appointment_id}")
        logger.info("=" * 80)
        
        return AppointmentResponse(
            success=True,
            message="Your appointment request has been received. We'll contact you shortly!",
            appointment_id=str(appointment_id)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process appointment request. Please try again."
        )
