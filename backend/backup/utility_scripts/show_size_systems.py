"""
Display sizing systems by category to help users understand what size format to expect
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager

def show_size_systems():
    db = DatabaseManager()
    
    print("\n" + "="*70)
    print("SIZE SYSTEMS BY GARMENT CATEGORY")
    print("="*70)
    
    categories = db.get_categories()
    
    for cat in categories:
        cat_id = cat['category_id']
        cat_name = cat['category_name']
        gender = cat['gender']
        
        print(f"\n📦 {cat_name} ({gender})")
        print("─" * 70)
        
        # Get all charts for this category
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sc.chart_id, b.brand_name
                FROM size_charts sc
                JOIN brands b ON sc.brand_id = b.brand_id
                WHERE sc.category_id = ?
                LIMIT 3
            """, (cat_id,))
            charts = [dict(row) for row in cursor.fetchall()]
        
        if not charts:
            print("   ⚠️  No size charts available")
            continue
        
        # Get sizes from first chart as example
        chart = charts[0]
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT size_label FROM sizes
                WHERE chart_id = ?
                ORDER BY size_order
            """, (chart['chart_id'],))
            sizes = [dict(row) for row in cursor.fetchall()]
        
        size_labels = [s['size_label'] for s in sizes]
        
        # Determine size system type
        first_size = size_labels[0] if size_labels else ""
        if first_size.isdigit():
            size_type = "🔢 NUMERIC (Waist in inches)"
        else:
            size_type = "📏 LETTER SIZES"
        
        print(f"   Size System: {size_type}")
        print(f"   Available Sizes: {', '.join(size_labels)}")
        print(f"   Example Brand: {chart['brand_name']}")
        
        # Show which brands have this category
        brand_names = [c['brand_name'] for c in charts]
        if len(charts) < 3:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(DISTINCT sc.brand_id) as count
                    FROM size_charts sc
                    WHERE sc.category_id = ?
                """, (cat_id,))
                total = dict(cursor.fetchone())['count']
            print(f"   Brands with data: {', '.join(brand_names)} ({total} total)")
        else:
            print(f"   Brands with data: {', '.join(brand_names)} (and more)")
    
    print("\n" + "="*70)
    print("💡 TIP:")
    print("   - For S/M/L/XL sizing → Select T-Shirt, Dress, or Jacket")
    print("   - For numeric sizing (24, 28, 32) → Select Jeans or Pants")
    print("="*70 + "\n")

if __name__ == "__main__":
    show_size_systems()
