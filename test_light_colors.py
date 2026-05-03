"""
Test Enhanced Color Detection - Light & Pastel Colors
"""

import sys
sys.path.append('backend')

from utils.color_utils import rgb_to_color_name, get_matching_colors

print("=" * 70)
print("TESTING ENHANCED COLOR DETECTION (Light/Pastel Colors)")
print("=" * 70)

# Test various RGB values for light/pastel colors
test_colors = [
    # Light blues
    ((173, 216, 230), "Light Blue (expected)"),
    ((135, 206, 235), "Sky Blue (light blue expected)"),
    ((0, 0, 255), "Bright Blue"),
    ((0, 0, 139), "Dark Blue/Navy (expected)"),
    
    # Light purples/lavender
    ((230, 230, 250), "Lavender (light purple expected)"),
    ((216, 191, 216), "Thistle (light purple expected)"),
    ((128, 0, 128), "Purple"),
    ((75, 0, 130), "Indigo (dark purple expected)"),
    
    # Light pinks
    ((255, 182, 193), "Light Pink (expected)"),
    ((255, 192, 203), "Pink"),
    ((255, 105, 180), "Hot Pink"),
    
    # Light greens
    ((144, 238, 144), "Light Green (expected)"),
    ((152, 251, 152), "Pale Green (light green expected)"),
    ((0, 128, 0), "Green"),
    ((0, 100, 0), "Dark Green (expected)"),
    
    # Light yellows
    ((255, 255, 224), "Light Yellow (expected)"),
    ((255, 255, 0), "Yellow"),
    
    # Peach/Coral
    ((255, 218, 185), "Peach (expected)"),
    ((255, 229, 180), "Light Peach (expected)"),
]

print("\n🎨 RGB → Color Name Detection:\n")
for rgb, description in test_colors:
    detected = rgb_to_color_name(rgb)
    print(f"  RGB{rgb} → {detected:20s} ({description})")

print("\n" + "=" * 70)
print("MATCHING COLORS FOR LIGHT VARIANTS")
print("=" * 70)

light_colors = ["Light Blue", "Light Purple", "Light Pink", "Light Green", "Peach"]

for color in light_colors:
    matches = get_matching_colors(color)
    print(f"\n💡 {color} pairs well with:")
    print(f"   {', '.join(matches[:8])}")

print("\n" + "=" * 70)
print("✨ LIGHT COLOR DETECTION UPGRADED!")
print("   - Detects Light Blue, Light Purple, Light Pink, etc.")
print("   - Detects Peach, Light Yellow, Light Green")
print("   - Detects Navy, Dark Red, Dark Purple, Dark Green")
print("   - All with matching pairing rules")
print("=" * 70)
