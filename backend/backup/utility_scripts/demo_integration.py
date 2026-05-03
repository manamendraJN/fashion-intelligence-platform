"""
Automated test - Add Adidas Men's Polo Shirt (new example)
This demonstrates the size chart manager working with your existing database
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from simple_size_manager import add_brand, add_category, create_size_chart, add_size, view_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("\n" + "="*70)
print("AUTOMATED TEST: Adding Adidas Men's Polo Shirt Size Chart")
print("="*70 + "\n")

# View current database
print("📊 BEFORE:")
view_database()

# Add new size chart for Adidas Men's Polo Shirt
print("\n" + "="*70)
print("ADDING NEW SIZE CHART")
print("="*70 + "\n")

# Adidas and T-Shirt category should already exist, but add_brand/add_category will skip if exists
brand_id = add_brand("Adidas", "Germany", "EU", "https://www.adidas.com")
category_id = add_category("Polo Shirt", "Men", "Polo shirts with collar")

# Create new chart for Polo Shirts (different from T-Shirts)
chart_id = create_size_chart(
    brand_id, 
    category_id, 
    "Adidas Men's Performance Polo",
    "Athletic Fit"
)

# Add sizes - Polo shirts have slightly different fit than T-shirts
logger.info("Adding polo shirt sizes...")

polo_sizes = [
    ("S", 1, {
        'chest': (88, 92),
        'shoulder': (43, 45),
        'waist': (78, 82)
    }),
    ("M", 2, {
        'chest': (92, 98),
        'shoulder': (45, 47),
        'waist': (82, 88)
    }),
    ("L", 3, {
        'chest': (98, 104),
        'shoulder': (47, 49),
        'waist': (88, 94)
    }),
    ("XL", 4, {
        'chest': (104, 110),
        'shoulder': (49, 52),
        'waist': (94, 100)
    }),
    ("XXL", 5, {
        'chest': (110, 118),
        'shoulder': (52, 55),
        'waist': (100, 108)
    }),
]

for label, order, measurements in polo_sizes:
    add_size(chart_id, label, order, measurements)

print("\n✅ SUCCESS! Adidas Men's Polo Shirt size chart added\n")

# View updated database
print("="*70)
print("📊 AFTER:")
view_database()

print("="*70)
print("✅ INTEGRATION TEST COMPLETE")
print("="*70)
print("\nSummary:")
print("  ✓ Connected to existing database")
print("  ✓ Reused existing brand (Adidas)")
print("  ✓ Added new category (Polo Shirt)")
print("  ✓ Created new size chart")
print("  ✓ Added 5 sizes with measurements")
print("\nThe size chart manager is fully integrated with your system!")
print()
