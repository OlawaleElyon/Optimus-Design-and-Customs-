// Local test script for Vercel serverless function
// This simulates how Vercel will call the /api/send function

const sendHandler = require('./frontend/api/send.js');

// Mock request object
const mockReq = {
  method: 'POST',
  body: {
    name: 'Test User',
    email: 'test@example.com',
    phone: '555-0123',
    serviceType: 'vehicle-wrap',
    preferredDate: '2025-12-25',
    message: 'This is a test booking'
  }
};

// Mock response object
const mockRes = {
  statusCode: null,
  headers: {},
  body: null,
  
  setHeader(key, value) {
    this.headers[key] = value;
  },
  
  status(code) {
    this.statusCode = code;
    return this;
  },
  
  json(data) {
    this.body = data;
    console.log('\n📧 RESPONSE:');
    console.log('Status:', this.statusCode);
    console.log('Body:', JSON.stringify(data, null, 2));
    return this;
  },
  
  end() {
    console.log('Response ended');
  }
};

// Test the function
async function testFunction() {
  console.log('🧪 Testing Vercel Serverless Function Locally\n');
  console.log('📤 REQUEST:');
  console.log('Method:', mockReq.method);
  console.log('Body:', JSON.stringify(mockReq.body, null, 2));
  
  console.log('\n🔑 Environment Variables:');
  console.log('RESEND_API_KEY:', process.env.RESEND_API_KEY ? '✅ Set' : '❌ Not set');
  console.log('RESEND_SENDER_EMAIL:', process.env.RESEND_SENDER_EMAIL || '(using default)');
  console.log('RECIPIENT_EMAIL:', process.env.RECIPIENT_EMAIL || '(using default)');
  
  try {
    await sendHandler(mockReq, mockRes);
    
    if (mockRes.statusCode === 200 && mockRes.body?.success) {
      console.log('\n✅ SUCCESS! Function works correctly.');
      console.log('Email ID:', mockRes.body.email_id);
    } else {
      console.log('\n❌ FAILED!');
      console.log('Error:', mockRes.body?.message);
    }
  } catch (error) {
    console.log('\n❌ EXCEPTION!');
    console.error('Error:', error.message);
    console.error('Stack:', error.stack);
  }
}

// Set environment variables for testing
process.env.RESEND_API_KEY = process.env.RESEND_API_KEY || 're_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9';
process.env.RESEND_SENDER_EMAIL = process.env.RESEND_SENDER_EMAIL || 'onboarding@resend.dev';
process.env.RECIPIENT_EMAIL = process.env.RECIPIENT_EMAIL || 'elyonolawale@gmail.com';

testFunction();
