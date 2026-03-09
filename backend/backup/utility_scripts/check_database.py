"""Check current database contents"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager

print("\n=== BRANDS IN DATABASE ===")
brands = db_manager.get_brands()
for brand in brands:
    print(f"  ID {brand['brand_id']}: {brand['brand_name']} ({brand['size_system']})")
print(f"Total: {len(brands)} brands\n")

print("=== CATEGORIES IN DATABASE ===")
categories = db_manager.get_categories()
for cat in categories:
    print(f"  ID {cat['category_id']}: {cat['category_name']} ({cat['gender']})")
print(f"Total: {len(categories)} categories\n")

print("=== SIZE CHARTS IN DATABASE ===")
with db_manager.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sc.chart_id, b.brand_name, gc.category_name, gc.gender, sc.fit_type
        FROM size_charts sc
        JOIN brands b ON sc.brand_id = b.brand_id
        JOIN garment_categories gc ON sc.category_id = gc.category_id
        ORDER BY b.brand_name, gc.category_name
    """)
    charts = cursor.fetchall()
    for chart in charts:
        print(f"  Chart ID {chart[0]}: {chart[1]} - {chart[2]} ({chart[3]}) - {chart[4]}")
    print(f"Total: {len(charts)} size charts\n")
