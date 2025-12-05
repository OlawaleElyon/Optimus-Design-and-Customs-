import React, { useEffect, useRef, useState } from 'react';
import { Instagram } from 'lucide-react';

const Footer = () => {
  const [isVisible, setIsVisible] = useState(false);
  const footerRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.1 }
    );

    if (footerRef.current) {
      observer.observe(footerRef.current);
    }

    return () => {
      if (footerRef.current) {
        observer.unobserve(footerRef.current);
      }
    };
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer ref={footerRef} className="bg-black border-t border-sky-500/20">
      <div className={`max-w-7xl mx-auto px-6 py-16 transition-all duration-1000 ease-out ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
      }`}>
        <div className="grid md:grid-cols-4 gap-12 mb-12">
          {/* Logo & Description */}
          <div className="md:col-span-2">
            <img 
              src="https://customer-assets.emergentagent.com/job_luxury-auto-2/artifacts/arff46fq_ChatGPT%20Image%20Nov%2013%2C%202025%2C%2004_50_22%20PM.png" 
              alt="Optimus Design & Customs"
              className="h-20 md:h-24 w-auto mb-4"
            />
            <p className="text-gray-400 mb-6 max-w-md font-serif-accent italic text-lg">
              Transforming vehicles into art. Premium wraps, tints, and custom designs that reflect your unique style.
            </p>
            <div className="flex gap-4">
              <a 
                href="https://instagram.com/optimus.customs" 
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gray-800 hover:bg-sky-600 p-3 rounded-lg transition-all duration-300 hover:scale-110"
              >
                <Instagram className="w-5 h-5 text-white" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-bold text-lg mb-4">Quick Links</h4>
            <ul className="space-y-3">
              <li>
                <button onClick={() => { window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="text-gray-400 hover:text-sky-400 transition-colors duration-300">
                  Home
                </button>
              </li>
              <li>
                <button onClick={() => scrollToSection('about')} className="text-gray-400 hover:text-sky-400 transition-colors duration-300">
                  About Us
                </button>
              </li>
              <li>
                <button onClick={() => scrollToSection('services')} className="text-gray-400 hover:text-sky-400 transition-colors duration-300">
                  Services
                </button>
              </li>
              <li>
                <button onClick={() => scrollToSection('projects')} className="text-gray-400 hover:text-sky-400 transition-colors duration-300">
                  Projects
                </button>
              </li>
              <li>
                <button onClick={() => scrollToSection('booking')} className="text-gray-400 hover:text-sky-400 transition-colors duration-300">
                  Book Now
                </button>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-bold text-lg mb-4">Contact</h4>
            <div className="space-y-3 text-gray-400">
              <p>
                <a href="mailto:optimusxcustoms@gmail.com" className="hover:text-sky-400 transition-colors duration-300">
                  optimusxcustoms@gmail.com
                </a>
              </p>
              <p>
                <a href="tel:+14434771124" className="hover:text-sky-400 transition-colors duration-300">
                  (443) 477-1124
                </a>
              </p>
              <p>
                <a href="https://www.google.com/maps/search/?api=1&query=Cherry+Lane+Laurel+MD+20707" target="_blank" rel="noopener noreferrer" className="hover:text-sky-400 transition-colors duration-300">
                  Cherry Lane Laurel MD, 20707
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-500 text-sm">
              © 2025 Optimus Design & Customs. All rights reserved.
            </p>
            <div className="flex gap-6">
              <a href="#" className="text-gray-500 hover:text-sky-400 text-sm transition-colors duration-300">
                Privacy Policy
              </a>
              <a href="#" className="text-gray-500 hover:text-sky-400 text-sm transition-colors duration-300">
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;