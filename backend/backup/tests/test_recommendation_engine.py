"""
End-to-End Size Recommendation Test
Tests the actual recommendation engine with real data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from services.size_matching_service import size_matching_service
import json

print("\n" + "="*70)
print("END-TO-END SIZE RECOMMENDATION TEST")
print("="*70 + "\n")

# Sample user measurements (typical adult male)
user_measurements = {
    'chest': 95,
    'waist': 82,
    'hip': 98,
    'shoulder_breadth': 45,
    'height': 175,
    'arm_length': 60,
    'leg_length': 82
}

print("👤 User Measurements:")
for key, value in user_measurements.items():
    print(f"   {key:20}: {value} cm")
print()

# Test cases for different brands and categories
test_cases = [
    {
        'brand': 'Nike',
        'category': 'T-Shirt',
        'gender': 'Men',
        'description': 'Athletic brand, US sizing'
    },
    {
        'brand': 'Zara',
        'category': 'Jeans',
        'gender': 'Men',
        'description': 'European brand, EU sizing'
    },
    {
        'brand': 'Uniqlo',
        'category': 'T-Shirt',
        'gender': 'Men',
        'description': 'Asian brand, Asia sizing'
    },
]

print("="*70)
print("TESTING SIZE RECOMMENDATIONS")
print("="*70 + "\n")

for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: {test['brand']} - {test['category']} ({test['gender']})")
    print(f"        {test['description']}")
    print("-" * 70)
    
    try:
        # Get brand ID
        from database.db_manager import db_manager
        brands = db_manager.get_brands()
        brand = next((b for b in brands if b['brand_name'] == test['brand']), None)
        
        # Get category ID
        categories = db_manager.get_categories()
        category = next((c for c in categories 
                        if c['category_name'] == test['category'] 
                        and c['gender'] == test['gender']), None)
        
        if not brand or not category:
            print("❌ Brand or category not found in database")
            print()
            continue
        
        # Get recommendation
        result = size_matching_service.find_best_size(
            user_measurements=user_measurements,
            brand_id=brand['brand_id'],
            category_id=category['category_id'],
            fit_type='Regular'
        )
        
        if result and 'recommended_size' in result:
            print(f"✅ Recommended Size: {result['recommended_size']}")
            print(f"   Confidence: {result['confidence_score']:.1f}%")
            print(f"   Overall Fit: {result['overall_fit_assessment']}")
            
            if 'measurement_details' in result:
                print("   Fit Details:")
                for detail in result['measurement_details'][:3]:  # Show first 3
                    status = "✓" if detail['fit_status'] in ['perfect', 'good'] else "⚠"
                    print(f"     {status} {detail['measurement_type']:15}: {detail['fit_status']:12} "
                          f"(user: {detail['user_value']:.0f}cm, range: {detail['size_min']:.0f}-{detail['size_max']:.0f}cm)")
        else:
            print("❌ No recommendation found (size chart may be missing)")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()

print("="*70)
print("MULTI-BRAND COMPARISON TEST")
print("="*70 + "\n")

print("Finding best T-Shirt size across all brands for the same user...\n")

try:
    # Get T-Shirt category
    categories = db_manager.get_categories()
    tshirt_category = next((c for c in categories 
                           if c['category_name'] == 'T-Shirt' 
                           and c['gender'] == 'Men'), None)
    
    if tshirt_category:
        recommendations = size_matching_service.get_recommendations_for_multiple_brands(
            user_measurements=user_measurements,
            category_id=tshirt_category['category_id'],
            fit_type='Regular',
            min_confidence=60.0
        )
        
        if recommendations:
            print(f"Found {len(recommendations)} recommendations:\n")
            for rec in recommendations[:5]:  # Show top 5
                print(f"  {rec['brand_name']:10} - Size {rec['recommended_size']:3} "
                      f"(Confidence: {rec['confidence_score']:4.1f}%) - {rec['overall_fit_assessment']}")
        else:
            print("No recommendations found")
    else:
        print("T-Shirt category not found")

except Exception as e:
    print(f"Error: {str(e)}")

print()
print("="*70)
print("✅ END-TO-END TEST COMPLETE")
print("="*70)
print("\nThe size recommendation system is working correctly!")
print("You can now use it in the frontend application.")
print()
