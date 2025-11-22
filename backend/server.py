from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timezone

# Import our services
from email_service import send_booking_confirmation
from payment_service import PaymentService, get_package_amount, get_package_currency, SERVICE_PACKAGES

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Optimus Design & Customs API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== MODELS ====================

class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class AppointmentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    serviceType: str
    preferredDate: str
    message: Optional[str] = ""

class Appointment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    serviceType: str
    preferredDate: str
    message: Optional[str] = ""
    status: str = "pending"
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PaymentRequest(BaseModel):
    package_id: str
    appointment_id: Optional[str] = None
    frontend_origin: str

class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    package_id: str
    amount: float
    currency: str
    payment_status: str = "pending"
    status: str = "initiated"
    appointment_id: Optional[str] = None
    metadata: Optional[Dict] = {}
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "Optimus Design & Customs API v1.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Optimus Design & Customs API"}

# ==================== DEBUGGING ENDPOINTS ====================

@api_router.get("/test-env")
async def test_environment_variables():
    """
    Test endpoint to verify environment variables are loaded correctly.
    Returns masked versions of sensitive data for security.
    """
    try:
        resend_key = os.environ.get('RESEND_API_KEY', '')
        sender_email = os.environ.get('RESEND_SENDER_EMAIL', '')
        recipient_email = os.environ.get('RECIPIENT_EMAIL', '')
        mongo_url = os.environ.get('MONGO_URL', '')
        db_name = os.environ.get('DB_NAME', '')
        
        # Mask sensitive data
        def mask_key(key: str) -> str:
            if not key:
                return "NOT_SET"
            if len(key) <= 8:
                return "*" * len(key)
            return key[:4] + "*" * (len(key) - 8) + key[-4:]
        
        return {
            "status": "success",
            "environment_variables": {
                "RESEND_API_KEY": mask_key(resend_key),
                "RESEND_API_KEY_LENGTH": len(resend_key),
                "RESEND_API_KEY_SET": bool(resend_key),
                "RESEND_SENDER_EMAIL": sender_email,
                "RECIPIENT_EMAIL": recipient_email,
                "MONGO_URL": mask_key(mongo_url),
                "DB_NAME": db_name,
            },
            "message": "All environment variables loaded successfully" if resend_key else "WARNING: RESEND_API_KEY not set!"
        }
    except Exception as e:
        logger.error(f"Error checking environment variables: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

@api_router.post("/test-email")
async def test_email_sending(test_data: Optional[Dict] = None):
    """
    Test endpoint to directly test Resend email sending.
    Sends a test email to verify the integration is working.
    """
    try:
        logger.info("=" * 80)
        logger.info("STARTING EMAIL TEST")
        logger.info("=" * 80)
        
        # Check if API key is set
        resend_key = os.environ.get('RESEND_API_KEY')
        if not resend_key:
            error_msg = "RESEND_API_KEY environment variable is not set"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        logger.info(f"✓ API Key loaded (length: {len(resend_key)})")
        
        # Get email addresses
        sender_email = os.environ.get('RESEND_SENDER_EMAIL', 'onboarding@resend.dev')
        recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
        
        logger.info(f"✓ Sender: {sender_email}")
        logger.info(f"✓ Recipient: {recipient_email}")
        
        # Create test booking data
        test_booking = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+1234567890",
            "serviceType": "Email Test",
            "preferredDate": datetime.now(timezone.utc).isoformat(),
            "message": "This is a test email to verify Resend integration is working correctly."
        }
        
        logger.info("✓ Test booking data created")
        logger.info("📧 Attempting to send test email...")
        
        # Send test email using the email service
        email_result = send_booking_confirmation(test_booking)
        
        logger.info("=" * 80)
        logger.info("EMAIL TEST COMPLETED")
        logger.info("=" * 80)
        
        if email_result["success"]:
            logger.info(f"✅ SUCCESS: Email sent with ID: {email_result.get('email_id')}")
            return {
                "status": "success",
                "message": "Test email sent successfully",
                "email_id": email_result.get('email_id'),
                "details": {
                    "sender": sender_email,
                    "recipient": recipient_email,
                    "api_key_set": True,
                    "api_key_length": len(resend_key)
                }
            }
        else:
            logger.error(f"❌ FAILED: {email_result['message']}")
            raise HTTPException(
                status_code=500, 
                detail=f"Email sending failed: {email_result['message']}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ EXCEPTION in test_email: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Email test failed: {str(e)}")

# Status Check Routes
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks

