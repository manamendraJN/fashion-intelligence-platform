"""
SIZE CHART MANAGER - Works with Existing 5-Table Database
Easy script to add size charts to your Fashion Intelligence Platform
Integrates with your current database structure
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_brand(name, country="USA", size_system="US", website=""):
    """Add a brand to the BRANDS table"""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        # Check if exists
        cursor.execute("SELECT brand_id FROM brands WHERE brand_name = ?", (name,))
        result = cursor.fetchone()
        if result:
            logger.info(f"✓ Brand '{name}' already exists (ID: {result[0]})")
            return result[0]
        
        # Insert new
        cursor.execute("""
            INSERT INTO brands (brand_name, brand_country, size_system, website_url)
            VALUES (?, ?, ?, ?)
        """, (name, country, size_system, website))
        brand_id = cursor.lastrowid
        logger.info(f"✓ Added brand '{name}' (ID: {brand_id})")
        return brand_id


def add_category(name, gender="Men", description=""):
    """Add a garment category to the GARMENT_CATEGORIES table"""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        # Check if exists
        cursor.execute("""
            SELECT category_id FROM garment_categories 
            WHERE category_name = ? AND gender = ?
        """, (name, gender))
        result = cursor.fetchone()
        if result:
            logger.info(f"✓ Category '{name} {gender}' already exists (ID: {result[0]})")
            return result[0]
        
        # Insert new
        cursor.execute("""
            INSERT INTO garment_categories (category_name, gender, description)
            VALUES (?, ?, ?)
        """, (name, gender, description))
        category_id = cursor.lastrowid
        logger.info(f"✓ Added category '{name} {gender}' (ID: {category_id})")
        return category_id


def create_size_chart(brand_id, category_id, chart_name="", fit_type="Regular"):
    """Create a size chart (link brand + category) in SIZE_CHARTS table"""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        # Check if exists
        cursor.execute("""
            SELECT chart_id FROM size_charts 
            WHERE brand_id = ? AND category_id = ? AND fit_type = ?
        """, (brand_id, category_id, fit_type))
        result = cursor.fetchone()
        if result:
            logger.warning(f"⚠️  Size chart already exists (ID: {result[0]})")
            return result[0]
        
        # Insert new
        cursor.execute("""
            INSERT INTO size_charts (brand_id, category_id, chart_name, fit_type)
            VALUES (?, ?, ?, ?)
        """, (brand_id, category_id, chart_name, fit_type))
        chart_id = cursor.lastrowid
        logger.info(f"✓ Created size chart (ID: {chart_id})")
        return chart_id


def add_size(chart_id, label, order, measurements):
    """
    Add a size with all measurements - Uses EXISTING 5-table system
    
    Args:
        chart_id: ID of the size chart
        label: Size label (S, M, L, XL, 32, etc.)
        order: Size order for sorting (1, 2, 3, 4...)
        measurements: Dictionary with measurement ranges
                     Example: {
                         'chest': (91, 97),
                         'shoulder': (44, 46),
                         'waist': (81, 86)
                     }
    """
    # Step 1: Insert the size label
    size_id = db_manager.insert_size(chart_id, label, order)
    
    # Step 2: Insert each measurement as a separate row
    measurement_map = {
        'chest': 'chest',
        'shoulder': 'shoulder_breadth',
        'waist': 'waist',
        'hip': 'hip',
        'arm_length': 'arm_length',
        'leg_length': 'leg_length'
    }
    
    for meas_name, db_type in measurement_map.items():
        if meas_name in measurements:
            min_val, max_val = measurements[meas_name]
            optimal_val = (min_val + max_val) / 2
            
            db_manager.insert_size_measurement(
                size_id=size_id,
                measurement_type=db_type,
                min_val=min_val,
                max_val=max_val,
                optimal_val=optimal_val,
                tolerance=2.0,
                weight=1.0
            )
    
    logger.info(f"  ✓ Added size '{label}' with {len(measurements)} measurements")
    return size_id


# ============================================================================
# EXAMPLE TEMPLATES
# ============================================================================

def example_mens_tshirt():
    """Complete example: Add Nike Men's T-Shirt size chart"""
    
    print("\n" + "="*70)
    print("EXAMPLE: Adding Nike Men's T-Shirt Size Chart")
    print("="*70 + "\n")
    
    # Step 1: Add brand
    brand_id = add_brand("Nike", "USA", "US", "https://www.nike.com")
    
    # Step 2: Add category
    category_id = add_category("T-Shirt", "Men", "Casual t-shirts")
    
    # Step 3: Create size chart (the link)
    chart_id = create_size_chart(
        brand_id, 
        category_id, 
        "Nike Men's Essential T-Shirts",
        "Regular"
    )
    
    # Step 4: Add sizes with measurements (all in one table!)
    logger.info("Adding sizes...")
    
    sizes_data = [
        ("XS", 1, {
            'chest': (81, 86),
            'shoulder': (40, 42),
            'waist': (71, 76)
        }),
        ("S", 2, {
            'chest': (86, 91),
            'shoulder': (42, 44),
            'waist': (76, 81)
        }),
        ("M", 3, {
            'chest': (91, 97),
            'shoulder': (44, 46),
            'waist': (81, 86)
        }),
        ("L", 4, {
            'chest': (97, 104),
            'shoulder': (46, 48),
            'waist': (86, 94)
        }),
        ("XL", 5, {
            'chest': (104, 114),
            'shoulder': (48, 51),
            'waist': (94, 104)
        }),
    ]
    
    for label, order, measurements in sizes_data:
        add_size(chart_id, label, order, measurements)
    
    print("\n" + "="*70)
    print("✅ SUCCESS! Nike Men's T-Shirt size chart added")
    print("="*70)
    print(f"\nSummary:")
    print(f"  Brand ID: {brand_id}")
    print(f"  Category ID: {category_id}")
    print(f"  Chart ID: {chart_id}")
    print(f"  Sizes added: {len(sizes_data)}")
    print()


