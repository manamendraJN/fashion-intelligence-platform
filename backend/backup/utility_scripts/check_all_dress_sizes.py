import sqlite3
import sys
import os

# Get the database path - use the same path as backend
db_path = 'D:/Github-Projects-Research/fashion-intelligence-platform/backend/database/fashion_db.sqlite'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n" + "="*80)
print("CHECKING ALL DRESS SIZES ACROSS ALL BRANDS")
print("="*80 + "\n")

# Get all dress sizes with brand info
query = """
SELECT 
    b.brand_name,
    s.size_label,
    s.chest_min, s.chest_max,
    s.waist_min, s.waist_max,
    s.hip_min, s.hip_max,
    s.size_order
FROM sizes s
JOIN size_charts sc ON s.chart_id = sc.chart_id
JOIN brands b ON sc.brand_id = b.brand_id
JOIN garment_categories c ON sc.category_id = c.category_id
WHERE c.category_name = 'Dress'
ORDER BY b.brand_name, s.size_order
"""

cursor.execute(query)
results = cursor.fetchall()

if results:
    print(f"Found {len(results)} dress sizes across all brands:\n")
    
    current_brand = None
    for row in results:
        brand, size, chest_min, chest_max, waist_min, waist_max, hip_min, hip_max, order = row
        
        if brand != current_brand:
            print(f"\n{brand}:")
            print("-" * 60)
            current_brand = brand
        
        print(f"  {size:4s} | Chest: {chest_min:5.1f}-{chest_max:5.1f} | "
              f"Waist: {waist_min:5.1f}-{waist_max:5.1f} | Hip: {hip_min:5.1f}-{hip_max:5.1f}")
    
    # Find maximum sizes
    print("\n" + "="*80)
    print("MAXIMUM SIZES AVAILABLE:")
    print("="*80)
    max_chest = max(row[3] for row in results)
    max_waist = max(row[5] for row in results) 
    max_hip = max(row[7] for row in results)
    print(f"Max Chest: {max_chest:.1f} cm")
    print(f"Max Waist: {max_waist:.1f} cm")
    print(f"Max Hip: {max_hip:.1f} cm")
    
    print("\n" + "="*80)
    print("USER'S MEASUREMENTS:")
    print("="*80)
    print(f"Chest: 134.46 cm (Exceeds max by {134.46 - max_chest:.1f} cm)")
    print(f"Waist: 123.46 cm (Exceeds max by {123.46 - max_waist:.1f} cm)")
    print(f"Hip: 145.46 cm (Exceeds max by {145.46 - max_hip:.1f} cm)")
else:
    print("No dress sizes found in database!")

conn.close()
