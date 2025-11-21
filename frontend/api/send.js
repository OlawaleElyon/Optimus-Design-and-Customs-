const { Resend } = require('resend');
const { MongoClient } = require('mongodb');

// MongoDB connection (singleton pattern)
let cachedClient = null;
let cachedDb = null;

async function connectToDatabase() {
  if (cachedClient && cachedDb) {
    return { client: cachedClient, db: cachedDb };
  }

  const mongoUrl = process.env.MONGO_URL || 'mongodb://localhost:27017';
  const dbName = process.env.DB_NAME || 'bookings_db';

  console.log('🔌 Connecting to MongoDB:', mongoUrl);

  const client = new MongoClient(mongoUrl);
  await client.connect();
  const db = client.db(dbName);

  cachedClient = client;
  cachedDb = db;

  return { client, db };
}

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

    // Prepare booking data
    const bookingData = {
      name,
      email,
      phone,
      serviceType,
      preferredDate,
      message: message || 'No message provided',
      createdAt: new Date(),
      status: 'pending',
      emailSent: false,
      emailError: null
    };

    // STEP 1: Save to MongoDB FIRST (so we never lose data)
    console.log('💾 Saving to MongoDB...');
    let bookingId = null;
    let mongoError = null;

    try {
      const { db } = await connectToDatabase();
      const result = await db.collection('bookings').insertOne(bookingData);
      bookingId = result.insertedId;
      console.log('✅ Saved to MongoDB! ID:', bookingId);
    } catch (error) {
      console.error('⚠️ MongoDB save failed:', error.message);
      mongoError = error.message;
      // Continue anyway - we'll still try to send email
    }

    // STEP 2: Try to send email via Resend
    const resendApiKey = process.env.RESEND_API_KEY;
    const senderEmail = process.env.SENDER_EMAIL || 'onboarding@resend.dev';
    const recipientEmail = process.env.RECIPIENT_EMAIL || 'elyonolawale@gmail.com';

    console.log('🔑 Environment check:');
    console.log('   Resend API Key:', resendApiKey ? 'Present' : 'MISSING');
    console.log('   Sender Email:', senderEmail);
    console.log('   Recipient Email:', recipientEmail);

    let emailId = null;
    let emailError = null;

    if (resendApiKey) {
      try {
        console.log('📤 Initializing Resend client...');
        const resend = new Resend(resendApiKey);

        // Generate HTML email
        const htmlBody = generateEmailHtml({
          name,
          email,
          phone,
          serviceType,
          preferredDate,
          message: message || 'No message provided'
        });

        console.log('📨 Sending email via Resend API...');
        
        // Send email via Resend
        const result = await resend.emails.send({
          from: `Optimus Design & Customs <${senderEmail}>`,
          to: [recipientEmail],
          subject: `New Booking Request from ${name}`,
          html: htmlBody,
          reply_to: email,
        });

        // Resend API returns { data: { id }, error }
        if (result.error) {
          console.error('❌ Resend API error:', JSON.stringify(result.error, null, 2));
          emailError = result.error.message || 'Failed to send email';
        } else {
          emailId = result.data?.id;
          console.log('✅ Email sent successfully!');
          console.log('   Email ID:', emailId);

          // Update MongoDB with email success
          if (bookingId) {
            try {
              const { db } = await connectToDatabase();
              await db.collection('bookings').updateOne(
                { _id: bookingId },
                { 
                  $set: { 
                    emailSent: true, 
                    emailId: emailId,
                    emailSentAt: new Date()
                  } 
                }
              );
              console.log('✅ Updated MongoDB with email status');
            } catch (err) {
              console.error('⚠️ Failed to update MongoDB:', err.message);
            }
          }
        }
      } catch (error) {
        console.error('❌ Error sending email:', error);
        emailError = error.message;

        // Update MongoDB with email error
        if (bookingId) {
          try {
            const { db } = await connectToDatabase();
            await db.collection('bookings').updateOne(
              { _id: bookingId },
              { $set: { emailError: error.message } }
            );
          } catch (err) {
            console.error('⚠️ Failed to update MongoDB:', err.message);
          }
        }
      }
    } else {
      console.error('⚠️ RESEND_API_KEY not found - email not sent');
      emailError = 'Resend API key not configured';
    }

    // STEP 3: Return response based on what succeeded
    if (bookingId && emailId) {
      // Perfect - both saved and emailed
      return res.status(200).json({
        success: true,
        message: 'Booking saved and email sent successfully',
        booking_id: bookingId.toString(),
        email_id: emailId
      });
    } else if (bookingId && !emailId) {
      // Saved to DB but email failed
      return res.status(200).json({
        success: true,
        message: 'Booking saved to database (email failed - will retry manually)',
        booking_id: bookingId.toString(),
        warning: `Email not sent: ${emailError}`
      });
    } else if (!bookingId && emailId) {
      // Email sent but DB save failed
      return res.status(200).json({
        success: true,
        message: 'Email sent successfully (database save failed)',
        email_id: emailId,
        warning: `Database error: ${mongoError}`
      });
    } else {
      // Both failed
      return res.status(500).json({
        success: false,
        message: 'Failed to save booking',
        errors: {
          mongodb: mongoError,
          email: emailError
        }
      });
    }

  } catch (error) {
    console.error('❌ Unexpected error:', error);
    return res.status(500).json({
      success: false,
      message: `Error processing booking: ${error.message}`
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
