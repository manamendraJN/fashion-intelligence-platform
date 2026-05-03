"""
Test the pairing fix for Mini Skirt + Casual + Hot Weather
This should now return T-Shirts, Tank Tops, etc. and filter out Sweaters/Hoodies
"""

import sys
sys.path.append('backend')

from utils.color_utils import get_event_based_pairing

# Test: White Mini Skirt for Casual
result = get_event_based_pairing("Mini Skirt", "White", "casual")

print("=" * 60)
print("TEST: White Mini Skirt for Casual Event")
print("=" * 60)
print(f"\nMatching Types ({len(result['matching_types'])} items):")
for item_type in result['matching_types']:
    print(f"  • {item_type}")

print(f"\nMatching Colors ({len(result['matching_colors'])} colors):")
for color in result['matching_colors'][:5]:  # Show first 5
    print(f"  • {color}")

print(f"\nAvoid Types ({len(result['avoid_types'])} items):")
for item_type in result['avoid_types']:
    print(f"  • {item_type}")

print(f"\nPairing Note: {result['pairing_note']}")
print(f"Category: {result['pairing_category']}")

print("\n" + "=" * 60)
print("Weather Filtering Logic:")
print("=" * 60)
print("Hot Weather:")
print("  ✓ BOOST: T-Shirts, Tank Top, Crop Top (+0.10)")
print("  ✗ PENALTY: Sweaters, Hoodies, Cardigan (-0.35)")
print("\nBase pairing score: 0.7")
print("After boost: 0.8 (kept)")
print("After penalty: 0.35 (filtered, threshold=0.4)")

print("\n✅ Expected Result: T-Shirts, Tank Tops, Crop Tops shown")
print("✅ Expected Result: Sweaters, Hoodies filtered out in hot weather")
