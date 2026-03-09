import sys
sys.path.insert(0, './backend')

from database.db_manager import db_manager

print("Checking all available sizes in the database...")
print("=" * 80)

with db_manager.get_connection() as conn:
    cursor = conn.cursor()
    
    # Get all size charts with their sizes
    cursor.execute('''
        SELECT 
            sc.chart_id,
            b.brand_name,
            gc.category_name,
            sc.fit_type,
            COUNT(s.size_id) as size_count
        FROM size_charts sc
        JOIN brands b ON sc.brand_id = b.brand_id
        JOIN garment_categories gc ON sc.category_id = gc.category_id
        LEFT JOIN sizes s ON sc.chart_id = s.chart_id
        GROUP BY sc.chart_id
        ORDER BY b.brand_name, gc.category_name
    ''')
    
    charts = cursor.fetchall()
    
    print(f"\nTotal Size Charts: {len(charts)}\n")
    
    for chart in charts:
        print(f"\n{chart['brand_name']} - {chart['category_name']} ({chart['fit_type']})")
        print(f"  Chart ID: {chart['chart_id']}, Sizes: {chart['size_count']}")
        
        if chart['size_count'] > 0:
            # Get size details
            cursor.execute('''
                SELECT 
                    size_label,
                    size_order,
                    chest_min, chest_max,
                    waist_min, waist_max,
                    hip_min, hip_max,
                    shoulder_breadth_min, shoulder_breadth_max
                FROM sizes
                WHERE chart_id = ?
                ORDER BY size_order
            ''', (chart['chart_id'],))
            
            sizes = cursor.fetchall()
            
            print("  Sizes:")
            for size in sizes:
                print(f"    {size['size_label']} (order: {size['size_order']})")
                if size['chest_min']:
                    print(f"      Chest: {size['chest_min']}-{size['chest_max']} cm")
                if size['waist_min']:
                    print(f"      Waist: {size['waist_min']}-{size['waist_max']} cm")
                if size['hip_min']:
                    print(f"      Hip: {size['hip_min']}-{size['hip_max']} cm")
                if size['shoulder_breadth_min']:
                    print(f"      Shoulder: {size['shoulder_breadth_min']}-{size['shoulder_breadth_max']} cm")

print("\n" + "=" * 80)
print("Database check complete!")
