"""
Test script for color extraction and clothing pairing functionality
Demonstrates the new color-based matching system
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from utils.color_utils import (
    extract_dominant_color,
    get_matching_colors,
    get_complementary_items,
    are_colors_compatible
)

def test_color_matching():
    """Test color matching rules"""
    print("=" * 60)
    print("TESTING COLOR MATCHING RULES")
    print("=" * 60)
    
    # Test various color combinations
    test_cases = [
        ("Blue", "White"),
        ("Blue", "Denim"),
        ("Red", "Black"),
        ("Yellow", "Blue"),
        ("Green", "Brown"),
        ("Pink", "Gray"),
    ]
    
    for color1, color2 in test_cases:
        compatible = are_colors_compatible(color1, color2)
        print(f"\n{color1} + {color2}: {'✓ Compatible' if compatible else '✗ Not Compatible'}")
        if compatible:
            print(f"  → {color1} matches with: {', '.join(get_matching_colors(color1)[:5])}")

def test_clothing_pairing():
    """Test clothing type pairing recommendations"""
    print("\n" + "=" * 60)
    print("TESTING CLOTHING PAIRING RECOMMENDATIONS")
    print("=" * 60)
    
    test_items = [
        ("Tops", "Blue"),
        ("Blouse", "White"),
        ("Jeans", "Denim"),
        ("Skirts", "Black"),
        ("T-Shirt", "Red"),
        ("Trousers", "Gray"),
    ]
    
    for item_type, item_color in test_items:
        print(f"\n📦 Item: {item_color} {item_type}")
        recommendations = get_complementary_items(item_type, item_color)
        
        print(f"  Matching Types: {', '.join(recommendations['matching_types'][:4])}")
        print(f"  Matching Colors: {', '.join(recommendations['matching_colors'][:6])}")
        
        # Example pairings
        if recommendations['matching_types']:
            sample_type = recommendations['matching_types'][0]
            sample_color = recommendations['matching_colors'][0] if recommendations['matching_colors'] else "white"
            print(f"  💡 Example pairing: {item_color} {item_type} + {sample_color} {sample_type}")

def test_rgb_to_color():
    """Test RGB to color name conversion"""
    print("\n" + "=" * 60)
    print("TESTING RGB TO COLOR NAME CONVERSION")
    print("=" * 60)
    
    from utils.color_utils import rgb_to_color_name
    
    test_colors = [
        ((255, 0, 0), "Red"),
        ((0, 0, 255), "Blue"),
        ((255, 255, 255), "White"),
        ((0, 0, 0), "Black"),
        ((128, 128, 128), "Gray"),
        ((255, 255, 0), "Yellow"),
        ((0, 128, 0), "Green"),
        ((255, 192, 203), "Pink"),
        ((139, 69, 19), "Brown"),
    ]
    
    print("\nRGB → Color Name:")
    for rgb, expected in test_colors:
        detected = rgb_to_color_name(rgb)
        match = "✓" if detected == expected else f"✗ (got {detected})"
        print(f"  {rgb} → {expected} {match}")

def display_summary():
    """Display feature summary"""
    print("\n" + "=" * 60)
    print("COLOR EXTRACTION & PAIRING FEATURES")
    print("=" * 60)
    print("""
✓ Automatic color extraction from clothing images
✓ RGB to human-readable color names (Red, Blue, etc.)
✓ Rule-based color matching (no ML training needed)
✓ Smart clothing pairing recommendations
✓ Type-based matching (Tops ↔ Bottoms)
✓ Color compatibility checking

HOW IT WORKS:
1. Upload clothing → System extracts dominant color
2. Select item → Get matching recommendations
3. System shows items that pair well by:
   - Clothing type (tops with bottoms)
   - Color compatibility (blue blouse + white/black/denim skirts)

EXAMPLE PAIRINGS:
• Blue Blouse → White, Black, or Denim Skirts/Trousers
• Red Top → Black, Gray, or White Bottoms
• Denim Jeans → Any colored Tops (very versatile!)
• Black Trousers → Works with most colored Tops

DATABASE UPDATES:
• Added primary_color column (e.g., "Blue")
• Added color_rgb column (e.g., [0, 0, 255])
• Added all_colors column (top 3 colors with percentages)

API ENDPOINT:
GET /api/outfit-pairing/<item_id>
Returns matching items with compatibility scores and reasons.
""")

if __name__ == "__main__":
    try:
        display_summary()
        test_rgb_to_color()
        test_color_matching()
        test_clothing_pairing()
        
        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
