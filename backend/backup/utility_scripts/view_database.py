"""
Quick database viewer script
Shows all data in the fashion size matching database
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import db_manager
import json


def view_database():
    """Display all database contents in a readable format"""
    
    print("\n" + "="*80)
    print("FASHION SIZE MATCHING DATABASE VIEWER")
    print("="*80)
    
    # Brands
    print("\n📦 BRANDS")
    print("-" * 80)
    brands = db_manager.get_brands()
    for brand in brands:
        print(f"ID: {brand['brand_id']} | {brand['brand_name']} ({brand['brand_country']}) | System: {brand['size_system']}")
        if brand['website_url']:
            print(f"   Website: {brand['website_url']}")
    
    # Categories
    print("\n👕 GARMENT CATEGORIES")
    print("-" * 80)
    categories = db_manager.get_categories()
    for cat in categories:
        print(f"ID: {cat['category_id']} | {cat['category_name']} ({cat['gender']})")
        if cat['description']:
            print(f"   {cat['description']}")
    
    # Size Charts
    print("\n📊 SIZE CHARTS")
    print("-" * 80)
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sc.chart_id, b.brand_name, gc.category_name, gc.gender,
                   sc.chart_name, sc.fit_type, 
                   COUNT(s.size_id) as num_sizes
            FROM size_charts sc
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            LEFT JOIN sizes s ON sc.chart_id = s.chart_id
            GROUP BY sc.chart_id
            ORDER BY b.brand_name, gc.category_name
        """)
        charts = cursor.fetchall()
        
        for chart in charts:
            chart_id, brand, category, gender, chart_name, fit_type, num_sizes = chart
            print(f"Chart ID: {chart_id}")
            print(f"  Brand: {brand} | Category: {category} ({gender})")
            print(f"  Fit Type: {fit_type or 'Regular'} | Sizes: {num_sizes}")
            
            # Get sizes for this chart
            cursor.execute("""
                SELECT size_label, size_order 
                FROM sizes 
                WHERE chart_id = ?
                ORDER BY size_order
            """, (chart_id,))
            sizes = cursor.fetchall()
            size_labels = [s[0] for s in sizes]
            print(f"  Available Sizes: {', '.join(size_labels)}")
            print()
    
    # Detailed view of one size chart
    print("\n🔍 DETAILED EXAMPLE: Nike Men's T-Shirt")
    print("-" * 80)
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sc.chart_id 
            FROM size_charts sc
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            WHERE b.brand_name = 'Nike' 
            AND gc.category_name = 'T-Shirt' 
            AND gc.gender = 'Men'
            LIMIT 1
        """)
        result = cursor.fetchone()
        
        if result:
            chart_id = result[0]
            sizes_data = db_manager.get_sizes_for_chart(chart_id)
            
            print("\nSize | Measurements")
            print("-" * 80)
            for size in sizes_data:
                print(f"\n{size['size_label']}:")
                for meas in size['measurements']:
                    mtype = meas['type']
                    min_val = meas['min']
                    max_val = meas['max']
                    optimal = meas['optimal']
                    print(f"  {mtype:20s}: {min_val:5.1f} - {max_val:5.1f} cm (optimal: {optimal:.1f})")
    
    # Summary statistics
    print("\n📈 STATISTICS")
    print("-" * 80)
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM brands")
        print(f"Total Brands: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM garment_categories")
        print(f"Total Categories: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM size_charts")
        print(f"Total Size Charts: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM sizes")
        print(f"Total Sizes: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM size_measurements")
        print(f"Total Measurements: {cursor.fetchone()[0]}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    view_database()
