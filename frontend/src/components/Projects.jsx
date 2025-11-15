import React, { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';

const Projects = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const sectionRef = useRef(null);

  const projects = [
    'https://images.unsplash.com/photo-1638731006124-1c9a33edba30?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBjYXIlMjB3cmFwfGVufDB8fHx8MTc2MzA1ODAzOXww&ixlib=rb-4.1.0&q=85',
    'https://images.unsplash.com/photo-1555534650-6bb24b6fc0e7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBjYXIlMjB3cmFwfGVufDB8fHx8MTc2MzA1ODAzOXww&ixlib=rb-4.1.0&q=85',
    'https://images.pexels.com/photos/13869047/pexels-photo-13869047.jpeg',
    'https://images.pexels.com/photos/18792905/pexels-photo-18792905.jpeg',
    'https://images.unsplash.com/photo-1758445048963-c8682c897428?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHw0fHxjYXIlMjBjdXN0b21pemF0aW9uJTIwc2hvcHxlbnwwfHx8fDE3NjMwNTgwNDV8MA&ixlib=rb-4.1.0&q=85',
    'https://images.unsplash.com/photo-1646531839801-7d0010d7513a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxjYXIlMjB3aW5kb3clMjB0aW50fGVufDB8fHx8MTc2MzA1ODA1MHww&ixlib=rb-4.1.0&q=85',
    'https://images.unsplash.com/photo-1755079602229-f46eceb2683e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxjdXN0b20lMjBjYXIlMjBkZWNhbHN8ZW58MHx8fHwxNzYzMDU4MDU2fDA&ixlib=rb-4.1.0&q=85',
    'https://images.unsplash.com/photo-1755079601926-0003a950186b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxjdXN0b20lMjBjYXIlMjBkZWNhbHN8ZW58MHx8fHwxNzYzMDU4MDU2fDA&ixlib=rb-4.1.0&q=85',
    'https://images.pexels.com/photos/33475330/pexels-photo-33475330.jpeg'
  ];

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

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev + 3 >= projects.length ? 0 : prev + 3));
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev - 3 < 0 ? Math.max(projects.length - 3, 0) : prev - 3));
  };

  const visibleProjects = projects.slice(currentIndex, currentIndex + 3);

  return (
    <section id="projects" ref={sectionRef} className="py-24 px-6 bg-gradient-to-b from-black to-gray-900">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className={`mb-16 transition-all duration-1000 ease-out ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Our Projects
          </h2>
          <p className="text-gray-300 text-lg max-w-3xl">
            A showcase of transformations that push the boundaries of automotive design.
          </p>
        </div>

        {/* Project Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {visibleProjects.map((project, index) => (
            <div
              key={currentIndex + index}
              className={`group relative overflow-hidden rounded-2xl transition-all duration-1000 ease-out ${
                isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20'
              }`}
              style={{ transitionDelay: `${index * 150}ms` }}
            >
              <div className="relative h-96 overflow-hidden">
                <img 
                  src={project}
                  alt={`Project ${currentIndex + index + 1}`}
                  className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="absolute bottom-0 left-0 right-0 p-6 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500">
                  <h3 className="text-white text-xl font-bold mb-2">Custom Wrap Project</h3>
                  <p className="text-gray-300 text-sm">Premium finish with attention to detail</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Navigation */}
        <div className={`flex items-center justify-between transition-all duration-1000 delay-500 ease-out ${
          isVisible ? 'opacity-100' : 'opacity-0'
        }`}>
          <div className="flex gap-2">
            {Array.from({ length: Math.ceil(projects.length / 3) }).map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentIndex(index * 3)}
                className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  Math.floor(currentIndex / 3) === index 
                    ? 'bg-sky-600 w-8' 
                    : 'bg-gray-600 hover:bg-gray-500'
                }`}
              />
            ))}
          </div>

          <div className="flex gap-3">
            <Button
              onClick={prevSlide}
              className="bg-gray-800 hover:bg-sky-600 text-white p-3 rounded-lg transition-all duration-300"
            >
              <ChevronLeft className="w-6 h-6" />
            </Button>
            <Button
              onClick={nextSlide}
              className="bg-gray-800 hover:bg-sky-600 text-white p-3 rounded-lg transition-all duration-300"
            >
              <ChevronRight className="w-6 h-6" />
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Projects;