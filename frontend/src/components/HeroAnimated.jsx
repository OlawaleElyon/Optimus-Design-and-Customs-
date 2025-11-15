import React, { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { Menu, X } from 'lucide-react';

const HeroAnimated = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Start animations after a short delay
    setTimeout(() => setIsVisible(true), 100);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setMobileMenuOpen(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden" id="home">
      {/* Navigation */}
      <nav className={`absolute top-0 left-0 right-0 z-50 px-6 py-6 transition-all duration-1000 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-10'
      }`}>
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <img 
              src="https://customer-assets.emergentagent.com/job_luxury-auto-2/artifacts/arff46fq_ChatGPT%20Image%20Nov%2013%2C%202025%2C%2004_50_22%20PM.png" 
              alt="Optimus Design & Customs"
              className="h-20 md:h-28 w-auto"
            />
          </div>
          
          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => scrollToSection('home')} className="text-gray-300 hover:text-white transition-colors duration-300">Home</button>
            <button onClick={() => scrollToSection('services')} className="text-gray-300 hover:text-white transition-colors duration-300">Services</button>
            <button onClick={() => scrollToSection('projects')} className="text-gray-300 hover:text-white transition-colors duration-300">Projects</button>
            <button onClick={() => scrollToSection('testimonials')} className="text-gray-300 hover:text-white transition-colors duration-300">Reviews</button>
            <button onClick={() => scrollToSection('about')} className="text-gray-300 hover:text-white transition-colors duration-300">About</button>
            <Button 
              onClick={() => scrollToSection('booking')}
              className="bg-sky-600 hover:bg-sky-700 text-white px-6 py-2 rounded-md font-semibold transition-all duration-300 hover:scale-105"
            >
              Book
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-white"
          >
            {mobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden absolute top-full left-0 right-0 bg-gray-900/95 backdrop-blur-lg border-t border-sky-500/20 py-4 animate-fade-in">
            <div className="flex flex-col gap-4 px-6">
              <button onClick={() => scrollToSection('home')} className="text-gray-300 hover:text-white transition-colors duration-300 text-left">Home</button>
              <button onClick={() => scrollToSection('services')} className="text-gray-300 hover:text-white transition-colors duration-300 text-left">Services</button>
              <button onClick={() => scrollToSection('projects')} className="text-gray-300 hover:text-white transition-colors duration-300 text-left">Projects</button>
              <button onClick={() => scrollToSection('about')} className="text-gray-300 hover:text-white transition-colors duration-300 text-left">About</button>
              <Button 
                onClick={() => scrollToSection('booking')}
                className="bg-sky-600 hover:bg-sky-700 text-white px-6 py-2 rounded-md font-semibold"
              >
                Book
              </Button>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Content */}
      <div className="relative min-h-screen flex items-center justify-center">
        {/* Background Image with Parallax Effect */}
        <div className="absolute inset-0">
          {/* Dark Overlay with Gradient */}
          <div className="absolute inset-0 bg-gradient-to-r from-black via-black/70 to-transparent z-10"></div>
          
          {/* Car Image with Slide-in Animation */}
          <img 
            src="https://images.unsplash.com/photo-1696960809870-7094f85696bf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBjYXIlMjB3cmFwfGVufDB8fHx8MTc2MzA1ODAzOXww&ixlib=rb-4.1.0&q=85"
            alt="Luxury Car Wrap"
            className={`w-full h-full object-cover transition-all duration-2000 ease-out ${
              isVisible ? 'scale-100 opacity-100 translate-x-0' : 'scale-110 opacity-0 translate-x-32'
            }`}
          />
        </div>

        {/* Animated Content */}
        <div className="relative z-20 max-w-7xl mx-auto px-6 text-center md:text-left">
          {/* Main Heading with Staggered Animation */}
          <div className="space-y-4 mb-8">
            <div className={`transition-all duration-1000 delay-500 ease-out ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}>
              <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight">
                TRANSFORM YOUR RIDE
              </h1>
            </div>
            
            <div className={`transition-all duration-1000 delay-700 ease-out ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}>
              <h1 className="text-5xl md:text-7xl font-bold leading-tight">
                <span className="bg-gradient-to-r from-sky-400 to-sky-600 bg-clip-text text-transparent animate-gradient">
                  WITH STYLE
                </span>
              </h1>
            </div>
          </div>
          
          {/* Subtitle with Fade-in */}
          <div className={`transition-all duration-1000 delay-900 ease-out ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          }`}>
            <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-2xl">
              Premium wraps, tint, and custom graphics.
            </p>
          </div>

          {/* CTA Buttons with Scale-in Animation */}
          <div className={`flex flex-col sm:flex-row gap-4 justify-center md:justify-start transition-all duration-1000 delay-1100 ease-out ${
            isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-90'
          }`}>
            <Button 
              onClick={() => scrollToSection('booking')}
              className="bg-sky-600 hover:bg-sky-700 text-white px-10 py-7 text-lg rounded-md font-semibold transition-all duration-300 hover:scale-110 hover:shadow-2xl hover:shadow-sky-500/50 animate-pulse-slow"
            >
              Book Appointment
            </Button>
            <Button 
              onClick={() => scrollToSection('projects')}
              className="bg-transparent border-2 border-sky-500 hover:bg-sky-600 text-white px-10 py-7 text-lg rounded-md font-semibold transition-all duration-300 hover:scale-110 backdrop-blur-sm"
            >
              View Projects
            </Button>
          </div>
        </div>

        {/* Animated Scroll Indicator */}
        <div className={`absolute bottom-12 left-1/2 transform -translate-x-1/2 transition-all duration-1000 delay-1300 ${
          isVisible ? 'opacity-100' : 'opacity-0'
        }`}>
          <div className="animate-bounce">
            <div className="w-6 h-10 border-2 border-sky-500 rounded-full flex items-start justify-center p-2">
              <div className="w-1 h-3 bg-sky-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>

        {/* Animated Background Particles */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute w-2 h-2 bg-sky-400 rounded-full opacity-60 animate-float" style={{ top: '20%', left: '15%', animationDelay: '0s' }} />
          <div className="absolute w-3 h-3 bg-sky-500 rounded-full opacity-40 animate-float" style={{ top: '40%', right: '20%', animationDelay: '2s' }} />
          <div className="absolute w-2 h-2 bg-sky-300 rounded-full opacity-50 animate-float" style={{ bottom: '30%', left: '25%', animationDelay: '4s' }} />
          <div className="absolute w-4 h-4 bg-sky-600 rounded-full opacity-30 animate-float" style={{ top: '60%', right: '15%', animationDelay: '1s' }} />
        </div>
      </div>
    </div>
  );
};

export default HeroAnimated;