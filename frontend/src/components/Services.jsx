import React, { useEffect, useRef, useState } from 'react';
import { Button } from './ui/button';
import { Palette, Shield, Sparkles } from 'lucide-react';

const Services = () => {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.1 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => {
      if (sectionRef.current) {
        observer.unobserve(sectionRef.current);
      }
    };
  }, []);

  const services = [
    {
      icon: <Palette className="w-12 h-12" />,
      title: 'Vehicle Wraps',
      description: 'Full color change and custom design options for every style.',
      image: 'https://images.unsplash.com/photo-1632432604371-cf8353f02be0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBjYXIlMjB3cmFwfGVufDB8fHx8MTc2MzA1ODAzOXww&ixlib=rb-4.1.0&q=85',
      delay: 0
    },
    {
      icon: <Shield className="w-12 h-12" />,
      title: 'Window Tint',
      description: 'Professional tinting that enhances privacy and comfort.',
      image: 'https://images.pexels.com/photos/30815197/pexels-photo-30815197.jpeg',
      delay: 200
    },
    {
      icon: <Sparkles className="w-12 h-12" />,
      title: 'Custom Decals',
      description: 'Unique graphics that make your ride stand out from the crowd.',
      image: 'https://images.unsplash.com/photo-1755079601887-91c8b991d1c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxjdXN0b20lMjBjYXIlMjBkZWNhbHN8ZW58MHx8fHwxNzYzMDU4MDU2fDA&ixlib=rb-4.1.0&q=85',
      delay: 400
    }
  ];

  return (
    <section id="services" ref={sectionRef} className="py-24 px-6 bg-gradient-to-b from-gray-900 to-black">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className={`text-center mb-16 transition-all duration-1000 ease-out ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Services
          </h2>
          <p className="text-gray-300 text-lg max-w-3xl mx-auto">
            We offer precision services that elevate your vehicle's aesthetic and performance.
          </p>
        </div>

        {/* Service Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {services.map((service, index) => (
            <div
              key={index}
              className={`group transition-all duration-1000 ease-out ${
                isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20'
              }`}
              style={{ transitionDelay: `${service.delay}ms` }}
            >
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl overflow-hidden border border-gray-700/50 hover:border-purple-500/50 transition-all duration-500 hover:transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-purple-500/20">
                {/* Image */}
                <div className="relative h-64 overflow-hidden">
                  <img 
                    src={service.image}
                    alt={service.title}
                    className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-gray-900 to-transparent opacity-60"></div>
                </div>

                {/* Content */}
                <div className="p-8">
                  <div className="text-purple-400 mb-4 transform group-hover:scale-110 transition-transform duration-300">
                    {service.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4">{service.title}</h3>
                  <p className="text-gray-400">{service.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA Button */}
        <div className={`flex justify-center transition-all duration-1000 delay-600 ease-out ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <Button className="bg-transparent border-2 border-purple-500 hover:bg-purple-600 text-white px-8 py-6 rounded-md font-semibold transition-all duration-300 hover:scale-105">
            Contact Us →
          </Button>
        </div>
      </div>
    </section>
  );
};

export default Services;