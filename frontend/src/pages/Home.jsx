import React, { useEffect, useState } from 'react';
import Hero from '../components/Hero';
import About from '../components/About';
import Services from '../components/Services';
import Projects from '../components/Projects';
import Booking from '../components/Booking';
import Footer from '../components/Footer';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-950 to-black">
      <Hero />
      <About />
      <Services />
      <Projects />
      <Booking />
      <Footer />
    </div>
  );
};

export default Home;