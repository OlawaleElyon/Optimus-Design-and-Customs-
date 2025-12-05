import React, { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';

const Projects = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const sectionRef = useRef(null);

  const projects = [
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/9nvoz2y5_WhatsApp%20Image%202025-12-05%20at%2016.05.36_1620f27e.jpg',
      category: 'Vehicle Wrap',
      description: 'Red commercial truck wrap'
    },
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/t60sptr3_WhatsApp%20Image%202025-12-05%20at%2016.05.37_15fdf985.jpg',
      category: 'Vehicle Wrap',
      description: 'Black contractor truck wrap'
    },
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/sgg5hhho_WhatsApp%20Image%202025-12-05%20at%2016.05.37_7f9531a4.jpg',
      category: 'Vehicle Wrap',
      description: 'Commercial trailer wrap'
    },
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/g72crkgc_WhatsApp%20Image%202025-12-05%20at%2016.06.00_84e76854.jpg',
      category: 'Window Tint',
      description: 'Ford F-150 dark tint'
    },
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/0oph98k7_WhatsApp%20Image%202025-12-05%20at%2016.06.00_37d1db8a.jpg',
      category: 'Window Tint',
      description: 'Honda sedan full tint'
    },
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/zsb9kpf3_WhatsApp%20Image%202025-12-05%20at%2016.06.00_ac9e0bf5.jpg',
      category: 'Window Tint',
      description: 'Nissan blue windshield tint'
    },
    {
      image: 'https://customer-assets.emergentagent.com/job_d82a89b0-3b7b-4e9f-952f-30a60f62b0f3/artifacts/t479uuit_WhatsApp%20Image%202025-12-05%20at%2016.06.43_6206c248.jpg',
      category: 'Custom Decals',
      description: 'Camo wrap design'
    },
    {
      image: 'https://images.unsplash.com/photo-1755079601926-0003a950186b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxjdXN0b20lMjBjYXIlMjBkZWNhbHN8ZW58MHx8fHwxNzYzMDU4MDU2fDA&ixlib=rb-4.1.0&q=85',
      category: 'Custom Decals',
      description: 'Custom logo & branding'
    },
    {
      image: 'https://images.unsplash.com/photo-1755079601887-91c8b991d1c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxjdXN0b20lMjBjYXIlMjBkZWNhbHN8ZW58MHx8fHwxNzYzMDU4MDU2fDA&ixlib=rb-4.1.0&q=85',
      category: 'Custom Decals',
      description: 'Hood & side graphics'
    }
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
          <p className="text-gray-300 text-lg max-w-3xl font-serif-accent italic">
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
                  src={project.image}
                  alt={`${project.category} - ${project.description}`}
                  className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                />
                {/* Category Badge - Always Visible */}
                <div className="absolute top-4 left-4 bg-sky-500/90 backdrop-blur-sm px-4 py-2 rounded-full">
                  <p className="text-white text-sm font-semibold">{project.category}</p>
                </div>
                
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="absolute bottom-0 left-0 right-0 p-6 transform translate-y-full group-hover:translate-y-0 transition-transform duration-500">
                  <h3 className="text-white text-xl font-bold mb-2">{project.category}</h3>
                  <p className="text-gray-300 text-sm font-serif-accent italic">{project.description}</p>
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