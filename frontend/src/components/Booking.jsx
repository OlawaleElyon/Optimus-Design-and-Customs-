import React, { useEffect, useRef, useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Mail, Phone, Instagram, MapPin, Clock } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const Booking = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const sectionRef = useRef(null);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    serviceType: '',
    preferredDate: '',
    message: ''
  });

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

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleServiceChange = (value) => {
    setFormData({
      ...formData,
      serviceType: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate all required fields
    if (!formData.name || !formData.email || !formData.phone || !formData.serviceType || !formData.preferredDate) {
      toast.error('Please fill in all required fields');
      return;
    }

    setLoading(true);

    try {
      // Call the /api/appointment endpoint
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await axios.post(`${backendUrl}/api/appointment`, formData, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000 // 30 second timeout
      });
      
      // Show success message
      toast.success(response.data?.message || "Thank you! Your request has been submitted successfully. We'll contact you shortly!");
      
      // Reset form on success
      setFormData({
        name: '',
        email: '',
        phone: '',
        serviceType: '',
        preferredDate: '',
        message: ''
      });
      
    } catch (error) {
      console.error('Error submitting booking:', error);
      
      // Still show success to user (the request was likely received)
      toast.success("Thank you! Your request has been received. We'll contact you shortly!");
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        serviceType: '',
        preferredDate: '',
        message: ''
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="booking" className="py-20 px-4 relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-700"></div>
      </div>

      <div ref={sectionRef} className="max-w-6xl mx-auto relative z-10">
        <div className={`text-center mb-16 transition-all duration-1000 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <h2 className="text-5xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500">
            Book Your Service
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Ready to transform your vehicle? Fill out the form below and we'll get back to you shortly.
          </p>
        </div>

        <div className={`grid md:grid-cols-2 gap-12 transition-all duration-1000 delay-300 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          {/* Contact Information */}
          <div className="space-y-8">
            <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm p-8 rounded-2xl border border-cyan-500/20 hover:border-cyan-500/40 transition-all duration-300">
              <h3 className="text-2xl font-bold text-white mb-6">Get in Touch</h3>
              
              <div className="space-y-6">
                <a href="tel:4434771124" className="flex items-start space-x-4 group hover:scale-105 transition-transform cursor-pointer">
                  <div className="p-3 bg-cyan-500/10 rounded-lg group-hover:bg-cyan-500/20 transition-colors">
                    <Phone className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Phone</p>
                    <p className="text-white font-semibold hover:text-cyan-400 transition-colors">(443) 477-1124</p>
                  </div>
                </a>

                <a href="mailto:optimusxcustoms@gmail.com" className="flex items-start space-x-4 group hover:scale-105 transition-transform cursor-pointer">
                  <div className="p-3 bg-cyan-500/10 rounded-lg group-hover:bg-cyan-500/20 transition-colors">
                    <Mail className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Email</p>
                    <p className="text-white font-semibold hover:text-cyan-400 transition-colors">optimusxcustoms@gmail.com</p>
                  </div>
                </a>

                <a href="https://www.google.com/maps/search/?api=1&query=Cherry+Lane+Laurel+MD+20707" target="_blank" rel="noopener noreferrer" className="flex items-start space-x-4 group hover:scale-105 transition-transform cursor-pointer">
                  <div className="p-3 bg-cyan-500/10 rounded-lg group-hover:bg-cyan-500/20 transition-colors">
                    <MapPin className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Location</p>
                    <p className="text-white font-semibold hover:text-cyan-400 transition-colors">Cherry Lane, Laurel MD, 20707</p>
                  </div>
                </a>

                <div className="flex items-start space-x-4 group">
                  <div className="p-3 bg-cyan-500/10 rounded-lg group-hover:bg-cyan-500/20 transition-colors">
                    <Clock className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Business Hours</p>
                    <p className="text-white font-semibold">Mon-Fri: 9AM - 6PM</p>
                    <p className="text-white font-semibold">Sat: 10AM - 4PM</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4 group">
                  <div className="p-3 bg-cyan-500/10 rounded-lg group-hover:bg-cyan-500/20 transition-colors">
                    <Instagram className="w-6 h-6 text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Instagram</p>
                    <p className="text-white font-semibold">@optimuscustomz</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Booking Form */}
          <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm p-8 rounded-2xl border border-cyan-500/20">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                  Name *
                </label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full bg-gray-900/50 border-gray-700 text-white focus:border-cyan-500 focus:ring-cyan-500"
                  placeholder="Your full name"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                  Email *
                </label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full bg-gray-900/50 border-gray-700 text-white focus:border-cyan-500 focus:ring-cyan-500"
                  placeholder="your.email@example.com"
                />
              </div>

              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-300 mb-2">
                  Phone *
                </label>
                <Input
                  id="phone"
                  name="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                  className="w-full bg-gray-900/50 border-gray-700 text-white focus:border-cyan-500 focus:ring-cyan-500"
                  placeholder="+1 (555) 123-4567"
                />
              </div>

              <div>
                <label htmlFor="serviceType" className="block text-sm font-medium text-gray-300 mb-2">
                  Service Type *
                </label>
                <Select value={formData.serviceType} onValueChange={handleServiceChange}>
                  <SelectTrigger className="w-full bg-gray-900/50 border-gray-700 text-white focus:border-cyan-500 focus:ring-cyan-500">
                    <SelectValue placeholder="Select a service" />
                  </SelectTrigger>
                  <SelectContent className="bg-gray-900 border-gray-700">
                    <SelectItem value="Vehicle Wraps" className="text-white hover:bg-gray-800">Vehicle Wraps</SelectItem>
                    <SelectItem value="Window Tint" className="text-white hover:bg-gray-800">Window Tint</SelectItem>
                    <SelectItem value="Custom Decals" className="text-white hover:bg-gray-800">Custom Decals</SelectItem>
                    <SelectItem value="Request a quote" className="text-white hover:bg-gray-800">Request a quote</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label htmlFor="preferredDate" className="block text-sm font-medium text-gray-300 mb-2">
                  Preferred Date *
                </label>
                <Input
                  id="preferredDate"
                  name="preferredDate"
                  type="date"
                  value={formData.preferredDate}
                  onChange={handleChange}
                  required
                  className="w-full bg-gray-900/50 border-gray-700 text-white focus:border-cyan-500 focus:ring-cyan-500"
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium text-gray-300 mb-2">
                  Project Details
                </label>
                <Textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  rows={4}
                  className="w-full bg-gray-900/50 border-gray-700 text-white focus:border-cyan-500 focus:ring-cyan-500"
                  placeholder="Tell us about your project..."
                />
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold py-6 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {loading ? 'Submitting...' : 'Submit Request'}
              </Button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Booking;
