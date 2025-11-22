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

def test_env_variables():
    """Test GET /api/test-env - Should return masked environment variables and confirm RESEND_API_KEY is set"""
    print("\n=== Testing GET /api/test-env ===")
    
    try:
        response = requests.get(f"{BACKEND_URL}/test-env", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if response has expected structure
            if "status" not in data or "environment_variables" not in data:
                print("❌ FAIL: Missing required response fields")
                return False
            
            env_vars = data["environment_variables"]
            
            # Check if RESEND_API_KEY is set and has proper length
            if not env_vars.get("RESEND_API_KEY_SET"):
                print("❌ FAIL: RESEND_API_KEY is not set")
                return False
            
            api_key_length = env_vars.get("RESEND_API_KEY_LENGTH", 0)
            if api_key_length < 20:  # Resend API keys should be longer
                print(f"❌ FAIL: RESEND_API_KEY length too short: {api_key_length}")
                return False
            
            # Check if API key is properly masked
            masked_key = env_vars.get("RESEND_API_KEY", "")
            if not masked_key or "NOT_SET" in masked_key:
                print("❌ FAIL: API key not properly masked")
                return False
            
            print(f"✅ PASS: Environment variables loaded correctly")
            print(f"  - RESEND_API_KEY set: {env_vars.get('RESEND_API_KEY_SET')}")
            print(f"  - API key length: {api_key_length}")
            print(f"  - Masked key: {masked_key}")
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

def test_email_sending():
    """Test POST /api/test-email - Should send a test email using Resend and return success with email ID"""
    print("\n=== Testing POST /api/test-email ===")
    
    try:
        response = requests.post(f"{BACKEND_URL}/test-email", json={}, timeout=30)  # Longer timeout for email
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if response has expected structure
            if "status" not in data or data["status"] != "success":
                print("❌ FAIL: Email test did not return success status")
                return False
            
            # Check if email_id is present
            if "email_id" not in data or not data["email_id"]:
                print("❌ FAIL: No email_id returned")
                return False
            
            # Check details
            details = data.get("details", {})
            if not details.get("api_key_set"):
                print("❌ FAIL: API key not set according to response")
                return False
            
            print(f"✅ PASS: Test email sent successfully")
            print(f"  - Email ID: {data['email_id']}")
            print(f"  - Sender: {details.get('sender', 'N/A')}")
            print(f"  - Recipient: {details.get('recipient', 'N/A')}")
            return True
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            if response.status_code == 500:
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data.get('detail', 'No details')}")
                except:
                    pass
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON response - {str(e)}")
        return False

def test_create_appointment():
    """Test POST /api/appointments - Create a new appointment with enhanced debugging"""
    print("\n=== Testing POST /api/appointments ===")
    
    # Test data as specified in the request
    test_data = {
        "name": "Test Customer",
        "email": "test@example.com", 
        "phone": "+1234567890",
        "serviceType": "Custom Paint Job",
        "preferredDate": "2025-12-01",
        "message": "Test booking message"
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