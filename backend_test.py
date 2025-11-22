#!/usr/bin/env python3
"""
Backend API Testing for Optimus Design & Customs Appointment System
Tests the complete booking/appointment system APIs
"""

import requests
import json
import sys
from datetime import datetime
import uuid

# Get backend URL from frontend .env
BACKEND_URL = "https://luxury-auto-book.preview.emergentagent.com/api"

def test_create_appointment():
    """Test POST /api/appointments - Create a new appointment"""
    print("\n=== Testing POST /api/appointments ===")
    
    # Test data as specified in the request
    test_data = {
        "name": "John Doe",
        "email": "john@example.com", 
        "phone": "(555) 123-4567",
        "serviceType": "vehicle-wrap",
        "preferredDate": "2025-07-20",
        "message": "I want a matte black wrap for my Tesla Model 3"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointments", json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            # Verify required fields are present
            required_fields = ['id', 'name', 'email', 'phone', 'serviceType', 'preferredDate', 'status', 'createdAt']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"❌ FAIL: Missing required fields: {missing_fields}")
                return False, None
            
            # Verify default status is "pending"
            if data.get('status') != 'pending':
                print(f"❌ FAIL: Expected status 'pending', got '{data.get('status')}'")
                return False, None
                
            print("✅ PASS: Appointment created successfully")
            print(f"Created appointment ID: {data['id']}")
            return True, data['id']
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False, None
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON response - {str(e)}")
        return False, None

def test_create_appointment_validation():
    """Test POST /api/appointments with invalid data"""
    print("\n=== Testing POST /api/appointments - Validation ===")
    
    # Test invalid email
    invalid_email_data = {
        "name": "Jane Doe",
        "email": "invalid-email",
        "phone": "(555) 123-4567", 
        "serviceType": "vehicle-wrap",
        "preferredDate": "2025-07-20",
        "message": "Test message"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointments", json=invalid_email_data, timeout=10)
        print(f"Invalid email test - Status Code: {response.status_code}")
        
        if response.status_code == 422:  # FastAPI validation error
            print("✅ PASS: Email validation working correctly")
        else:
            print(f"❌ FAIL: Expected 422 for invalid email, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    
    # Test missing required fields
    incomplete_data = {
        "name": "Jane Doe"
        # Missing required fields
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointments", json=incomplete_data, timeout=10)
        print(f"Missing fields test - Status Code: {response.status_code}")
        
        if response.status_code == 422:  # FastAPI validation error
            print("✅ PASS: Required field validation working correctly")
            return True
        else:
            print(f"❌ FAIL: Expected 422 for missing fields, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_get_all_appointments():
    """Test GET /api/appointments - Get all appointments"""
    print("\n=== Testing GET /api/appointments ===")
    
    try:
        response = requests.get(f"{BACKEND_URL}/appointments", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            
            if isinstance(data, list):
                print(f"✅ PASS: Retrieved {len(data)} appointments")
                
                # Check if appointments are sorted by createdAt (newest first)
                if len(data) > 1:
                    dates = [appt.get('createdAt') for appt in data if 'createdAt' in appt]
                    if dates:
                        # Convert to datetime for comparison
                        parsed_dates = []
                        for date_str in dates:
                            try:
                                parsed_dates.append(datetime.fromisoformat(date_str.replace('Z', '+00:00')))
                            except:
                                parsed_dates.append(datetime.fromisoformat(date_str))
                        
                        is_sorted = all(parsed_dates[i] >= parsed_dates[i+1] for i in range(len(parsed_dates)-1))
                        if is_sorted:
                            print("✅ PASS: Appointments sorted by createdAt (newest first)")
                        else:
                            print("❌ FAIL: Appointments not properly sorted")
                            return False
                
                return True
            else:
                print(f"❌ FAIL: Expected list, got {type(data)}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON response - {str(e)}")
        return False

def test_get_single_appointment(appointment_id):
    """Test GET /api/appointments/{id} - Get single appointment"""
    print(f"\n=== Testing GET /api/appointments/{appointment_id} ===")
    
    try:
        response = requests.get(f"{BACKEND_URL}/appointments/{appointment_id}", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Retrieved appointment: {data.get('name', 'Unknown')}")
            
            # Verify it's the correct appointment
            if data.get('id') == appointment_id:
                print("✅ PASS: Retrieved correct appointment")
                return True
            else:
                print(f"❌ FAIL: Expected ID {appointment_id}, got {data.get('id')}")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON response - {str(e)}")
        return False

def test_get_nonexistent_appointment():
    """Test GET /api/appointments/{id} with invalid ID"""
    print("\n=== Testing GET /api/appointments with invalid ID ===")
    
    fake_id = str(uuid.uuid4())
    
    try:
        response = requests.get(f"{BACKEND_URL}/appointments/{fake_id}", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ PASS: Correctly returned 404 for non-existent appointment")
            return True
        else:
            print(f"❌ FAIL: Expected 404, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Backend API Tests for Optimus Design & Customs")
    print(f"Testing against: {BACKEND_URL}")
    
    results = []
    
    # Test 1: Create appointment
    success, appointment_id = test_create_appointment()
    results.append(("Create Appointment", success))
    
    # Test 2: Validation tests
    success = test_create_appointment_validation()
    results.append(("Appointment Validation", success))
    
    # Test 3: Get all appointments
    success = test_get_all_appointments()
    results.append(("Get All Appointments", success))
    
    # Test 4: Get single appointment (if we have an ID)
    if appointment_id:
        success = test_get_single_appointment(appointment_id)
        results.append(("Get Single Appointment", success))
    
    # Test 5: Get non-existent appointment
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