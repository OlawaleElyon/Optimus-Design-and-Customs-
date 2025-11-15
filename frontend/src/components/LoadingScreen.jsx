import React, { useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';

const LoadingScreen = ({ onLoadingComplete }) => {
  const [progress, setProgress] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Simulate loading progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            setIsLoaded(true);
            setTimeout(onLoadingComplete, 500);
          }, 300);
          return 100;
        }
        return prev + 10;
      });
    }, 150);

    return () => clearInterval(interval);
  }, [onLoadingComplete]);

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-black transition-opacity duration-500 ${
        isLoaded ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
    >
      <div className="text-center">
        {/* Logo Animation */}
        <div className="mb-12 animate-pulse">
          <img
            src="https://customer-assets.emergentagent.com/job_luxury-auto-2/artifacts/arff46fq_ChatGPT%20Image%20Nov%2013%2C%202025%2C%2004_50_22%20PM.png"
            alt="Optimus Design & Customs"
            className="h-32 w-auto mx-auto"
          />
        </div>

        {/* Loading Spinner */}
        <div className="flex items-center justify-center mb-6">
          <Loader2 className="w-12 h-12 text-purple-400 animate-spin" />
        </div>

        {/* Progress Bar */}
        <div className="w-64 h-2 bg-gray-800 rounded-full overflow-hidden mx-auto mb-4">
          <div
            className="h-full bg-gradient-to-r from-purple-600 to-purple-400 transition-all duration-300 ease-out rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Loading Text */}
        <p className="text-gray-400 text-sm">
          {progress < 30
            ? 'Initializing...'
            : progress < 60
            ? 'Loading assets...'
            : progress < 90
            ? 'Preparing experience...'
            : 'Ready!'}
        </p>
      </div>

      {/* Background Animation */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute w-96 h-96 bg-purple-600/20 rounded-full blur-3xl animate-pulse" style={{ top: '10%', left: '10%' }} />
        <div className="absolute w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse" style={{ bottom: '10%', right: '10%', animationDelay: '1s' }} />
      </div>
    </div>
  );
};

export default LoadingScreen;