"""
Test Size Matching Algorithm
Tests the algorithm with sample user measurements across multiple brands
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.size_matching_service import size_matching_service
from database.db_manager import db_manager


def test_single_brand():
    """Test recommendation for a single brand"""
    print("\n" + "="*70)
    print("TEST 1: Single Brand Size Recommendation")
    print("="*70 + "\n")
    
    # Sample user: John (average male)
    user_measurements = {
        'chest': 98,
        'waist': 84,
        'shoulder_breadth': 46
    }
    
    print("👤 User: John")
    print(f"   Measurements: Chest {user_measurements['chest']}cm, "
          f"Waist {user_measurements['waist']}cm, "
          f"Shoulder {user_measurements['shoulder_breadth']}cm\n")
    
    # Get a T-Shirt category
    brands = db_manager.get_brands()
    
    if not brands:
        print("❌ No brands in database! Run add_popular_brands.py first.")
        return
    
    # Try first brand that has data
    for brand in brands:
        print(f"🏷️  Testing: {brand['brand_name']}")
        print("-" * 70)
        
        try:
            # Get T-Shirt category
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT category_id FROM garment_categories 
                    WHERE category_name = 'T-Shirt' AND gender = 'Men'
                """)
                result = cursor.fetchone()
                
                if result:
                    category_id = result['category_id']
                    
                    result = size_matching_service.find_best_size(
                        user_measurements=user_measurements,
                        brand_id=brand['brand_id'],
                        category_id=category_id,
                        fit_type='Regular'
                    )
                    
                    if 'error' not in result:
                        print(f"\n✅ RECOMMENDATION:")
                        print(f"   Size: {result['recommended_size']}")
                        print(f"   Confidence: {result['confidence']}%")
                        print(f"   Match Score: {result['match_score']}/100")
                        
                        print(f"\n📊 Alternatives:")
                        for alt in result['alternatives']:
                            print(f"   • {alt['size']} (Score: {alt['score']}) - {alt['fit_note']}")
                        
                        print(f"\n💡 Fit Advice:")
                        for advice in result['fit_advice']:
                            print(f"   {advice}")
                        
                        print(f"\n📏 Measurement Details:")
                        for detail in result['match_details']:
                            print(f"   • {detail['measurement'].title()}: "
                                  f"{detail['user_value']}cm vs {detail['size_range']} "
                                  f"(Score: {detail['score']}, Fit: {detail['fit']})")
                        
                        print()
                        break
                    else:
                        print(f"   ⏭️  No T-Shirt chart for {brand['brand_name']}\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            continue


def test_multiple_brands():
    """Test recommendations across multiple brands"""
    print("\n" + "="*70)
    print("TEST 2: Multi-Brand Comparison")
    print("="*70 + "\n")
    
    user_measurements = {
        'chest': 102,
        'waist': 88,
        'hip': 100
    }
    
    print("👤 User: Sarah")
    print(f"   Measurements: Chest {user_measurements['chest']}cm, "
          f"Waist {user_measurements['waist']}cm, "
          f"Hip {user_measurements['hip']}cm\n")
    
    # Get Women's Dress category
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category_id FROM garment_categories 
            WHERE category_name = 'Dress' AND gender = 'Women'
        """)
        result = cursor.fetchone()
        
        if not result:
            print("❌ No Women's Dress category found!")
            return
        
        category_id = result['category_id']
    
    print("🔍 Searching across all brands...\n")
    
    recommendations = size_matching_service.get_recommendations_for_multiple_brands(
        user_measurements=user_measurements,
        category_id=category_id,
        fit_type='Regular',
        min_confidence=50.0
    )
    
    if not recommendations:
        print("❌ No suitable recommendations found!")
        return
    
    print(f"✅ Found {len(recommendations)} recommendations:\n")
    print("-" * 70)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['brand_name']} - Size {rec['recommended_size']}")
        print(f"   Confidence: {rec['confidence']}% | Match: {rec['match_score']}/100")
        print(f"   📊 Alternatives: " + ", ".join([f"{a['size']} ({a['score']})" for a in rec['alternatives']]))


def test_brand_comparison():
    """Compare size across specific brands"""
    print("\n" + "="*70)
    print("TEST 3: Brand Size Comparison")
    print("="*70 + "\n")
    
    user_measurements = {
        'chest': 95,
        'waist': 80,
        'shoulder_breadth': 45
    }
    
    print("👤 User: Mike")
    print(f"   Measurements: Chest {user_measurements['chest']}cm, "
          f"Waist {user_measurements['waist']}cm, "
          f"Shoulder {user_measurements['shoulder_breadth']}cm\n")
    
    # Get Men's T-Shirt category
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category_id FROM garment_categories 
            WHERE category_name = 'T-Shirt' AND gender = 'Men'
        """)
        result = cursor.fetchone()
        
        if not result:
            print("❌ No Men's T-Shirt category found!")
            return
        
        category_id = result['category_id']
    
    # Get brand IDs to compare
    brands = db_manager.get_brands()
    brand_ids = [b['brand_id'] for b in brands[:4]]  # First 4 brands
    
    if not brand_ids:
        print("❌ Not enough brands in database!")
        return
    
    print(f"📊 Comparing across {len([b for b in brands if b['brand_id'] in brand_ids])} brands:\n")
    
    comparison = size_matching_service.compare_sizes_across_brands(
        user_measurements=user_measurements,
        category_id=category_id,
        brand_ids=brand_ids,
        fit_type='Regular'
    )
    
    if comparison['comparisons']:
        print("-" * 70)
        for comp in comparison['comparisons']:
            print(f"• {comp['brand_name']:15s}: Size {comp['recommended_size']:5s} "
                  f"(Confidence: {comp['confidence']:5.1f}%, Match: {comp['match_score']:5.1f})")
        
        print(f"\n💡 Summary: {comparison['summary']}")
    else:
        print("❌ No comparisons available!")


