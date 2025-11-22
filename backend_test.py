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

def test_create_appointment_valid():
    """Test POST /api/appointment - Create appointment with valid data"""
    print("\n=== Testing POST /api/appointment - Valid Data ===")
    
    # Test data as specified in the review request
    test_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-15",
        "message": "I need a full vehicle wrap for my car"
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
                
            print("✅ PASS: Appointment created successfully")
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
    """Run all tests"""
    print("🚀 Starting Backend API Tests for Optimus Design & Customs")
    print(f"Testing against: {BACKEND_URL}")
    
    results = []
    
    # Priority 1 - Debugging Endpoints
    print("\n" + "="*60)
    print("🔧 PRIORITY 1 - DEBUGGING ENDPOINTS")
    print("="*60)
    
    # Test 1: Environment variables
    success = test_env_variables()
    results.append(("GET /api/test-env", success))
    
    # Test 2: Email sending
    success = test_email_sending()
    results.append(("POST /api/test-email", success))
    
    # Priority 2 - Main Booking Endpoint
    print("\n" + "="*60)
    print("📝 PRIORITY 2 - MAIN BOOKING ENDPOINT")
    print("="*60)
    
    # Test 3: Create appointment
    success, appointment_id = test_create_appointment()
    results.append(("POST /api/appointments", success))
    
    # Priority 3 - Validation
    print("\n" + "="*60)
    print("✅ PRIORITY 3 - VALIDATION")
    print("="*60)
    
    # Test 4: Validation tests
    success = test_create_appointment_validation()
    results.append(("Appointment Validation", success))
    
    # Additional tests
    print("\n" + "="*60)
    print("🔍 ADDITIONAL TESTS")
    print("="*60)
    
    # Test 5: Get all appointments
    success = test_get_all_appointments()
    results.append(("Get All Appointments", success))
    
    # Test 6: Get single appointment (if we have an ID)
    if appointment_id:
        success = test_get_single_appointment(appointment_id)
        results.append(("Get Single Appointment", success))
    
    # Test 7: Get non-existent appointment
    success = test_get_nonexistent_appointment()
    results.append(("Get Non-existent Appointment", success))
    
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
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())