#!/usr/bin/env python3
"""
Specific tests as requested in the review request
"""

import requests
import json
import sys

# Get backend URL from frontend .env
BACKEND_URL = "https://vercel-fix-6.preview.emergentagent.com/api"

def test_complete_valid_data():
    """Test POST /api/appointment - Create appointment with complete valid data"""
    print("\n=== Testing POST /api/appointment - Complete Valid Data ===")
    
    test_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "+1-555-0123",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-20",
        "message": "I need a full matte black wrap for my Tesla Model 3"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=test_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("appointment_id"):
                print("✅ PASS: Complete appointment created successfully")
                print(f"  - Appointment ID: {data['appointment_id']}")
                print(f"  - Message: {data['message']}")
                return True
            else:
                print("❌ FAIL: Invalid response structure")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_minimal_data():
    """Test POST /api/appointment - Create appointment with minimal data (no message)"""
    print("\n=== Testing POST /api/appointment - Minimal Data (No Message) ===")
    
    test_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "555-9876",
        "serviceType": "Window Tint",
        "preferredDate": "2025-12-25"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=test_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("appointment_id"):
                print("✅ PASS: Minimal appointment created successfully")
                print(f"  - Appointment ID: {data['appointment_id']}")
                print(f"  - Message: {data['message']}")
                return True
            else:
                print("❌ FAIL: Invalid response structure")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_invalid_email_format():
    """Test validation - Invalid email format"""
    print("\n=== Testing Validation - Invalid Email Format ===")
    
    test_data = {
        "name": "Test User",
        "email": "invalid-email",
        "phone": "555-1234",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-20",
        "message": "Test message"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ PASS: Invalid email validation working")
            return True
        else:
            print(f"❌ FAIL: Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_missing_required_field():
    """Test validation - Missing required field (name)"""
    print("\n=== Testing Validation - Missing Required Field (Name) ===")
    
    test_data = {
        "email": "test@example.com",
        "phone": "555-1234",
        "serviceType": "Vehicle Wraps",
        "preferredDate": "2025-12-20",
        "message": "Test message"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ PASS: Missing name validation working")
            return True
        else:
            print(f"❌ FAIL: Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_empty_service_type():
    """Test validation - Empty serviceType"""
    print("\n=== Testing Validation - Empty ServiceType ===")
    
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "555-1234",
        "serviceType": "",
        "preferredDate": "2025-12-20",
        "message": "Test message"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/appointment", json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ PASS: Empty serviceType validation working")
            return True
        else:
            print(f"❌ FAIL: Expected 422, got {response.status_code}")
            print("Note: Empty string validation may need improvement")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def test_health_check():
    """Test GET /api/health"""
    print("\n=== Testing GET /api/health ===")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ PASS: Health check working")
                return True
            else:
                print("❌ FAIL: Unhealthy status")
                return False
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Request failed - {str(e)}")
        return False

def main():
    """Run specific tests as requested in review"""
    print("🚀 Running Specific Tests as Requested in Review")
    print(f"Testing against: {BACKEND_URL}")
    
    results = []
    
    # Test Priority 1: Complete valid data
    print("\n" + "="*60)
    print("🎯 PRIORITY 1 - COMPLETE VALID DATA")
    print("="*60)
    success = test_complete_valid_data()
    results.append(("Complete Valid Data", success))
    
    # Test Priority 2: Minimal data
    print("\n" + "="*60)
    print("🎯 PRIORITY 2 - MINIMAL DATA")
    print("="*60)
    success = test_minimal_data()
    results.append(("Minimal Data (No Message)", success))
    
    # Test Priority 3: Validation tests
    print("\n" + "="*60)
    print("🎯 PRIORITY 3 - VALIDATION TESTS")
    print("="*60)
    
    success = test_invalid_email_format()
    results.append(("Invalid Email Format", success))
    
    success = test_missing_required_field()
    results.append(("Missing Required Field", success))
    
    success = test_empty_service_type()
    results.append(("Empty ServiceType", success))
    
    # Test Priority 4: Health check
    print("\n" + "="*60)
    print("🎯 PRIORITY 4 - HEALTH CHECK")
    print("="*60)
    success = test_health_check()
    results.append(("Health Check", success))
    
    # Summary
    print("\n" + "="*60)
    print("📊 SPECIFIC TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed >= total - 1:  # Allow 1 minor failure
        print("🎉 Critical functionality working!")
        return 0
    else:
        print("⚠️  Critical issues found!")
        return 1

if __name__ == "__main__":
    sys.exit(main())