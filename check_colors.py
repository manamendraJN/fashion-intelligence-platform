"""
Check if existing database items have color information
"""

import sys
sys.path.append('backend')
import database

items = database.get_all_wardrobe_items()

print("=" * 60)
print(f"CHECKING COLOR DATA IN DATABASE ({len(items)} items)")
print("=" * 60)

# Count items with/without colors
items_with_color = 0
items_without_color = 0

print("\nSample of first 10 items:\n")
for i, item in enumerate(items[:10], 1):
    has_color = item.get('primaryColor') is not None
    color_display = item.get('primaryColor', 'NO COLOR')
    
    if has_color:
        items_with_color += 1
        status = "✓"
    else:
        items_without_color += 1
        status = "✗"
    
    print(f"{status} ID {item['id']:3d}: {item['type']:20s} | Color: {color_display}")

# Count all items
for item in items[10:]:
    if item.get('primaryColor') is not None:
        items_with_color += 1
    else:
        items_without_color += 1

print("\n" + "=" * 60)
print(f"SUMMARY:")
print(f"  Items WITH color:    {items_with_color} ({items_with_color/len(items)*100:.1f}%)")
print(f"  Items WITHOUT color: {items_without_color} ({items_without_color/len(items)*100:.1f}%)")
print("=" * 60)

if items_without_color > 0:
    print("\n⚠️  OLD ITEMS DON'T HAVE COLORS")
    print("   Solution: Re-upload or re-analyze them to extract colors")
else:
    print("\n✅ All items have color data!")
