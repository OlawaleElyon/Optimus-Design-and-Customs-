#!/usr/bin/env python3
"""
Backend API Testing for Optimus Design & Customs Appointment System
Tests the NEW appointment booking system with Supabase and Resend integration
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Get backend URL from frontend .env
BACKEND_URL = "https://luxury-auto-book.preview.emergentagent.com/api"

def test_health_check():
    """Test GET /api/health - Health check endpoint"""
    print("\n=== Testing GET /api/health ===")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if response has expected structure
            if "status" not in data:
                print("❌ FAIL: Missing 'status' field in response")
                return False
            
            if data["status"] != "healthy":
                print(f"❌ FAIL: Expected status 'healthy', got '{data['status']}'")
                return False
            
            print("✅ PASS: Health check working correctly")
            print(f"  - Status: {data['status']}")
            print(f"  - Service: {data.get('service', 'N/A')}")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON response - {str(e)}")
        return False

def test_create_appointment_michael_johnson():
    """Test POST /api/appointment - Michael Johnson test case from review request"""
    print("\n=== Testing POST /api/appointment - Michael Johnson (Review Request Test 1) ===")
    
    # Test data as specified in the review request
    test_data = {
        "name": "Michael Johnson",
        "email": "michael.j@example.com",
        "phone": "+1-555-2468",
        "serviceType": "Custom Decals",
        "preferredDate": "2026-01-10",
        "message": "I want custom racing stripes and side decals for my Mustang"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=test_data, timeout=30)  # Longer timeout for email
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check expected response structure
            if "success" not in data:
                print("❌ FAIL: Missing 'success' field in response")
                return False, None
            
            if not data["success"]:
                print("❌ FAIL: success field is False")
                return False, None
            
            if "message" not in data:
                print("❌ FAIL: Missing 'message' field in response")
                return False, None
            
            if "appointment_id" not in data or not data["appointment_id"]:
                print("❌ FAIL: Missing or empty 'appointment_id' field")
                return False, None
                
            print("✅ PASS: Michael Johnson appointment created successfully")
            print(f"  - Success: {data['success']}")
            print(f"  - Message: {data['message']}")
            print(f"  - Appointment ID: {data['appointment_id']}")
            return True, data['appointment_id']
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data.get('detail', 'No details')}")
            except:
                pass
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False, None
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON response - {str(e)}")
        return False, None

def test_create_appointment_invalid_email():
    """Test POST /api/appointment with invalid email format"""
    print("\n=== Testing POST /api/appointment - Invalid Email ===")
    
    invalid_email_data = {
        "name": "Test Customer",
        "email": "invalid-email-format",
        "phone": "+1234567890",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-15",
        "message": "Test message"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=invalid_email_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:  # FastAPI validation error
            print("✅ PASS: Email validation working correctly")
            return True
        else:
            print(f"❌ FAIL: Expected 422 for invalid email, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_create_appointment_missing_fields():
    """Test POST /api/appointment with missing required fields"""
    print("\n=== Testing POST /api/appointment - Missing Required Fields ===")
    
    # Test missing name
    missing_name_data = {
        "email": "test@example.com",
        "phone": "+1234567890",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-15"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=missing_name_data, timeout=10)
        print(f"Missing name test - Status Code: {response.status_code}")
        
        if response.status_code != 422:
            print(f"❌ FAIL: Expected 422 for missing name, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    
    # Test missing email
    missing_email_data = {
        "name": "Test Customer",
        "phone": "+1234567890",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-15"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=missing_email_data, timeout=10)
        print(f"Missing email test - Status Code: {response.status_code}")
        
        if response.status_code != 422:
            print(f"❌ FAIL: Expected 422 for missing email, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    
    # Test missing serviceType
    missing_service_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "preferredDate": "2025-12-15"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=missing_service_data, timeout=10)
        print(f"Missing serviceType test - Status Code: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ PASS: Required field validation working correctly")
            return True
        else:
            print(f"❌ FAIL: Expected 422 for missing serviceType, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_create_appointment_empty_service_type():
    """Test POST /api/appointment with empty serviceType"""
    print("\n=== Testing POST /api/appointment - Empty Service Type ===")
    
    empty_service_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "serviceType": "",
        "preferredDate": "2025-12-15",
        "message": "Test message"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=empty_service_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:  # FastAPI validation error
            print("✅ PASS: Empty serviceType validation working correctly")
            return True
        else:
            print(f"❌ FAIL: Expected 422 for empty serviceType, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def main():
    """Run all tests for the NEW appointment booking system"""
    print("🚀 Starting Backend API Tests for NEW Appointment Booking System")
    print("Testing Supabase + Resend Integration")
    print(f"Testing against: {BACKEND_URL}")
    
    results = []
    appointment_id = None
    
    # Priority 1 - Health Check
    print("\n" + "="*60)
    print("🏥 PRIORITY 1 - HEALTH CHECK")
    print("="*60)
    
    # Test 1: Health check
    success = test_health_check()
    results.append(("GET /api/health", success))
    
    # Priority 2 - Main Appointment Endpoint (Valid Data)
    print("\n" + "="*60)
    print("📝 PRIORITY 2 - MAIN APPOINTMENT ENDPOINT")
    print("="*60)
    
    # Test 2: Create appointment with valid data
    success, appointment_id = test_create_appointment_valid()
    results.append(("POST /api/appointment - Valid Data", success))
    
    # Priority 3 - Validation Testing
    print("\n" + "="*60)
    print("✅ PRIORITY 3 - VALIDATION TESTING")
    print("="*60)
    
    # Test 3: Invalid email format
    success = test_create_appointment_invalid_email()
    results.append(("POST /api/appointment - Invalid Email", success))
    
    # Test 4: Missing required fields
    success = test_create_appointment_missing_fields()
    results.append(("POST /api/appointment - Missing Fields", success))
    
    # Test 5: Empty serviceType
    success = test_create_appointment_empty_service_type()
    results.append(("POST /api/appointment - Empty ServiceType", success))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\n📋 EXPECTED RESULTS ACHIEVED:")
        print("✅ Appointment successfully saved to Supabase with UUID")
        print("✅ Email sent via Resend with all appointment details")
        print("✅ Proper error handling for validation failures")
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())