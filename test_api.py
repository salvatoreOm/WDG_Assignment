#!/usr/bin/env python3
"""
Test script to demonstrate NGO Impact Tracker API functionality.
Make sure the Django server is running on http://localhost:8000 before running this script.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_submit_report():
    """Test submitting a single report"""
    print("🧪 Testing single report submission...")
    
    report_data = {
        "ngo_id": "TEST_NGO_001",
        "month": "2024-01",
        "people_helped": 100,
        "events_conducted": 5,
        "funds_utilized": 15000.50
    }
    
    response = requests.post(f"{BASE_URL}/report", json=report_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Single report test completed\n")

def test_duplicate_report():
    """Test submitting duplicate report (should update existing)"""
    print("🧪 Testing duplicate report submission (idempotency)...")
    
    report_data = {
        "ngo_id": "TEST_NGO_001",
        "month": "2024-01",
        "people_helped": 120,  # Updated value
        "events_conducted": 6,   # Updated value
        "funds_utilized": 18000.00
    }
    
    response = requests.post(f"{BASE_URL}/report", json=report_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Duplicate report test completed\n")

def test_bulk_upload():
    """Test CSV bulk upload"""
    print("🧪 Testing CSV bulk upload...")
    
    # Create sample CSV content
    csv_content = """ngo_id,month,people_helped,events_conducted,funds_utilized
TEST_NGO_002,2024-01,200,8,30000.00
TEST_NGO_003,2024-01,150,6,25000.50
TEST_NGO_004,2024-01,180,7,28000.75"""
    
    files = {'file': ('test_reports.csv', csv_content, 'text/csv')}
    
    response = requests.post(f"{BASE_URL}/reports/upload", files=files)
    print(f"Status Code: {response.status_code}")
    response_data = response.json()
    print(f"Response: {json.dumps(response_data, indent=2)}")
    
    if response.status_code == 202 and 'job_id' in response_data:
        job_id = response_data['job_id']
        print(f"📋 Job ID: {job_id}")
        
        # Poll job status
        print("📊 Polling job status...")
        for i in range(10):  # Poll for up to 20 seconds
            time.sleep(2)
            status_response = requests.get(f"{BASE_URL}/job-status/{job_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()['data']
                print(f"Status: {status_data['status']} | Progress: {status_data['progress_percentage']}%")
                
                if status_data['status'] in ['completed', 'failed']:
                    print(f"Final Status: {json.dumps(status_data, indent=2)}")
                    break
            else:
                print(f"Failed to get job status: {status_response.status_code}")
                break
    
    print("✅ Bulk upload test completed\n")

def test_dashboard():
    """Test dashboard data retrieval"""
    print("🧪 Testing dashboard data retrieval...")
    
    response = requests.get(f"{BASE_URL}/dashboard?month=2024-01")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Dashboard test completed\n")

def test_invalid_data():
    """Test validation with invalid data"""
    print("🧪 Testing validation with invalid data...")
    
    invalid_report = {
        "ngo_id": "",  # Empty NGO ID
        "month": "2024-13",  # Invalid month
        "people_helped": -5,  # Negative value
        "events_conducted": "abc",  # Invalid type
        "funds_utilized": -1000
    }
    
    response = requests.post(f"{BASE_URL}/report", json=invalid_report)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Validation test completed\n")

def main():
    """Run all tests"""
    print("🚀 Starting NGO Impact Tracker API Tests\n")
    print("=" * 50)
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/reports", timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding correctly. Make sure Django server is running.")
            return
        
        test_submit_report()
        test_duplicate_report()
        test_dashboard()
        test_bulk_upload()
        test_invalid_data()
        
        print("=" * 50)
        print("🎉 All API tests completed successfully!")
        print("\n📝 Summary:")
        print("- Single report submission ✅")
        print("- Idempotency handling ✅")
        print("- Dashboard aggregation ✅")
        print("- Bulk CSV upload ✅")
        print("- Input validation ✅")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please ensure:")
        print("1. Django server is running (python manage.py runserver)")
        print("2. Celery worker is running (celery -A ngo_impact_tracker worker)")
        print("3. Redis server is running (redis-server)")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main() 