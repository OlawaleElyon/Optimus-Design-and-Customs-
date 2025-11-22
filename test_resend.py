#!/usr/bin/env python3
"""
Test Resend API key directly
"""

import os
import resend
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# Set API key
resend.api_key = os.environ.get('RESEND_API_KEY')

print(f"Testing Resend API key: {resend.api_key}")

try:
    # Test email send
    params = {
        "from": "Optimus Design & Customs <onboarding@resend.dev>",
        "to": ["elyonolawale@gmail.com"],
        "subject": "Test Email - Appointment System",
        "html": "<h1>Test Email</h1><p>This is a test email from the appointment system.</p>",
    }
    
    response = resend.Emails.send(params)
    print(f"✅ Email sent successfully!")
    print(f"Response: {response}")
    
except Exception as e:
    print(f"❌ Email sending failed: {str(e)}")
    print(f"Error type: {type(e)}")