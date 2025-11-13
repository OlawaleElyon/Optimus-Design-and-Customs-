import React, { useEffect, useRef, useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Mail, Phone, Instagram, MapPin, Clock } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

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
    setLoading(true);

    try {
      const response = await axios.post(`${API}/appointments`, formData);
      
      toast.success("Your request has been sent successfully! We'll contact you shortly.");

      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        serviceType: '',
        preferredDate: '',
        message: ''
      });
    } catch (error) {
      console.error('Error submitting appointment:', error);
      toast.error("Failed to submit request. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="booking" ref={sectionRef} className="py-24 px-6 bg-gradient-to-b from-gray-900 to-black">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className={`text-center mb-16 transition-all duration-1000 ease-out ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}>
          <h2 className="text-5xl md:text-6xl font-bold mb-4">
            <span className="text-white">Book Your </span>
            <span className="text-purple-400">Appointment</span>
          </h2>
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Contact Info */}
          <div className={`transition-all duration-1000 delay-200 ease-out ${
            isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-20'
          }`}>
            <div className="space-y-8">
              <div>
                <h3 className="text-3xl font-bold text-white mb-6">Get In Touch</h3>
                <p className="text-gray-400 text-lg">
                  Ready to transform your ride? Contact us today and let's bring your vision to life.
                </p>
              </div>

              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="bg-purple-600/20 p-3 rounded-lg">
                    <Mail className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Email</p>
                    <p className="text-white font-semibold">info@optimusdesign.com</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="bg-purple-600/20 p-3 rounded-lg">
                    <Phone className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Phone</p>
                    <p className="text-white font-semibold">(555) 123-4567</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="bg-purple-600/20 p-3 rounded-lg">
                    <Instagram className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Instagram</p>
                    <p className="text-white font-semibold">@optimusdesign</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="bg-purple-600/20 p-3 rounded-lg">
                    <MapPin className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Address</p>
                    <p className="text-white font-semibold">123 Custom Street, Auto City, CA 90210</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="bg-purple-600/20 p-3 rounded-lg">
                    <Clock className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <p className="text-gray-400 text-sm">Hours</p>
                    <p className="text-white font-semibold">Mon-Fri: 9AM - 6PM</p>
                    <p className="text-white font-semibold">Sat: 10AM - 4PM</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className={`transition-all duration-1000 delay-400 ease-out ${
            isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-20'
          }`}>
            <div className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm p-8 rounded-2xl border border-purple-500/20">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="text-white font-semibold mb-2 block">Name</label>
                    <Input 
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      className="bg-gray-900/50 border-purple-500/30 text-white focus:border-purple-500 transition-colors"
                      placeholder="Your name"
                    />
                  </div>

                  <div>
                    <label className="text-white font-semibold mb-2 block">Email</label>
                    <Input 
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="bg-gray-900/50 border-purple-500/30 text-white focus:border-purple-500 transition-colors"
                      placeholder="your@email.com"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="text-white font-semibold mb-2 block">Phone</label>
                    <Input 
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      required
                      className="bg-gray-900/50 border-purple-500/30 text-white focus:border-purple-500 transition-colors"
                      placeholder="(555) 123-4567"
                    />
                  </div>

                  <div>
                    <label className="text-white font-semibold mb-2 block">Service Type</label>
                    <Select onValueChange={handleServiceChange} value={formData.serviceType} required>
                      <SelectTrigger className="bg-gray-900/50 border-purple-500/30 text-white focus:border-purple-500">
                        <SelectValue placeholder="Select a service" />
                      </SelectTrigger>
                      <SelectContent className="bg-gray-900 border-purple-500/30">
                        <SelectItem value="vehicle-wrap" className="text-white hover:bg-purple-600">Vehicle Wrap</SelectItem>
                        <SelectItem value="window-tint" className="text-white hover:bg-purple-600">Window Tint</SelectItem>
                        <SelectItem value="custom-decals" className="text-white hover:bg-purple-600">Custom Decals</SelectItem>
                        <SelectItem value="consultation" className="text-white hover:bg-purple-600">Consultation</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div>
                  <label className="text-white font-semibold mb-2 block">Preferred Date</label>
                  <Input 
                    type="date"
                    name="preferredDate"
                    value={formData.preferredDate}
                    onChange={handleChange}
                    required
                    className="bg-gray-900/50 border-purple-500/30 text-white focus:border-purple-500 transition-colors"
                  />
                </div>

                <div>
                  <label className="text-white font-semibold mb-2 block">Project Details</label>
                  <Textarea 
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    rows={5}
                    className="bg-gray-900/50 border-purple-500/30 text-white focus:border-purple-500 transition-colors resize-none"
                    placeholder="Tell us about your project..."
                  />
                </div>

                <Button 
                  type="submit"
                  disabled={loading}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white py-6 text-lg rounded-md font-semibold transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-purple-500/50"
                >
                  {loading ? 'Submitting...' : 'Submit Request'}
                </Button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Booking;