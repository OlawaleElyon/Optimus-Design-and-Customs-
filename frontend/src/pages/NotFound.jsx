import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Home, ArrowLeft } from 'lucide-react';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black flex items-center justify-center px-6">
      <div className="max-w-2xl mx-auto text-center">
        {/* 404 Text */}
        <h1 className="text-9xl font-bold text-sky-500 mb-4">
          404
        </h1>
        
        {/* Error Message */}
        <h2 className="text-4xl font-bold text-white mb-4">
          Page Not Found
        </h2>
        <p className="text-xl text-gray-300 mb-12">
          Sorry, the page you're looking for doesn't exist or has been moved.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            onClick={() => navigate('/')}
            className="bg-sky-600 hover:bg-sky-700 text-white px-8 py-4 text-lg inline-flex items-center gap-2"
          >
            <Home className="w-5 h-5" />
            Back to Home
          </Button>
          <Button
            onClick={() => navigate(-1)}
            className="bg-transparent border-2 border-sky-500 hover:bg-sky-600 text-white px-8 py-4 text-lg inline-flex items-center gap-2"
          >
            <ArrowLeft className="w-5 h-5" />
            Go Back
          </Button>
        </div>

        {/* Decorative Elements */}
        <div className="mt-16 grid grid-cols-3 gap-8 max-w-lg mx-auto">
          <div className="bg-sky-500/10 p-6 rounded-lg backdrop-blur-sm border border-sky-500/20">
            <p className="text-gray-400 text-sm">Quick Links</p>
            <button onClick={() => navigate('/')} className="text-sky-400 hover:text-sky-300 text-sm mt-2">Home</button>
          </div>
          <div className="bg-sky-500/10 p-6 rounded-lg backdrop-blur-sm border border-sky-500/20">
            <p className="text-gray-400 text-sm">Services</p>
            <button onClick={() => navigate('/#services')} className="text-sky-400 hover:text-sky-300 text-sm mt-2">View All</button>
          </div>
          <div className="bg-sky-500/10 p-6 rounded-lg backdrop-blur-sm border border-sky-500/20">
            <p className="text-gray-400 text-sm">Contact</p>
            <button onClick={() => navigate('/#booking')} className="text-sky-400 hover:text-sky-300 text-sm mt-2">Get in Touch</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;