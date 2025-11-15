import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { CheckCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Success = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [paymentInfo, setPaymentInfo] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    
    if (!sessionId) {
      setError('No payment session found');
      setLoading(false);
      return;
    }

    // Poll for payment status
    pollPaymentStatus(sessionId);
  }, [searchParams]);

  const pollPaymentStatus = async (sessionId, attempts = 0) => {
    const maxAttempts = 5;
    const pollInterval = 2000; // 2 seconds

    if (attempts >= maxAttempts) {
      setError('Payment verification timed out. Please check your email for confirmation.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get(`${API}/payments/status/${sessionId}`);
      const data = response.data;

      if (data.payment_status === 'paid') {
        setPaymentInfo(data);
        setLoading(false);
        return;
      } else if (data.status === 'expired') {
        setError('Payment session expired. Please try again.');
        setLoading(false);
        return;
      }

      // If payment is still pending, continue polling
      setTimeout(() => pollPaymentStatus(sessionId, attempts + 1), pollInterval);
    } catch (err) {
      console.error('Error checking payment status:', err);
      setError('Error verifying payment. Please contact us if you were charged.');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-sky-500 animate-spin mx-auto mb-4" />
          <p className="text-white text-xl">Verifying your payment...</p>
          <p className="text-gray-400 mt-2">Please wait a moment</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black flex items-center justify-center">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-8 mb-6">
            <h1 className="text-3xl font-bold text-red-400 mb-4">Payment Verification Error</h1>
            <p className="text-gray-300 text-lg">{error}</p>
          </div>
          <Button
            onClick={() => navigate('/booking')}
            className="bg-sky-600 hover:bg-sky-700 text-white px-8 py-4 text-lg"
          >
            Return to Booking
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black flex items-center justify-center py-20 px-6">
      <div className="max-w-2xl mx-auto text-center">
        {/* Success Icon */}
        <div className="mb-8 animate-bounce">
          <CheckCircle className="w-24 h-24 text-green-500 mx-auto" />
        </div>

        {/* Success Message */}
        <h1 className="text-5xl font-bold text-white mb-4">
          Payment Successful!
        </h1>
        <p className="text-xl text-gray-300 mb-8">
          Thank you for your deposit. We'll be in touch shortly to confirm your appointment.
        </p>

        {/* Payment Details */}
        {paymentInfo && (
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-sky-500/20 mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">Payment Details</h2>
            <div className="space-y-4 text-left">
              <div className="flex justify-between items-center border-b border-gray-700 pb-3">
                <span className="text-gray-400">Amount Paid</span>
                <span className="text-white font-semibold">
                  ${(paymentInfo.amount_total / 100).toFixed(2)} {paymentInfo.currency.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between items-center border-b border-gray-700 pb-3">
                <span className="text-gray-400">Payment Status</span>
                <span className="text-green-400 font-semibold">Paid</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Session ID</span>
                <span className="text-gray-300 font-mono text-sm">{paymentInfo.session_id.substring(0, 20)}...</span>
              </div>
            </div>
          </div>
        )}

        {/* Next Steps */}
        <div className="bg-sky-500/10 border border-sky-500/30 rounded-lg p-6 mb-8">
          <h3 className="text-xl font-bold text-white mb-3">What's Next?</h3>
          <ul className="text-gray-300 space-y-2 text-left">
            <li className="flex items-start">
              <span className="text-sky-400 mr-2">•</span>
              You'll receive a confirmation email shortly
            </li>
            <li className="flex items-start">
              <span className="text-sky-400 mr-2">•</span>
              Our team will contact you within 24 hours
            </li>
            <li className="flex items-start">
              <span className="text-sky-400 mr-2">•</span>
              We'll schedule your service appointment
            </li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            onClick={() => navigate('/')}
            className="bg-sky-600 hover:bg-sky-700 text-white px-8 py-4 text-lg"
          >
            Back to Home
          </Button>
          <Button
            onClick={() => navigate('/booking')}
            className="bg-transparent border-2 border-sky-500 hover:bg-sky-600 text-white px-8 py-4 text-lg"
          >
            Book Another Service
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Success;