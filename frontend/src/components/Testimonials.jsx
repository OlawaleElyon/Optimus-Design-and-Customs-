import React, { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Star } from 'lucide-react';
import { Button } from './ui/button';

const Testimonials = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const sectionRef = useRef(null);

  const reviews = [
    {
      name: "nehemiah lattie",
      rating: 5,
      date: "2 months ago",
      text: "Absolutely blown away by the quality and professionalism of Optimums. Not only was the craftsmanship top tier, the job was completed on time. They helped me choose the perfect wrap and tints for my vehicle. My finish wrap and tint look flawless and smooth- like a factory finish. All for a fair price if may add. 5 STAR would recommend."
    },
    {
      name: "Beeka B",
      rating: 5,
      date: "Recently",
      text: "I couldn't be happier with the wrap on my car! The attention to detail was flawless smooth lines, no bubbles, and the finish looks factory-perfect. My car literally turned heads the moment I drove it out. Professional, reliable, and clearly passionate about the craft. If you're looking to transform your vehicle with quality work that lasts, this is the place to go. Highly recommend!"
    },
    {
      name: "Darryl Bagley",
      rating: 5,
      date: "Recently",
      text: "Ivan did a wrap for my 2008 Escalade ESV and tinted the windows. He is polite professional, cares about his customers and takes pride in his work unlike many business owners today. I would give him 10 stars not just 5. I will be working with him in the future and if you are reading this you won't be disappointed."
    },
    {
      name: "Oscar Martinez",
      rating: 5,
      date: "2 months ago",
      text: "Good quality work! If you're looking for a good tint or wrap, this place is the one! Good pricing, good customer service. I highly recommend in the DMV area!"
    },
    {
      name: "DMV Medical Trans",
      rating: 5,
      date: "2 months ago",
      text: "Reached out to get custom decals, came out exactly how I wanted it. Quick turnaround and very reasonable with the price."
    },
    {
      name: "Marvin Santos",
      rating: 5,
      date: "2 months ago",
      text: "Optimus customs did the decals on my work truck and it came out perfect. The attention to detail is what really sets Optimus customs apart from anyone else. Highly recommend."
    },
    {
      name: "Lester",
      rating: 5,
      date: "2 months ago",
      text: "Great guy, he's very helpful and professional with his wrapping and tints. The waiting room is also nice."
    },
    {
      name: "palung g",
      rating: 5,
      date: "a week ago",
      text: "Reasonable Prices with amazing quality and a lounge room to wait in."
    },
    {
      name: "Anderson Mayorga",
      rating: 5,
      date: "2 months ago",
      text: "Does great work, very reliable and gets it exactly how you want it."
    },
    {
      name: "Donovan Braithwaite",
      rating: 5,
      date: "2 months ago",
      text: "This was a wonderful experience and Ivan does a great job"
    },
    {
      name: "Marbin Argueta",
      rating: 5,
      date: "4 days ago",
      text: "Ivan worked on many of our Company Trucks, he did an excellent Job on all of them, he communicated well with us on his schedule and Got the Job done Right, great person and great work!!"
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

  const nextReview = () => {
    setCurrentIndex((prev) => (prev + 3 >= reviews.length ? 0 : prev + 3));
  };

  const prevReview = () => {
    setCurrentIndex((prev) => (prev - 3 < 0 ? Math.max(reviews.length - 3, 0) : prev - 3));
  };

  const visibleReviews = reviews.slice(currentIndex, currentIndex + 3);

  const renderStars = (rating) => {
    return Array(rating).fill(0).map((_, i) => (
      <span key={i} className="text-yellow-400">⭐</span>
    ));
  };

  return (
    <section id="testimonials" ref={sectionRef} className="py-24 px-6 bg-gradient-to-b from-gray-900 to-black">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className={`text-center mb-16 transition-all duration-1000 ease-out ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
            Testimonials
          </h2>
          <p className="text-gray-300 text-lg max-w-3xl mx-auto font-serif-accent italic">
            Real reviews from our valued customers who trusted us with their vehicles.
          </p>
          
          {/* Google Reviews Link */}
          <a 
            href="https://maps.app.goo.gl/XuAro5qBHefyuJsx9" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 mt-6 text-sky-400 hover:text-sky-300 transition-colors duration-300"
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            View all reviews on Google
          </a>
        </div>

        {/* Reviews Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {visibleReviews.map((review, index) => (
            <div
              key={currentIndex + index}
              className={`bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50 hover:border-sky-500/50 transition-all duration-1000 ease-out hover:transform hover:scale-[1.02] ${
                isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20'
              }`}
              style={{ transitionDelay: `${index * 150}ms` }}
            >
              {/* Stars */}
              <div className="flex items-center gap-1 mb-4">
                {renderStars(review.rating)}
              </div>

              {/* Review Text */}
              <p className="text-gray-300 mb-6 leading-relaxed font-serif-accent italic">
                "{review.text}"
              </p>

              {/* Author Info */}
              <div className="border-t border-gray-700 pt-4">
                <p className="text-white font-semibold">{review.name}</p>
                <p className="text-gray-400 text-sm">{review.date}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Navigation */}
        <div className={`flex items-center justify-between transition-all duration-1000 delay-600 ease-out ${
          isVisible ? 'opacity-100' : 'opacity-0'
        }`}>
          <div className="flex gap-2">
            {Array.from({ length: Math.ceil(reviews.length / 3) }).map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentIndex(index * 3)}
                className={`w-3 h-3 rounded-full transition-all duration-300 ${
                  Math.floor(currentIndex / 3) === index 
                    ? 'bg-sky-500 w-8' 
                    : 'bg-gray-600 hover:bg-gray-500'
                }`}
              />
            ))}
          </div>

          <div className="flex gap-3">
            <Button
              onClick={prevReview}
              className="bg-gray-800 hover:bg-sky-600 text-white p-3 rounded-lg transition-all duration-300"
            >
              <ChevronLeft className="w-6 h-6" />
            </Button>
            <Button
              onClick={nextReview}
              className="bg-gray-800 hover:bg-sky-600 text-white p-3 rounded-lg transition-all duration-300"
            >
              <ChevronRight className="w-6 h-6" />
            </Button>
          </div>
        </div>

        {/* Google Rating Summary */}
        <div className={`mt-16 text-center transition-all duration-1000 delay-800 ease-out ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <div className="inline-flex items-center gap-3 bg-sky-500/10 backdrop-blur-sm px-8 py-4 rounded-full border border-sky-500/30">
            <div className="flex items-center gap-1">
              {renderStars(5)}
            </div>
            <span className="text-white font-bold text-xl">5.0</span>
            <span className="text-gray-400">•</span>
            <span className="text-gray-300">Based on {reviews.length} Google Reviews</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
