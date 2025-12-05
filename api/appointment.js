/**
 * Vercel Serverless Function - Appointment Booking
 * Sends email via Resend - Always returns success to user
 */

const { Resend } = require('resend');

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');
  
  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      status: 'error',
      message: 'Method not allowed' 
    });
  }
  
  try {
    const data = req.body || {};
    
    console.log('=== NEW BOOKING REQUEST ===' );
    console.log('Name:', data.name);
    console.log('Email:', data.email);
    console.log('Phone:', data.phone);
    console.log('Service:', data.serviceType);
    console.log('Date:', data.preferredDate);
    console.log('Message:', data.message);
    console.log('========================');
    
    // Try to send email via Resend
    try {
      const apiKey = process.env.RESEND_API_KEY;
      
      if (apiKey) {
        const resend = new Resend(apiKey);
        
        const recipientEmail = process.env.RECIPIENT_EMAIL || 'elyonolawale@gmail.com';
        const senderEmail = process.env.RESEND_SENDER_EMAIL || 'onboarding@resend.dev';
        
        const emailHtml = `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #0891b2, #06b6d4); color: white; padding: 25px; text-align: center;">
              <h1 style="margin: 0; font-size: 24px;">New Appointment Request</h1>
              <p style="margin: 10px 0 0 0; opacity: 0.9;">Optimus Design & Customs</p>
            </div>
            <div style="padding: 25px; background: #ffffff;">
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: bold; color: #0891b2; width: 140px;">Customer Name</td>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">${data.name || 'N/A'}</td>
                </tr>
                <tr>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: bold; color: #0891b2;">Email</td>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;"><a href="mailto:${data.email}" style="color: #0891b2;">${data.email || 'N/A'}</a></td>
                </tr>
                <tr>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: bold; color: #0891b2;">Phone</td>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;"><a href="tel:${data.phone}" style="color: #0891b2;">${data.phone || 'N/A'}</a></td>
                </tr>
                <tr>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: bold; color: #0891b2;">Service Type</td>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">${data.serviceType || 'N/A'}</td>
                </tr>
                <tr>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: bold; color: #0891b2;">Preferred Date</td>
                  <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">${data.preferredDate || 'N/A'}</td>
                </tr>
                <tr>
                  <td style="padding: 12px; font-weight: bold; color: #0891b2; vertical-align: top;">Project Details</td>
                  <td style="padding: 12px;">${data.message || 'No additional details provided'}</td>
                </tr>
              </table>
            </div>
            <div style="padding: 15px; text-align: center; background: #f3f4f6; color: #6b7280; font-size: 12px;">
              Submitted on ${new Date().toLocaleString()}
            </div>
          </div>
        `;
        
        const result = await resend.emails.send({
          from: `Optimus Design & Customs <${senderEmail}>`,
          to: [recipientEmail],
          subject: `New Booking: ${data.serviceType} - ${data.name}`,
          html: emailHtml,
          reply_to: data.email
        });
        
        console.log('Email result:', JSON.stringify(result));
      } else {
        console.log('RESEND_API_KEY not configured');
      }
    } catch (emailError) {
      console.error('Email error:', emailError.message);
    }
    
    // Always return success to user
    return res.status(200).json({
      status: 'success',
      message: "Thank you! Your request has been submitted successfully. We'll contact you shortly!"
    });
    
  } catch (error) {
    console.error('Server error:', error.message);
    // Still return success to provide good user experience
    return res.status(200).json({
      status: 'success', 
      message: "Thank you! Your request has been received. We'll contact you shortly!"
    });
  }
};
