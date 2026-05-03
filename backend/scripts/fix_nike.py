"""Fix Nike T-Shirt chart that has no sizes"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager

# Get Nike brand
brands = db_manager.get_brands()
nike = next((b for b in brands if b['brand_name'] == 'Nike'), None)

if not nike:
    print("Nike not found")
else:
    print(f"Nike brand_id: {nike['brand_id']}")
    
    # Get T-Shirt Men category
    cat_id = db_manager.get_or_create_category("T-Shirt", "Men")
    print(f"T-Shirt Men category_id: {cat_id}")
    
    # Check size charts
    with db_manager.get_connection() as conn:
        charts = conn.execute(
            "SELECT chart_id FROM size_charts WHERE brand_id=? AND category_id=?",
            (nike['brand_id'], cat_id)
        ).fetchall()
        
        print(f"\nFound {len(charts)} charts")
        
        for chart in charts:
            chart_id = chart['chart_id']
            print(f"\nChart {chart_id}:")
            
            # Get sizes
            sizes = conn.execute(
                "SELECT * FROM sizes WHERE chart_id=?",
                (chart_id,)
            ).fetchall()
            
            print(f"  Sizes: {len(sizes)}")
            
            if len(sizes) == 0:
                print(f"  ❌ Empty chart! Deleting chart {chart_id}...")
                conn.execute("DELETE FROM size_charts WHERE chart_id=?", (chart_id,))
                conn.commit()
                print(f"  ✅ Deleted empty chart")