def example_womens_jeans():
    """Example: Add Zara Women's Jeans"""
    
    print("\n" + "="*70)
    print("EXAMPLE: Adding Zara Women's Jeans Size Chart")
    print("="*70 + "\n")
    
    brand_id = add_brand("Zara", "Spain", "EU", "https://www.zara.com")
    category_id = add_category("Jeans", "Women", "Denim pants")
    chart_id = create_size_chart(brand_id, category_id, "Zara Women's Jeans", "Regular")
    
    logger.info("Adding sizes...")
    
    # Jeans use: waist, hip, leg_length (not chest or shoulder)
    sizes_data = [
        ("24", 1, {
            'waist': (60, 62),
            'hip': (84, 87),
            'leg_length': (76, 81)
        }),
        ("26", 2, {
            'waist': (64, 66),
            'hip': (88, 91),
            'leg_length': (76, 81)
        }),
        ("28", 3, {
            'waist': (68, 70),
            'hip': (92, 95),
            'leg_length': (81, 86)
        }),
        ("30", 4, {
            'waist': (72, 74),
            'hip': (96, 99),
            'leg_length': (81, 86)
        }),
    ]
    
    for label, order, measurements in sizes_data:
        add_size(chart_id, label, order, measurements)
    
    print("\n✅ Zara Women's Jeans added!")
    print(f"Sizes: {len(sizes_data)}\n")


def example_womens_dress():
    """Example: Add H&M Women's Dress"""
    
    print("\n" + "="*70)
    print("EXAMPLE: Adding H&M Women's Dress Size Chart")
    print("="*70 + "\n")
    
    brand_id = add_brand("H&M", "Sweden", "EU", "https://www.hm.com")
    category_id = add_category("Dress", "Women", "Dresses")
    chart_id = create_size_chart(brand_id, category_id, "H&M Women's Dresses", "Regular")
    
    logger.info("Adding sizes...")
    
    # Dresses use: chest (bust), waist, hip
    sizes_data = [
        ("XS", 1, {
            'chest': (80, 84),
            'waist': (60, 64),
            'hip': (86, 90)
        }),
        ("S", 2, {
            'chest': (84, 88),
            'waist': (64, 68),
            'hip': (90, 94)
        }),
        ("M", 3, {
            'chest': (88, 92),
            'waist': (68, 72),
            'hip': (94, 98)
        }),
        ("L", 4, {
            'chest': (92, 98),
            'waist': (72, 78),
            'hip': (98, 104)
        }),
    ]
    
    for label, order, measurements in sizes_data:
        add_size(chart_id, label, order, measurements)
    
    print("\n✅ H&M Women's Dress added!")
    print(f"Sizes: {len(sizes_data)}\n")