# Appointment Routes
@api_router.post("/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment_data: AppointmentCreate):
    """
    Create a new appointment with comprehensive logging and error handling.
    Saves to MongoDB and sends email notification.
    """
    try:
        logger.info("=" * 80)
        logger.info("NEW APPOINTMENT REQUEST")
        logger.info("=" * 80)
        logger.info(f"📝 Received appointment data: {appointment_data.model_dump()}")
        
        # Step 1: Create appointment object
        appointment_dict = appointment_data.model_dump()
        appointment_obj = Appointment(**appointment_dict)
        logger.info(f"✓ Appointment object created with ID: {appointment_obj.id}")
        
        # Step 2: Prepare for database insertion
        doc = appointment_obj.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        logger.info("✓ Document prepared for MongoDB")
        
        # Step 3: Save to MongoDB (backup)
        try:
            result = await db.appointments.insert_one(doc)
            if not result.inserted_id:
                raise HTTPException(status_code=500, detail="Failed to create appointment in database")
            logger.info(f"✅ Appointment saved to MongoDB successfully")
        except Exception as db_error:
            logger.error(f"❌ Database error: {str(db_error)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
        
        # Step 4: Send confirmation email
        logger.info("📧 Attempting to send confirmation email...")
        try:
            email_result = send_booking_confirmation(appointment_dict)
            if email_result["success"]:
                logger.info(f"✅ Email sent successfully! Email ID: {email_result.get('email_id')}")
            else:
                logger.warning(f"⚠️  Email failed but appointment saved: {email_result['message']}")
        except Exception as email_error:
            logger.error(f"❌ Email sending exception: {str(email_error)}")
            # Don't fail the request if email fails - appointment is already saved
            logger.warning("⚠️  Continuing despite email failure - appointment is saved in database")
        
        logger.info("=" * 80)
        logger.info(f"✅ APPOINTMENT CREATED SUCCESSFULLY: {appointment_obj.id}")
        logger.info("=" * 80)
        
        return appointment_obj
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR creating appointment: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to create appointment: {str(e)}")

@api_router.get("/appointments", response_model=List[Appointment])
async def get_appointments():
    try:
        appointments = await db.appointments.find({}, {"_id": 0}).sort("createdAt", -1).to_list(1000)
        for appointment in appointments:
            if isinstance(appointment['createdAt'], str):
                appointment['createdAt'] = datetime.fromisoformat(appointment['createdAt'])
        return appointments
    except Exception as e:
        logger.error(f"Error fetching appointments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    try:
        appointment = await db.appointments.find_one({"id": appointment_id}, {"_id": 0})
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        if isinstance(appointment['createdAt'], str):
            appointment['createdAt'] = datetime.fromisoformat(appointment['createdAt'])
        return Appointment(**appointment)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Payment Routes
@api_router.get("/payment-packages")
async def get_payment_packages():
    """Get available service packages with prices"""
    return {"packages": SERVICE_PACKAGES}

@api_router.post("/payments/checkout")
async def create_payment_checkout(payment_request: PaymentRequest, request: Request):
    """Create a Stripe checkout session for a service package"""
    try:
        # Validate package
        if payment_request.package_id not in SERVICE_PACKAGES:
            raise HTTPException(status_code=400, detail="Invalid package ID")
        
        # Get amount from server-side definition (NEVER from frontend)
        amount = get_package_amount(payment_request.package_id)
        currency = get_package_currency(payment_request.package_id)
        
        # Get host URL from request
        host_url = str(request.base_url).rstrip('/')
        
        # Initialize payment service
        payment_service = PaymentService(host_url=host_url)
        
        # Create metadata
        metadata = {
            "package_id": payment_request.package_id,
            "appointment_id": payment_request.appointment_id or "",
            "source": "web_checkout"
        }
        
        # Create checkout session
        session = await payment_service.create_checkout_session(
            amount=amount,
            currency=currency,
            metadata=metadata,
            frontend_origin=payment_request.frontend_origin
        )
        
        # Store transaction in database
        transaction = PaymentTransaction(
            session_id=session.session_id,
            package_id=payment_request.package_id,
            amount=amount,
            currency=currency,
            appointment_id=payment_request.appointment_id,
            metadata=metadata
        )
        
        doc = transaction.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        doc['updatedAt'] = doc['updatedAt'].isoformat()
        
        await db.payment_transactions.insert_one(doc)
        
        logger.info(f"Payment checkout created: {session.session_id}")
        
        return {
            "url": session.url,
            "session_id": session.session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating payment checkout: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/payments/status/{session_id}")
async def get_payment_status(session_id: str, request: Request):
    """Get the status of a payment session"""
    try:
        # Get host URL
        host_url = str(request.base_url).rstrip('/')
        payment_service = PaymentService(host_url=host_url)
        
        # Get status from Stripe
        status_response = await payment_service.get_checkout_status(session_id)
        
        # Check if transaction already processed
        existing_transaction = await db.payment_transactions.find_one(
            {"session_id": session_id}, 
            {"_id": 0}
        )
        
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Only update if status changed and not already processed
        if (status_response.payment_status == "paid" and 
            existing_transaction.get('payment_status') != "paid"):
            
            # Update transaction
            await db.payment_transactions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "payment_status": status_response.payment_status,
                        "status": status_response.status,
                        "updatedAt": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
            logger.info(f"Payment completed: {session_id}")
        
        return {
            "session_id": session_id,
            "status": status_response.status,
            "payment_status": status_response.payment_status,
            "amount_total": status_response.amount_total,
            "currency": status_response.currency,
            "metadata": status_response.metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting payment status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    try:
        body = await request.body()
        signature = request.headers.get("Stripe-Signature")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing Stripe signature")
        
        # Get host URL
        host_url = str(request.base_url).rstrip('/')
        payment_service = PaymentService(host_url=host_url)
        
        # Handle webhook
        webhook_response = await payment_service.handle_webhook(body, signature)
        
        # Update transaction if payment completed
        if webhook_response["payment_status"] == "paid":
            await db.payment_transactions.update_one(
                {"session_id": webhook_response["session_id"]},
                {
                    "$set": {
                        "payment_status": webhook_response["payment_status"],
                        "status": "completed",
                        "updatedAt": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
        
        return {"success": True}
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Include the router in the main app
app.include_router(api_router)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
