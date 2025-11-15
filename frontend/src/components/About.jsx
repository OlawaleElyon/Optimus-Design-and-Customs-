import React, { useEffect, useRef, useState } from 'react';
import { Button } from './ui/button';

const About = () => {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.2 }
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

  return (
    <section id="about" ref={sectionRef} className="py-24 px-6 bg-gradient-to-b from-black to-gray-900">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Image Side */}
          <div className={`transition-all duration-1000 ease-out ${
            isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-20'
          }`}>
            <div className="relative group">
              <div className="absolute inset-0 bg-sky-600/20 rounded-2xl transform group-hover:scale-105 transition-transform duration-500"></div>
              <img 
                src="https://images.unsplash.com/photo-1646531839844-034be6a06aad?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxjYXIlMjB3aW5kb3clMjB0aW50fGVufDB8fHx8MTc2MzA1ODA1MHww&ixlib=rb-4.1.0&q=85"
                alt="Car Customization Shop"
                className="relative rounded-2xl shadow-2xl w-full h-[500px] object-cover transform group-hover:scale-[1.02] transition-transform duration-500"
              />
            </div>
          </div>

          {/* Content Side */}
          <div className={`transition-all duration-1000 delay-300 ease-out ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20'
          }`}>
            <p className="text-sky-400 font-semibold text-sm uppercase tracking-wider mb-4 font-sans">Craft</p>
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Who We Are
            </h2>
            <p className="text-gray-300 text-lg leading-relaxed font-serif-accent italic">
              Optimus Design & Customs is a premier car wrap company dedicated to providing top-notch custom designs and products for our valued customers. Our team is passionate about transforming vehicles with our expertise in vehicle wraps, window tints, and decals/graphics. We take pride in delivering exceptional results that exceed expectations.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;