def test_edge_cases():
    """Test algorithm with edge cases"""
    print("\n" + "="*70)
    print("TEST 4: Edge Cases")
    print("="*70 + "\n")
    
    test_cases = [
        {
            'name': 'Very Small User',
            'measurements': {'chest': 78, 'waist': 65},
            'expected': 'Should recommend XS or smallest size'
        },
        {
            'name': 'Very Large User',
            'measurements': {'chest': 130, 'waist': 115},
            'expected': 'Should recommend XXL or largest size'
        },
        {
            'name': 'Between Sizes',
            'measurements': {'chest': 98.5, 'waist': 83.5},
            'expected': 'Should show close alternatives with similar confidence'
        }
    ]
    
    # Get first available brand and category
    brands = db_manager.get_brands()
    if not brands:
        print("❌ No brands in database!")
        return
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category_id FROM garment_categories 
            WHERE category_name = 'T-Shirt' AND gender = 'Men'
            LIMIT 1
        """)
        result = cursor.fetchone()
        
        if not result:
            print("❌ No category found!")
            return
        
        category_id = result['category_id']
    
    brand_id = brands[0]['brand_id']
    
    for test in test_cases:
        print(f"\n📋 {test['name']}")
        print(f"   Measurements: {test['measurements']}")
        print(f"   Expected: {test['expected']}")
        print("-" * 70)
        
        try:
            result = size_matching_service.find_best_size(
                user_measurements=test['measurements'],
                brand_id=brand_id,
                category_id=category_id,
                fit_type='Regular'
            )
            
            if 'error' not in result:
                print(f"   ✅ Recommended: Size {result['recommended_size']} "
                      f"(Confidence: {result['confidence']}%, Score: {result['match_score']})")
                print(f"   📊 Alternatives: " + 
                      ", ".join([f"{a['size']} ({a['score']})" for a in result['alternatives'][:2]]))
            else:
                print(f"   ⚠️  {result['error']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def main():
    """Run all tests"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*18 + "SIZE MATCHING ALGORITHM TESTS" + " "*20 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        test_single_brand()
        test_multiple_brands()
        test_brand_comparison()
        test_edge_cases()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
