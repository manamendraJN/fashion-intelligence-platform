"""
Test to demonstrate different sizing systems for different garment types
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.size_matching_service import SizeMatchingService
from database.db_manager import DatabaseManager

def test_sizing_systems():
    service = SizeMatchingService()
    db = DatabaseManager()
    
    # Example user measurements
    user_measurements = {
        'chest': 90,        # 90 cm
        'waist': 68,        # 68 cm (approx. 26-27 inches)
        'hip': 95,          # 95 cm
        'shoulder_breadth': 40,
        'height': 170,
        'leg_length': 78
    }
    
    print("\n" + "="*70)
    print("SIZING SYSTEM COMPARISON TEST")
    print("="*70)
    print("\nUser Measurements:")
    print(f"  Chest: {user_measurements['chest']} cm")
    print(f"  Waist: {user_measurements['waist']} cm")
    print(f"  Hip: {user_measurements['hip']} cm")
    print(f"  Shoulder: {user_measurements['shoulder_breadth']} cm")
    print(f"  Height: {user_measurements['height']} cm")
    print(f"  Leg Length: {user_measurements['leg_length']} cm")
    
    print("\n" + "="*70)
    print("TESTING WITH DIFFERENT GARMENT CATEGORIES")
    print("="*70)
    
    # Get category IDs
    categories = db.get_categories()
    tshirt_men = next((c for c in categories if c['category_name'] == 'T-Shirt' and c['gender'] == 'Men'), None)
    tshirt_women = next((c for c in categories if c['category_name'] == 'T-Shirt' and c['gender'] == 'Women'), None)
    jeans_women = next((c for c in categories if c['category_name'] == 'Jeans' and c['gender'] == 'Women'), None)
    
    brands = db.get_brands()
    nike = next((b for b in brands if b['brand_name'] == 'Nike'), None)
    zara = next((b for b in brands if b['brand_name'] == 'Zara'), None)
    
    # Test 1: T-Shirt (Women) - Should give letter size
    print("\n1️⃣  WOMEN'S T-SHIRT (Zara)")
    print("─" * 70)
    if tshirt_women and zara:
        result = service.find_best_size(
            user_measurements=user_measurements,
            brand_id=zara['brand_id'],
            category_id=tshirt_women['category_id'],
            fit_type='Regular'
        )
        if 'error' not in result:
            print(f"   ✅ Recommended Size: {result['recommended_size']}")
            print(f"   📊 Confidence: {result['confidence']}%")
            print(f"   📏 Size System: LETTER SIZE (XS/S/M/L/XL)")
        else:
            print(f"   ❌ Error: {result['error']}")
    
    # Test 2: Women's Jeans - Should give numeric size
    print("\n2️⃣  WOMEN'S JEANS (Zara)")
    print("─" * 70)
    if jeans_women and zara:
        result = service.find_best_size(
            user_measurements=user_measurements,
            brand_id=zara['brand_id'],
            category_id=jeans_women['category_id'],
            fit_type='Regular'
        )
        if 'error' not in result:
            print(f"   ✅ Recommended Size: {result['recommended_size']}")
            print(f"   📊 Confidence: {result['confidence']}%")
            print(f"   🔢 Size System: NUMERIC (waist in inches)")
            waist_cm = user_measurements['waist']
            waist_inches = waist_cm / 2.54
            print(f"   📐 Your waist: {waist_cm}cm ≈ {waist_inches:.1f} inches")
        else:
            print(f"   ❌ Error: {result['error']}")
    
    # Test 3: Men's T-Shirt - Should give letter size
    print("\n3️⃣  MEN'S T-SHIRT (Nike)")
    print("─" * 70)
    if tshirt_men and nike:
        result = service.find_best_size(
            user_measurements=user_measurements,
            brand_id=nike['brand_id'],
            category_id=tshirt_men['category_id'],
            fit_type='Regular'
        )
        if 'error' not in result:
            print(f"   ✅ Recommended Size: {result['recommended_size']}")
            print(f"   📊 Confidence: {result['confidence']}%")
            print(f"   📏 Size System: LETTER SIZE (XS/S/M/L/XL)")
        else:
            print(f"   ❌ Error: {result['error']}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
The same measurements produce DIFFERENT SIZE FORMATS based on category:

✅ T-Shirts, Dresses, Jackets → Letter Sizes (S, M, L, XL)
✅ Jeans, Pants, Trousers → Numeric Sizes (24, 26, 28, 30, 32)

💡 This is CORRECT behavior - different garment types use different
   sizing conventions in the real world!

🎯 To get S/M/L/XL sizes:
   → Select "T-Shirt", "Dress", or other tops/outerwear categories
   
🎯 To get numeric sizes (24, 28, 32):
   → Select "Jeans" or "Pants" categories (these use waist measurements)
""")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_sizing_systems()
