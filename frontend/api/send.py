from http.server import BaseHTTPRequestHandler
import json
import os
import resend
from datetime import datetime

# Initialize Resend
resend.api_key = os.environ.get('RESEND_API_KEY', '')

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            booking_data = json.loads(post_data.decode('utf-8'))
            
            # Get configuration from environment
            sender_email = os.environ.get('RESEND_SENDER_EMAIL', 'onboarding@resend.dev')
            recipient_email = os.environ.get('RECIPIENT_EMAIL', 'elyonolawale@gmail.com')
            
            # Generate HTML email
            html_body = self.generate_email_html(booking_data)
            
            # Send email via Resend
            params = {
                "from": f"Optimus Design & Customs <{sender_email}>",
                "to": [recipient_email],
                "subject": f"New Booking Request from {booking_data['name']}",
                "html": html_body,
                "reply_to": booking_data['email'],
            }
            
            email_response = resend.Emails.send(params)
            
            # Return success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "message": "Booking email sent successfully",
                "email_id": email_response.get('id')
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "success": False,
                "message": f"Error sending email: {str(e)}"
            }
            
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def generate_email_html(self, booking_data):
        """Generate HTML email template"""
        import html
        
        # Escape user content
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
                    .header {{ background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .header h1 {{ margin: 0; font-size: 28px; }}
                    .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }}
                    .detail {{ margin: 15px 0; padding: 15px; background: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    .label {{ font-weight: bold; color: #0ea5e9; display: block; margin-bottom: 5px; font-size: 12px; text-transform: uppercase; }}
                    .value {{ color: #333; font-size: 16px; }}
                    .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #0ea5e9; text-align: center; font-size: 12px; color: #666; }}
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
                        <p style="font-size: 16px; color: #555; margin-bottom: 25px;">A new booking request has been received:</p>
                        
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
                    </div>
                </div>
            </body>
        </html>
        """
        return html_template