# ============================================================================
# VIEW DATABASE
# ============================================================================

def view_database():
    """Show what's currently in the database"""
    
    print("\n" + "="*70)
    print("CURRENT DATABASE CONTENTS")
    print("="*70 + "\n")
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Show brands
        cursor.execute("SELECT brand_id, brand_name, size_system FROM brands ORDER BY brand_name")
        brands = cursor.fetchall()
        print(f"📦 BRANDS ({len(brands)}):")
        for row in brands:
            print(f"   {row[0]}. {row[1]} ({row[2]})")
        
        # Show categories
        cursor.execute("SELECT category_id, category_name, gender FROM garment_categories ORDER BY category_name")
        categories = cursor.fetchall()
        print(f"\n👕 GARMENT CATEGORIES ({len(categories)}):")
        for row in categories:
            print(f"   {row[0]}. {row[1]} ({row[2]})")
        
        # Show size charts
        cursor.execute("""
            SELECT sc.chart_id, b.brand_name, gc.category_name, gc.gender, sc.fit_type
            FROM size_charts sc
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            ORDER BY b.brand_name, gc.category_name
        """)
        charts = cursor.fetchall()
        print(f"\n📊 SIZE CHARTS ({len(charts)}):")
        for row in charts:
            print(f"   {row[0]}. {row[1]} - {row[2]} ({row[3]}) - {row[4]}")
        
        # Show size count
        cursor.execute("SELECT COUNT(*) FROM sizes")
        size_count = cursor.fetchone()[0]
        print(f"\n📏 TOTAL SIZES: {size_count}")
        
        # Show measurement count
        cursor.execute("SELECT COUNT(*) FROM size_measurements")
        meas_count = cursor.fetchone()[0]
        print(f"📐 TOTAL MEASUREMENTS: {meas_count}")
        
        # Show sample data
        cursor.execute("""
            SELECT b.brand_name, gc.category_name, s.size_label, 
                   COUNT(sm.measurement_id) as meas_count
            FROM sizes s
            JOIN size_charts sc ON s.chart_id = sc.chart_id
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            LEFT JOIN size_measurements sm ON s.size_id = sm.size_id
            GROUP BY s.size_id
            ORDER BY b.brand_name, gc.category_name, s.size_order
            LIMIT 10
        """)
        samples = cursor.fetchall()
        if samples:
            print(f"\n📋 SAMPLE SIZES (first 10):")
            for row in samples:
                print(f"   {row[0]} {row[1]} Size {row[2]} - {row[3]} measurements")
        
        print()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n🎯 SIZE CHART MANAGER - Fashion Intelligence Platform\n")
    print("Choose an option:")
    print("  1. View current database")
    print("  2. Add Nike Men's T-Shirt example")
    print("  3. Add Zara Women's Jeans example")
    print("  4. Add H&M Women's Dress example")
    print("  5. Add all examples")
    print()
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "1":
        view_database()
    elif choice == "2":
        example_mens_tshirt()
    elif choice == "3":
        example_womens_jeans()
    elif choice == "4":
        example_womens_dress()
    elif choice == "5":
        print("\n📦 Adding all examples...\n")
        example_mens_tshirt()
        example_womens_jeans()
        example_womens_dress()
        view_database()
    else:
        print("Invalid choice")
    
    print("\n💡 Tips:")
    print("  - Modify this script to add your own brands")
    print("  - Works with your existing 5-table database")
    print("  - Check DATABASE_DESIGN_EXPLAINED.md for documentation")
    print()
