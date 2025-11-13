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
              <div className="absolute inset-0 bg-purple-600/20 rounded-2xl transform group-hover:scale-105 transition-transform duration-500"></div>
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
            <p className="text-purple-400 font-semibold text-sm uppercase tracking-wider mb-4">Craft</p>
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Who We Are
            </h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Optimus Design & Customs transforms vehicles into art. We blend precision engineering with creative vision to deliver custom wraps that reflect your unique style. Every project is a masterpiece crafted with passion and attention to detail.
            </p>
            <p className="text-gray-400 text-base leading-relaxed mb-8">
              With years of experience and a commitment to excellence, we've become the trusted choice for automotive enthusiasts who demand nothing but the best. From luxury vehicles to everyday rides, we treat each car as our own.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-6 rounded-md font-semibold transition-all duration-300 hover:scale-105">
                Learn More
              </Button>
              <Button className="bg-transparent border-2 border-purple-500 hover:bg-purple-600 text-white px-8 py-6 rounded-md font-semibold transition-all duration-300 hover:scale-105">
                Our Process →
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;