"""Quick test to verify recommendations work for all categories"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.size_matching_service import size_matching_service
from database.db_manager import db_manager

def test_all_categories():
    """Test that recommendations work for different categories"""
    
    print("\n" + "="*70)
    print("TESTING SIZE RECOMMENDATIONS - ALL CATEGORIES")
    print("="*70)
    
    test_cases = [
        {
            'name': 'John',
            'measurements': {'chest': 95, 'waist': 80, 'shoulder_breadth': 45},
            'category': 'T-Shirt',
            'gender': 'Men',
            'brand': 'Nike'
        },
        {
            'name': 'Sarah',
            'measurements': {'chest': 88, 'waist': 70, 'hip': 96},
            'category': 'Dress',
            'gender': 'Women',
            'brand': 'Zara'
        },
        {
            'name': 'Mike',
            'measurements': {'waist': 81, 'hip': 97, 'leg_length': 82},
            'category': 'Jeans',
            'gender': 'Men',
            'brand': 'Levi\'s'
        },
        {
            'name': 'Emma',
            'measurements': {'waist': 66, 'hip': 91, 'leg_length': 77},
            'category': 'Jeans',
            'gender': 'Women',
            'brand': 'H&M'
        },
        {
            'name': 'David',
            'measurements': {'waist': 86, 'hip': 102, 'leg_length': 82},
            'category': 'Pants',
            'gender': 'Men',
            'brand': 'Gap'
        },
        {
            'name': 'Alex',
            'measurements': {'chest': 96, 'waist': 84, 'shoulder_breadth': 48, 'sleeve_length': 64},
            'category': 'Shirt',
            'gender': 'Men',
            'brand': 'Uniqlo'
        },
        {
            'name': 'Lisa',
            'measurements': {'chest': 86, 'waist': 68, 'shoulder_breadth': 40},
            'category': 'T-Shirt',
            'gender': 'Women',
            'brand': 'Adidas'
        },
    ]
    
    all_passed = True
    
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
                all_passed = False
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
                all_passed = False
            else:
                print(f"✅ SUCCESS")
                print(f"   Recommended Size: {result.get('recommended_size', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.1f}%")
                print(f"   Match Score: {result.get('match_score', 0):.1f}/100")
                alt_count = len(result.get('alternatives', []))
                print(f"   Alternatives: {alt_count} sizes")
        
        except Exception as e:
            print(f"❌ FAILED with exception: {e}")
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Recommendations work for all categories!")
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
    print("="*70)


if __name__ == "__main__":
    test_all_categories()
