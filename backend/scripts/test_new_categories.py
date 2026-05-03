"""Test recommendations for new garment categories"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.size_matching_service import size_matching_service
from database.db_manager import db_manager

def test_new_categories():
    """Test recommendations for all new categories"""
    
    print("\n" + "="*70)
    print("TESTING NEW GARMENT CATEGORIES")
    print("="*70)
    
    test_cases = [
        {
            'name': 'John',
            'measurements': {'chest': 96, 'waist': 84, 'shoulder_breadth': 48, 'sleeve_length': 65},
            'category': 'Jacket',
            'gender': 'Men',
            'brand': 'Nike'
        },
        {
            'name': 'Mike',
            'measurements': {'chest': 100, 'waist': 88, 'shoulder_breadth': 49},
            'category': 'Hoodie',
            'gender': 'Men',
            'brand': 'Adidas'
        },
        {
            'name': 'Tom',
            'measurements': {'waist': 80, 'hip': 94, 'leg_length': 46},
            'category': 'Shorts',
            'gender': 'Men',
            'brand': 'Puma'
        },
        {
            'name': 'Alex',
            'measurements': {'chest': 94, 'waist': 82, 'shoulder_breadth': 47},
            'category': 'Polo',
            'gender': 'Men',
            'brand': 'Gap'
        },
        {
            'name': 'David',
            'measurements': {'chest': 100, 'waist': 88, 'shoulder_breadth': 49, 'sleeve_length': 66},
            'category': 'Sweater',
            'gender': 'Men',
            'brand': 'H&M'
        },
        {
            'name': 'Sarah',
            'measurements': {'chest': 88, 'waist': 70, 'shoulder_breadth': 41, 'sleeve_length': 61},
            'category': 'Jacket',
            'gender': 'Women',
            'brand': 'Zara'
        },
        {
            'name': 'Emma',
            'measurements': {'chest': 90, 'waist': 72, 'shoulder_breadth': 42},
            'category': 'Hoodie',
            'gender': 'Women',
            'brand': 'Uniqlo'
        },
        {
            'name': 'Lisa',
            'measurements': {'waist': 68, 'hip': 94, 'leg_length': 39},
            'category': 'Shorts',
            'gender': 'Women',
            'brand': 'Under Armour'
        },
        {
            'name': 'Amy',
            'measurements': {'waist': 72, 'hip': 98, 'length': 50},
            'category': 'Skirt',
            'gender': 'Women',
            'brand': 'Mango'
        },
        {
            'name': 'Kate',
            'measurements': {'chest': 92, 'waist': 74, 'shoulder_breadth': 43, 'sleeve_length': 63},
            'category': 'Sweater',
            'gender': 'Women',
            'brand': 'COS'
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─'*70}")
        print(f"TEST {i}: {test['name']} - {test['brand']} {test['category']} ({test['gender']})")
        print(f"{'─'*70}")
        
        try:
            # Get brand and category IDs
            brands = db_manager.get_brands()
            brand = next((b for b in brands if b['brand_name'] == test['brand']), None)
            if not brand:
                print(f"❌ FAILED: Brand '{test['brand']}' not found")
                failed += 1
                continue
            
            category_id = db_manager.get_or_create_category(test['category'], test['gender'])
            
            # Get recommendation
            result = size_matching_service.find_best_size(
                user_measurements=test['measurements'],
                brand_id=brand['brand_id'],
                category_id=category_id,
                fit_type='Regular'
            )
            
            if result.get('error'):
                print(f"❌ FAILED: {result['error']}")
                failed += 1
            else:
                print(f"✅ SUCCESS")
                print(f"   Size: {result.get('recommended_size', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.1f}%")
                print(f"   Match Score: {result.get('match_score', 0):.1f}/100")
                passed += 1
        
        except Exception as e:
            print(f"❌ FAILED with exception: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    if failed == 0:
        print("✅ ALL NEW CATEGORIES WORKING PERFECTLY!")
    print("="*70)


if __name__ == "__main__":
    test_new_categories()
