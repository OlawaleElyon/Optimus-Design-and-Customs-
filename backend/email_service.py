import resend
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

# Initialize Resend with API key
resend.api_key = os.environ.get('RESEND_API_KEY')

def send_booking_confirmation(booking_data: dict) -> dict:
    """
    Send booking confirmation email using Resend API.
    
    Args:
        booking_data: Dictionary containing booking details
        
    Returns:
        Dictionary with email send result
    """
    try:
        sender_email = os.environ.get('RESEND_SENDER_EMAIL', 'onboarding@resend.dev')
        recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
        
        # Format the email body
        html_body = generate_email_html(booking_data)
        
        # Prepare email parameters
        params = {
            "from": f"Optimus Design & Customs <{sender_email}>",
            "to": [recipient_email],
            "subject": f"New Booking Request from {booking_data['name']}",
            "html": html_body,
            "reply_to": booking_data['email'],
        }
        
        # Send email via Resend
        email_response = resend.Emails.send(params)
        
        logger.info(f"Email sent successfully. ID: {email_response.get('id')}")
        return {
            "success": True,
            "email_id": email_response.get('id'),
            "message": "Booking confirmation email sent"
        }
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return {
            "success": False,
            "message": f"Email sending failed: {str(e)}"
        }

def generate_email_html(booking_data: dict) -> str:
    """
    Generate HTML email template with booking details.
    
    Args:
        booking_data: Dictionary containing booking details
        
    Returns:
        HTML string for email body
    """
    import html
    
    # Escape user content to prevent injection
    name = html.escape(booking_data.get('name', 'N/A'))
    email = html.escape(booking_data.get('email', 'N/A'))
    phone = html.escape(booking_data.get('phone', 'N/A'))
    service_type = html.escape(booking_data.get('serviceType', 'N/A'))
    preferred_date = html.escape(booking_data.get('preferredDate', 'N/A'))
    message = html.escape(booking_data.get('message', 'No message provided'))
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
                .detail {{ margin: 15px 0; padding: 15px; background: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                .label {{ font-weight: bold; color: #9333ea; display: block; margin-bottom: 5px; font-size: 12px; text-transform: uppercase; }}
                .value {{ color: #333; font-size: 16px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #9333ea; text-align: center; font-size: 12px; color: #666; }}
                .logo {{ font-size: 24px; font-weight: bold; letter-spacing: 1px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">OPTIMUS DESIGN & CUSTOMS</div>
                    <h1>New Booking Request</h1>
                </div>
                <div class="content">
                    <p style="font-size: 16px; color: #555; margin-bottom: 25px;">A new booking request has been received. Please review the details below:</p>
                    
                    <div class="detail">
                        <span class="label">Customer Name</span>
                        <span class="value">{name}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Email Address</span>
                        <span class="value">{email}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Phone Number</span>
                        <span class="value">{phone}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Service Type</span>
                        <span class="value">{service_type}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Preferred Date</span>
                        <span class="value">{preferred_date}</span>
                    </div>
                    <div class="detail">
                        <span class="label">Message</span>
                        <span class="value">{message}</span>
                    </div>
                </div>
                <div class="footer">
                    <p><strong>Optimus Design & Customs</strong></p>
                    <p>Transform Your Ride with Style</p>
                    <p>This is an automated booking notification. Please respond directly to the customer's email address.</p>
                </div>
            </div>
        </body>
    </html>
    """
    return html_template
