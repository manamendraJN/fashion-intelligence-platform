"""
Test script for measurement save and retrieve functionality
"""
from database.db_manager import DatabaseManager
from datetime import datetime

def test_measurement_workflow():
    """Test complete measurement save and retrieval workflow"""
    db = DatabaseManager()
    
    print("=" * 60)
    print("TESTING MEASUREMENT SAVE AND RETRIEVE WORKFLOW")
    print("=" * 60)
    
    # Sample measurements (with underscored keys as expected by database)
    sample_measurements = {
        'height': 175.5,
        'chest': 95.2,
        'waist': 82.0,
        'hip': 98.5,
        'shoulder_breadth': 45.3,
        'shoulder_to_crotch': 62.8,
        'arm_length': 58.4,
        'bicep': 32.1,
        'forearm': 27.5,
        'wrist': 17.2,
        'leg_length': 95.6,
        'thigh': 55.3,
        'calf': 37.8,
        'ankle': 23.4
    }
    
    print("\n1. Testing Save Measurements")
    print("-" * 60)
    try:
        user_id = db.save_user_measurements(
            measurements=sample_measurements,
            user_identifier='default',
            gender='Men'
        )
        print(f"✅ Successfully saved measurements with user_id: {user_id}")
        print(f"   User identifier: default")
        print(f"   Gender: Men")
        print(f"   Number of measurements: {len(sample_measurements)}")
    except Exception as e:
        print(f"❌ Error saving measurements: {e}")
        return
    
    print("\n2. Testing Retrieve Latest Measurements (90 days)")
    print("-" * 60)
    try:
        result = db.get_latest_user_measurements(
            user_identifier='default',
            max_age_days=90
        )
        
        if result:
            print(f"✅ Successfully retrieved measurements")
            print(f"   User ID: {result['user_id']}")
            print(f"   Gender: {result.get('gender')}")
            print(f"   Unit: {result.get('unit')}")
            print(f"   Measured at: {result['measured_at']}")
            print(f"   Number of measurements: {len(result['measurements'])}")
            print(f"\n   Sample measurements:")
            for i, (key, value) in enumerate(list(result['measurements'].items())[:5]):
                print(f"      - {key}: {value} cm")
            if len(result['measurements']) > 5:
                print(f"      ... and {len(result['measurements']) - 5} more")
        else:
            print(f"❌ No measurements found")
            return
    except Exception as e:
        print(f"❌ Error retrieving measurements: {e}")
        return
    
    print("\n3. Verifying Measurement Values Match")
    print("-" * 60)
    mismatches = []
    for key, original_value in sample_measurements.items():
        retrieved_value = result['measurements'].get(key)
        if retrieved_value is None:
            mismatches.append(f"{key}: Not found in retrieved data")
        elif abs(retrieved_value - original_value) > 0.01:
            mismatches.append(f"{key}: {original_value} → {retrieved_value}")
    
    if mismatches:
        print(f"❌ Found {len(mismatches)} mismatches:")
        for mismatch in mismatches:
            print(f"   - {mismatch}")
    else:
        print(f"✅ All {len(sample_measurements)} measurements match perfectly!")
    
    print("\n4. Testing Get All User Measurements")
    print("-" * 60)
    try:
        all_measurements = db.get_all_user_measurements('default')
        print(f"✅ Found {len(all_measurements)} measurement record(s) for user 'default'")
        for i, record in enumerate(all_measurements[:3]):
            print(f"   Record {i+1}: Created at {record.get('created_at')}, {len(record.get('measurements', {}))} measurements")
    except Exception as e:
        print(f"❌ Error getting all measurements: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_measurement_workflow()
