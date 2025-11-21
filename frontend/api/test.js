// Simple test endpoint to verify Vercel API routes work
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');
  
  return res.status(200).json({
    success: true,
    message: 'Vercel API route is working!',
    timestamp: new Date().toISOString(),
    method: req.method
  });
};
