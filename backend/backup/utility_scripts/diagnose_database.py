"""
Diagnostic script to check current database state
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager

def diagnose_database():
    db = DatabaseManager()
    
    print("="*60)
    print("DATABASE DIAGNOSTIC REPORT")
    print("="*60)
    
    # Check if tables exist
    print("\n1. CHECKING TABLE EXISTENCE:")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)
        tables = [dict(row) for row in cursor.fetchall()]
    print(f"   Tables found: {len(tables)}")
    for table in tables:
        print(f"   - {table['name']}")
    
    # Check brands
    print("\n2. CHECKING BRANDS:")
    brands = db.get_brands()
    print(f"   Total brands: {len(brands)}")
    for brand in brands[:10]:  # Show first 10
        print(f"   - {brand['brand_name']} (ID: {brand['brand_id']})")
    
    # Check categories
    print("\n3. CHECKING GARMENT CATEGORIES:")
    categories = db.get_categories()
    print(f"   Total categories: {len(categories)}")
    for cat in categories:
        print(f"   - {cat['category_name']} ({cat['gender']}) (ID: {cat['category_id']})")
    
    # Check size charts
    print("\n4. CHECKING SIZE CHARTS:")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sc.chart_id, b.brand_name, gc.category_name, sc.fit_type
            FROM size_charts sc
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            ORDER BY b.brand_name, gc.category_name
        """)
        charts = [dict(row) for row in cursor.fetchall()]
    print(f"   Total size charts: {len(charts)}")
    for chart in charts[:20]:  # Show first 20
        print(f"   - {chart['brand_name']} × {chart['category_name']} ({chart['fit_type']})")
    
    # Check sizes
    print("\n5. CHECKING SIZES:")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM sizes")
        sizes_count = dict(cursor.fetchone())
    print(f"   Total sizes: {sizes_count['count']}")
    
    # Sample sizes from each chart
    print("\n6. SAMPLE SIZES FROM EACH CHART:")
    for chart in charts[:10]:  # Show first 10 charts
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT size_label FROM sizes 
                WHERE chart_id = ? 
                ORDER BY size_order
            """, (chart['chart_id'],))
            sizes = [dict(row) for row in cursor.fetchall()]
        size_labels = [s['size_label'] for s in sizes]
        print(f"   {chart['brand_name']} {chart['category_name']}: {', '.join(size_labels)}")
    
    # Check measurements
    print("\n7. CHECKING MEASUREMENTS (denormalized in sizes table):")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM sizes
            WHERE chest_min IS NOT NULL OR waist_min IS NOT NULL OR hip_min IS NOT NULL
        """)
        measurements_count = dict(cursor.fetchone())
    print(f"   Sizes with measurements: {measurements_count['count']}")
    
    # Check for size "24" specifically
    print("\n8. SEARCHING FOR SIZE '24':")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.size_label, b.brand_name, gc.category_name, sc.fit_type
            FROM sizes s
            JOIN size_charts sc ON s.chart_id = sc.chart_id
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            WHERE s.size_label = '24'
        """)
        size_24 = [dict(row) for row in cursor.fetchall()]
    if size_24:
        print(f"   Found {len(size_24)} occurrences of size '24':")
        for s in size_24:
            print(f"   - {s['brand_name']} {s['category_name']} ({s['fit_type']})")
    else:
        print("   Size '24' not found in database")
    
    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    diagnose_database()
