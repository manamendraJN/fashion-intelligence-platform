import sys
sys.path.insert(0, './backend')

from services.size_matching_service import size_matching_service

# Test with actual user measurements
user_measurements = {
    'chest': 96,
    'waist': 82,
    'hip': 98
}

print("Testing Size Recommendations")
print("=" * 60)
print(f"User Measurements: Chest={user_measurements['chest']}, Waist={user_measurements['waist']}, Hip={user_measurements['hip']}")
print()

# Test for T-Shirt category (category_id = 1)
category_id = 1
brands_to_test = [1, 2, 3, 4]  # Nike, Adidas, Zara, H&M

for brand_id in brands_to_test:
    print(f"\nTesting Brand ID {brand_id}...")
    result = size_matching_service.find_best_size(
        user_measurements,
        brand_id,
        category_id,
        'Regular'
    )
    
    if 'error' not in result:
        print(f"  ✓ Brand: {result['brand_name']}")
        print(f"  ✓ Recommended Size: {result['recommended_size']}")
        print(f"  ✓ Confidence: {result['confidence']:.1f}%")
        print(f"  ✓ Match Score: {result['match_score']:.1f}%")
        if result.get('match_details'):
            print(f"  ✓ Match Details:")
            for detail in result['match_details']:
                print(f"    - {detail['measurement']}: User={detail['user_value']}, Size Range={detail['size_range']}, Fit={detail['fit']}")
    else:
        print(f"  ✗ Error: {result['error']}")

# Now test multiple brands at once
print("\n" + "=" * 60)
print("Testing Multiple Brands Recommendation:")
print("=" * 60)

recommendations = size_matching_service.get_recommendations_for_multiple_brands(
    user_measurements,
    category_id,
    gender=None,
    fit_type='Regular',
    min_confidence=60.0
)

print(f"\nFound {len(recommendations)} recommendations:")
for rec in recommendations:
    print(f"  • {rec['brand_name']}: Size {rec['recommended_size']} ({rec['confidence']:.1f}% confidence)")
