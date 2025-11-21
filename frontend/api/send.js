const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Handle OPTIONS request (CORS preflight)
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    console.log('❌ Method not allowed:', req.method);
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    console.log('📧 Booking email request received');
    console.log('Request body:', JSON.stringify(req.body));
    
    // Get data from request body
    const { name, email, phone, serviceType, preferredDate, message } = req.body;

    // Validate required fields
    if (!name || !email || !phone || !serviceType || !preferredDate) {
      console.log('❌ Missing required fields');
      return res.status(400).json({ 
        success: false, 
        message: 'Missing required fields' 
      });
    }

    console.log('✅ All required fields present');

    // Get Mailtrap credentials from environment variables
    const mailtrapHost = process.env.MAILTRAP_HOST || 'live.smtp.mailtrap.io';
    const mailtrapPort = process.env.MAILTRAP_PORT || 587;
    const mailtrapUser = process.env.MAILTRAP_USER;
    const mailtrapPass = process.env.MAILTRAP_PASS;
    const senderEmail = process.env.SENDER_EMAIL || 'noreply@optimuscustomz.com';
    const recipientEmail = process.env.RECIPIENT_EMAIL || 'elyonolawale@gmail.com';

    console.log('🔑 Environment check:');
    console.log('   Mailtrap Host:', mailtrapHost);
    console.log('   Mailtrap Port:', mailtrapPort);
    console.log('   Mailtrap User:', mailtrapUser ? 'Present' : 'MISSING');
    console.log('   Mailtrap Pass:', mailtrapPass ? 'Present' : 'MISSING');
    console.log('   Sender Email:', senderEmail);
    console.log('   Recipient Email:', recipientEmail);

    if (!mailtrapUser || !mailtrapPass) {
      console.error('❌ Mailtrap credentials not found in environment variables');
      return res.status(500).json({ 
        success: false, 
        message: 'Email service not configured - Mailtrap credentials missing' 
      });
    }

    console.log('📤 Creating Mailtrap transporter...');
    
    // Create Mailtrap transporter
    const transporter = nodemailer.createTransport({
      host: mailtrapHost,
      port: mailtrapPort,
      secure: false, // Use TLS
      auth: {
        user: mailtrapUser,
        pass: mailtrapPass,
      },
    });

    // Generate HTML email
    const htmlBody = generateEmailHtml({
      name,
      email,
      phone,
      serviceType,
      preferredDate,
      message: message || 'No message provided'
    });

    console.log('📨 Sending email via Mailtrap...');
    
    // Send email
    const info = await transporter.sendMail({
      from: `"Optimus Design & Customs" <${senderEmail}>`,
      to: recipientEmail,
      subject: `New Booking Request from ${name}`,
      html: htmlBody,
      replyTo: email,
    });

    console.log('✅ Email sent successfully!');
    console.log('   Message ID:', info.messageId);

    // Return success response
    return res.status(200).json({
      success: true,
      message: 'Booking email sent successfully',
      email_id: info.messageId
    });

  } catch (error) {
    console.error('❌ Error sending email:', error);
    return res.status(500).json({
      success: false,
      message: `Error sending email: ${error.message}`
    });
  }
};

function generateEmailHtml(booking) {
  const escapeHtml = (text) => {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
  };

  const name = escapeHtml(booking.name);
  const email = escapeHtml(booking.email);
  const phone = escapeHtml(booking.phone);
  const serviceType = escapeHtml(booking.serviceType);
  const preferredDate = escapeHtml(booking.preferredDate);
  const message = escapeHtml(booking.message);

  return `
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0; }
          .header h1 { margin: 0; font-size: 28px; }
          .content { background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px; }
          .detail { margin: 15px 0; padding: 15px; background: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
          .label { font-weight: bold; color: #0ea5e9; display: block; margin-bottom: 5px; font-size: 12px; text-transform: uppercase; }
          .value { color: #333; font-size: 16px; }
          .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #0ea5e9; text-align: center; font-size: 12px; color: #666; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>OPTIMUS DESIGN & CUSTOMS</h1>
            <p style="margin: 10px 0 0 0;">New Booking Request</p>
          </div>
          <div class="content">
            <p style="font-size: 16px; color: #555; margin-bottom: 25px;">A new booking request has been received:</p>
            
            <div class="detail">
              <span class="label">Customer Name</span>
              <span class="value">${name}</span>
            </div>
            <div class="detail">
              <span class="label">Email Address</span>
              <span class="value">${email}</span>
            </div>
            <div class="detail">
              <span class="label">Phone Number</span>
              <span class="value">${phone}</span>
            </div>
            <div class="detail">
              <span class="label">Service Type</span>
              <span class="value">${serviceType}</span>
            </div>
            <div class="detail">
              <span class="label">Preferred Date</span>
              <span class="value">${preferredDate}</span>
            </div>
            <div class="detail">
              <span class="label">Message</span>
              <span class="value">${message}</span>
            </div>
          </div>
          <div class="footer">
            <p><strong>Optimus Design & Customs</strong></p>
            <p>Transform Your Ride with Style</p>
            <p>Cherry Lane, Laurel MD, 20707</p>
            <p>Phone: (443) 477-1124</p>
          </div>
        </div>
      </body>
    </html>
  `;
}
