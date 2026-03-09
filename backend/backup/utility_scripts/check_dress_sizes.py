import sys
sys.path.insert(0, './backend')

from database.db_manager import db_manager

print("Checking Dress sizes (category_id = 7)...")
print("=" * 60)

with db_manager.get_connection() as conn:
    cursor = conn.cursor()

    # Get dress sizes
    cursor.execute('''
        SELECT 
            b.brand_name,
            s.size_label, 
            s.chest_min, s.chest_max, 
            s.waist_min, s.waist_max, 
            s.hip_min, s.hip_max
        FROM sizes s 
        JOIN size_charts sc ON s.chart_id = sc.chart_id
        JOIN brands b ON sc.brand_id = b.brand_id
        WHERE sc.category_id = 7
        ORDER BY b.brand_name, s.size_order
    ''')

    rows = cursor.fetchall()

    if rows:
        print(f"Found {len(rows)} dress sizes:")
        print()
        for row in rows:
            print(f"{row['brand_name']} - Size {row['size_label']}:")
            print(f"  Chest: {row['chest_min']}-{row['chest_max']} cm")
            print(f"  Waist: {row['waist_min']}-{row['waist_max']} cm")
            print(f"  Hip: {row['hip_min']}-{row['hip_max']} cm")
            print()
    else:
        print("No dress sizes found!")
