"""
Test script to verify measurement history endpoint
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_measurement_history():
    """Test the measurement history endpoint"""
    print("Testing measurement history endpoint...")
    print("-" * 50)
    
    try:
        # Test with default user
        response = requests.get(f"{BASE_URL}/api/size/measurements/history", params={
            'user_identifier': 'default'
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        data = response.json()
        print(json.dumps(data, indent=2))
        
        if data.get('success'):
            count = data.get('data', {}).get('count', 0)
            print(f"\n✅ Success! Found {count} measurement records")
            
            if count > 0:
                measurements = data.get('data', {}).get('measurements', [])
                print(f"\nFirst record:")
                print(f"  Date: {measurements[0].get('measured_at')}")
                print(f"  Measurements: {list(measurements[0].get('measurements', {}).keys())}")
        else:
            print(f"\n❌ Error: {data.get('error')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Make sure it's running on port 5000.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_measurement_history()
