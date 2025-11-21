#!/usr/bin/env node
// Local server to handle /api/send for Emergent preview environment
const http = require('http');
const sendHandler = require('./frontend/api/send.js');

// Load environment variables from .env file
require('dotenv').config({ path: './frontend/.env' });

// Set environment variables
process.env.RESEND_API_KEY = process.env.RESEND_API_KEY || 're_7nbWquCk_LCt6wDx9ZMi6LQxZrXGmj3db';
process.env.RECIPIENT_EMAIL = process.env.RECIPIENT_EMAIL || 'elyonolawale@gmail.com';

const PORT = 3001;

console.log('🚀 Starting Local Email API Server...\n');
console.log('📧 Configuration:');
console.log('   RESEND_API_KEY:', process.env.RESEND_API_KEY ? '✅ Set' : '❌ Missing');
console.log('   RECIPIENT_EMAIL:', process.env.RECIPIENT_EMAIL);
console.log('');

const server = http.createServer(async (req, res) => {
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  console.log(`\n📥 ${req.method} ${req.url}`);
  
  // Only handle /api/send
  if (req.url === '/api/send' || req.url === '/api/send/') {
    if (req.method !== 'POST') {
      res.writeHead(405, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: false, message: 'Method not allowed' }));
      return;
    }
    
    // Parse request body
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    
    req.on('end', async () => {
      try {
        // Parse JSON body
        req.body = JSON.parse(body);
        
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
  console.log(`✅ Local API server running on http://localhost:${PORT}`);
  console.log(`📧 Endpoint: http://localhost:${PORT}/api/send`);
  console.log('');
  console.log('💡 To test the booking form:');
  console.log('   1. Frontend must proxy /api/send to http://localhost:3001');
  console.log('   2. Or update frontend to call http://localhost:3001/api/send');
  console.log('');
  console.log('🔥 Press Ctrl+C to stop');
});
