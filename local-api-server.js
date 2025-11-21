// Local development server to test the /api/send endpoint
// This mimics how Vercel handles serverless functions

const http = require('http');
const sendHandler = require('./frontend/api/send.js');

// Set environment variables
process.env.RESEND_API_KEY = 're_iBSMDRfP_DHb6h4azEy8bz1PUo5Bw5hG9';
process.env.RESEND_SENDER_EMAIL = 'onboarding@resend.dev';
process.env.RECIPIENT_EMAIL = 'elyonolawale@gmail.com';

const PORT = 3001;

const server = http.createServer(async (req, res) => {
  console.log(`\n📥 ${req.method} ${req.url}`);
  
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // Only handle /api/send
  if (req.url === '/api/send' || req.url === '/api/send/') {
    // Parse request body
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    
    req.on('end', async () => {
      try {
        // Parse JSON body
        req.body = JSON.parse(body);
        console.log('📦 Request body:', req.body);
        
        // Call the serverless function handler
        await sendHandler(req, res);
        
      } catch (error) {
        console.error('❌ Error:', error);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          success: false,
          message: error.message
        }));
      }
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(PORT, () => {
  console.log(`🚀 Local API server running on http://localhost:${PORT}`);
  console.log(`📧 Test endpoint: http://localhost:${PORT}/api/send`);
  console.log('');
  console.log('🔑 Environment variables loaded:');
  console.log('   RESEND_API_KEY:', process.env.RESEND_API_KEY ? '✅' : '❌');
  console.log('   RECIPIENT_EMAIL:', process.env.RECIPIENT_EMAIL);
  console.log('');
  console.log('💡 Update your frontend to use http://localhost:3001 for local testing');
  console.log('   or configure a proxy in package.json');
});
