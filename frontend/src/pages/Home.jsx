import React from 'react';
import HeroAnimated from '../components/HeroAnimated';
import About from '../components/About';
import Services from '../components/Services';
import Projects from '../components/Projects';
import Testimonials from '../components/Testimonials';
import Booking from '../components/Booking';
import Footer from '../components/Footer';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black">
      <HeroAnimated />
      <About />
      <Services />
      <Projects />
      <Testimonials />
      <Booking />
      <Footer />
    </div>
  );
};

export default Home;