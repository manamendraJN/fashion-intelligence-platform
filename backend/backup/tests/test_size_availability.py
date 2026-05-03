"""
Test Size Recommendation API with Populated Data
Verify that the "Size chart not found" error is fixed
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
import json

print("\n" + "="*70)
print("TESTING SIZE RECOMMENDATION API")
print("="*70 + "\n")

# Test sample user measurements
sample_measurements = {
    'chest': 95,
    'waist': 82,
    'hip': 98,
    'shoulder_breadth': 45,
    'height': 175
}

print("Sample User Measurements:")
print(json.dumps(sample_measurements, indent=2))
print()

# Test all brand/category combinations
test_cases = [
    ("Nike", "T-Shirt", "Men"),
    ("Nike", "Jeans", "Men"),
    ("Nike", "T-Shirt", "Women"),
    ("Adidas", "T-Shirt", "Men"),
    ("Adidas", "Jeans", "Men"),
    ("Adidas", "T-Shirt", "Women"),
    ("Zara", "T-Shirt", "Men"),
    ("Zara", "Jeans", "Men"),
    ("Zara", "T-Shirt", "Women"),
    ("Zara", "Jeans", "Women"),
    ("H&M", "T-Shirt", "Men"),
    ("H&M", "Jeans", "Men"),
    ("H&M", "Jeans", "Women"),
    ("H&M", "Dress", "Women"),
    ("Levi's", "T-Shirt", "Men"),
    ("Levi's", "Jeans", "Women"),
    ("Uniqlo", "T-Shirt", "Men"),
    ("Uniqlo", "Jeans", "Men"),
    ("Uniqlo", "T-Shirt", "Women"),
    ("Uniqlo", "Jeans", "Women"),
]

print("=" * 70)
print("TESTING SIZE CHART AVAILABILITY")
print("=" * 70)
print()

success_count = 0
fail_count = 0

for brand_name, category_name, gender in test_cases:
    # Get brand ID
    brands = db_manager.get_brands()
    brand = next((b for b in brands if b['brand_name'] == brand_name), None)
    
    # Get category ID
    categories = db_manager.get_categories()
    category = next((c for c in categories if c['category_name'] == category_name and c['gender'] == gender), None)
    
    if not brand or not category:
        print(f"❌ {brand_name} - {category_name} ({gender}): Brand or category not found")
        fail_count += 1
        continue
    
    # Try to get size chart
    chart = db_manager.get_size_chart(brand['brand_id'], category['category_id'], 'Regular')
    
    if chart:
        sizes = db_manager.get_sizes_for_chart(chart['chart_id'])
        print(f"✅ {brand_name:12} - {category_name:10} ({gender:6}): {len(sizes)} sizes available")
        success_count += 1
    else:
        print(f"❌ {brand_name:12} - {category_name:10} ({gender:6}): SIZE CHART NOT FOUND")
        fail_count += 1

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✅ Success: {success_count}/{len(test_cases)}")
print(f"❌ Failed:  {fail_count}/{len(test_cases)}")

if fail_count == 0:
    print("\n🎉 ALL SIZE CHARTS AVAILABLE!")
    print("The 'Size chart not found' error should now be fixed.")
else:
    print(f"\n⚠️  {fail_count} combinations still missing size charts.")

print()
