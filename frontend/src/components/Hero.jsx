import React, { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { Menu, X } from 'lucide-react';

const Hero = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setMobileMenuOpen(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Navigation */}
      <nav className="absolute top-0 left-0 right-0 z-50 px-6 py-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <img 
              src="https://customer-assets.emergentagent.com/job_luxury-auto-2/artifacts/arff46fq_ChatGPT%20Image%20Nov%2013%2C%202025%2C%2004_50_22%20PM.png" 
              alt="Optimus Design & Customs"
              className="h-16 md:h-20 w-auto"
            />
          </div>
          
          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => scrollToSection('home')} className="text-gray-300 hover:text-white transition-colors duration-300">Home</button>
            <button onClick={() => scrollToSection('services')} className="text-gray-300 hover:text-white transition-colors duration-300">Services</button>
            <button onClick={() => scrollToSection('projects')} className="text-gray-300 hover:text-white transition-colors duration-300">Projects</button>
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
          <div className="md:hidden absolute top-full left-0 right-0 bg-gray-900/95 backdrop-blur-lg border-t border-sky-500/20 py-4">
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
        {/* Background Image with Overlay */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-transparent z-10"></div>
          <img 
            src="https://images.unsplash.com/photo-1696960809870-7094f85696bf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBjYXIlMjB3cmFwfGVufDB8fHx8MTc2MzA1ODAzOXww&ixlib=rb-4.1.0&q=85"
            alt="Luxury Car Wrap"
            className={`w-full h-full object-cover transition-all duration-1500 ease-out ${
              isVisible ? 'scale-100 opacity-100 translate-x-0' : 'scale-110 opacity-0 translate-x-20'
            }`}
          />
        </div>

        {/* Content */}
        <div className="relative z-20 max-w-7xl mx-auto px-6 text-center md:text-left">
          <div className={`transition-all duration-1000 delay-300 ease-out ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          }`}>
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
              TRANSFORM YOUR RIDE<br />
              <span className="text-sky-400">WITH STYLE</span>
            </h1>
          </div>
          
          <div className={`transition-all duration-1000 delay-500 ease-out ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          }`}>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl">
              Premium wraps, tint, and custom graphics.
            </p>
          </div>

          <div className={`flex flex-col sm:flex-row gap-4 justify-center md:justify-start transition-all duration-1000 delay-700 ease-out ${
            isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-90'
          }`}>
            <Button 
              onClick={() => scrollToSection('booking')}
              className="bg-sky-600 hover:bg-sky-700 text-white px-8 py-6 text-lg rounded-md font-semibold transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-sky-500/50"
            >
              Book Appointment
            </Button>
            <Button 
              onClick={() => scrollToSection('projects')}
              className="bg-transparent border-2 border-sky-500 hover:bg-sky-600 text-white px-8 py-6 text-lg rounded-md font-semibold transition-all duration-300 hover:scale-105"
            >
              View Projects
            </Button>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-sky-500 rounded-full flex items-start justify-center p-2">
            <div className="w-1 h-3 bg-sky-500 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;