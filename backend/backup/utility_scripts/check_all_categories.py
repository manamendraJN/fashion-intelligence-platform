import sqlite3

db_path = 'D:/Github-Projects-Research/fashion-intelligence-platform/backend/database/fashion_db.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n" + "="*80)
print("CHECKING ALL CATEGORIES - USER MEASUREMENTS VS AVAILABLE")
print("="*80)
print(f"\nUser Measurements: Chest=134.46, Waist=123.46, Hip=145.46\n")

# Get all categories with size data
query = """
SELECT DISTINCT
    c.category_name,
    c.category_id,
    COUNT(DISTINCT b.brand_id) as brand_count,
    COUNT(s.size_id) as size_count,
    MAX(s.chest_max) as max_chest,
    MAX(s.waist_max) as max_waist,
    MAX(s.hip_max) as max_hip
FROM garment_categories c
JOIN size_charts sc ON c.category_id = sc.category_id
JOIN sizes s ON sc.chart_id = s.chart_id
JOIN brands b ON sc.brand_id = b.brand_id
WHERE s.chest_max IS NOT NULL OR s.waist_max IS NOT NULL
GROUP BY c.category_name, c.category_id
ORDER BY c.category_name
"""

cursor.execute(query)
results = cursor.fetchall()

for row in results:
    cat_name, cat_id, brand_count, size_count, max_chest, max_waist, max_hip = row
    
    print(f"{cat_name}")
    print("-" * 60)
    print(f"  Brands: {brand_count} | Sizes: {size_count}")
    
    if max_chest:
        print(f"  Max Chest: {max_chest:.1f} cm", end="")
        if max_chest < 134.46:
            print(f" ❌ (Need {134.46 - max_chest:.1f} cm more)")
        else:
            print(" ✅")
    
    if max_waist:
        print(f"  Max Waist: {max_waist:.1f} cm", end="")
        if max_waist < 123.46:
            print(f" ❌ (Need {123.46 - max_waist:.1f} cm more)")
        else:
            print(" ✅")
    
    if max_hip:
        print(f"  Max Hip: {max_hip:.1f} cm", end="")
        if max_hip < 145.46:
            print(f" ❌ (Need {145.46 - max_hip:.1f} cm more)")
        else:
            print(" ✅")
    print()

conn.close()
