// Detailed Resend API test
const { Resend } = require('./frontend/api/node_modules/resend');

async function testResendAPI() {
  console.log('🧪 Testing Resend API\n');
  
  const apiKey = 're_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9';
  const senderEmail = 'onboarding@resend.dev';
  const recipientEmail = 'elyonolawale@gmail.com';
  
  console.log('📋 Configuration:');
  console.log('API Key:', apiKey.substring(0, 10) + '...');
  console.log('From:', senderEmail);
  console.log('To:', recipientEmail);
  console.log('');
  
  const resend = new Resend(apiKey);
  
  try {
    console.log('📤 Sending test email...\n');
    
    const result = await resend.emails.send({
      from: `Optimus Design & Customs <${senderEmail}>`,
      to: [recipientEmail],
      subject: 'Test Booking Request',
      html: `
        <h1>Test Email</h1>
        <p>This is a test email from the booking form.</p>
        <p><strong>Name:</strong> Test User</p>
        <p><strong>Email:</strong> test@example.com</p>
        <p><strong>Phone:</strong> 555-0123</p>
        <p><strong>Service:</strong> Vehicle Wrap</p>
        <p><strong>Date:</strong> 2025-12-25</p>
      `,
      reply_to: 'test@example.com',
    });
    
    console.log('📧 Result:', JSON.stringify(result, null, 2));
    
    if (result.error) {
      console.log('\n❌ ERROR from Resend API:');
      console.log('Error:', result.error);
      console.log('Message:', result.error.message);
      console.log('');
      
      // Check if it's a domain verification issue
      if (result.error.message && result.error.message.toLowerCase().includes('domain')) {
        console.log('⚠️  This appears to be a DOMAIN VERIFICATION issue!');
        console.log('');
        console.log('The sender email "onboarding@resend.dev" can only send to:');
        console.log('1. The verified email address on your Resend account');
        console.log('2. OR you need to verify your own domain (optimuscustomz.com)');
        console.log('');
        console.log('SOLUTION:');
        console.log('- Go to Resend Dashboard: https://resend.com/domains');
        console.log('- Add and verify your domain: optimuscustomz.com');
        console.log('- Then use: noreply@optimuscustomz.com as sender');
      }
    } else if (result.data) {
      console.log('\n✅ SUCCESS!');
      console.log('Email ID:', result.data.id);
      console.log('Email sent successfully!');
    }
    
  } catch (error) {
    console.log('\n❌ EXCEPTION:');
    console.log('Error:', error.message);
    console.log('');
    
    if (error.message.includes('API key')) {
      console.log('⚠️  The API key appears to be invalid or expired.');
      console.log('Please check your Resend dashboard for the correct API key.');
    } else if (error.message.includes('401')) {
      console.log('⚠️  Authentication failed. The API key is invalid.');
    } else if (error.message.includes('403')) {
      console.log('⚠️  Forbidden. Check domain verification and email permissions.');
    } else {
      console.log('Stack:', error.stack);
    }
  }
}

testResendAPI();
