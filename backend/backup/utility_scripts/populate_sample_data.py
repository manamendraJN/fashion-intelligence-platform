"""
Sample Data Population Script
Populates database with example brand size charts for research prototype

Data sources and methodology:
- Brand size charts collected from official brand websites
- Measurements are in centimeters
- Data represents common US/International brands for demonstration
"""

import sys
from pathlib import Path
import argparse

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_database():
    """Clear all data from database tables"""
    logger.info("🗑️  Clearing existing data...")
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        # Delete in reverse order of dependencies
        cursor.execute("DELETE FROM recommendation_log")
        cursor.execute("DELETE FROM user_measurements")
        cursor.execute("DELETE FROM size_measurements")
        cursor.execute("DELETE FROM category_measurements")
        cursor.execute("DELETE FROM sizes")
        cursor.execute("DELETE FROM size_charts")
        cursor.execute("DELETE FROM garment_categories")
        cursor.execute("DELETE FROM brands")
    logger.info("✅ Database cleared")


def populate_sample_data(reset=False):
    """Populate database with sample brand data"""
    
    logger.info("🚀 Starting sample data population...")
    
    # Initialize database
    db_manager.initialize_database()    
    # Reset if requested
    if reset:
        reset_database()    
    # =========================================================================
    # STEP 1: Add Brands
    # =========================================================================
    logger.info("📦 Adding brands...")
    
    brands_data = [
        ("Nike", "USA", "US", "https://www.nike.com", "Athletic and sportswear"),
        ("Adidas", "Germany", "EU", "https://www.adidas.com", "Athletic and sportswear"),
        ("Zara", "Spain", "EU", "https://www.zara.com", "Fast fashion"),
        ("H&M", "Sweden", "EU", "https://www.hm.com", "Fast fashion"),
        ("Levi's", "USA", "US", "https://www.levi.com", "Denim and casual wear"),
        ("Uniqlo", "Japan", "Asia", "https://www.uniqlo.com", "Basic casual wear"),
    ]
    
    brands = {}
    for name, country, size_system, website, notes in brands_data:
        brand_id = db_manager.get_or_create_brand(name, country, size_system, website, notes)
        brands[name] = brand_id
        logger.info(f"  ✓ {name}")
    
    # =========================================================================
    # STEP 2: Add Garment Categories
    # =========================================================================
    logger.info("👕 Adding garment categories...")
    
    categories_data = [
        ("T-Shirt", "Men", "Short sleeve and long sleeve t-shirts"),
        ("T-Shirt", "Women", "Short sleeve and long sleeve t-shirts"),
        ("Dress Shirt", "Men", "Formal button-up shirts"),
        ("Blouse", "Women", "Formal and casual tops"),
        ("Jeans", "Men", "Denim pants"),
        ("Jeans", "Women", "Denim pants"),
        ("Dress", "Women", "One-piece garments"),
        ("Jacket", "Men", "Outerwear and jackets"),
        ("Jacket", "Women", "Outerwear and jackets"),
    ]
    
    categories = {}
    for name, gender, description in categories_data:
        category_id = db_manager.get_or_create_category(name, gender, description)
        key = f"{name}_{gender}"
        categories[key] = category_id
        logger.info(f"  ✓ {name} ({gender})")
    
    # =========================================================================
    # STEP 3: Define Category Measurement Requirements
    # =========================================================================
    logger.info("📏 Mapping category measurement requirements...")
    
    # Define which measurements are important for each garment type
    category_requirements = {
        "T-Shirt_Men": [
            ("chest", 1.0, True, "Primary measurement for upper body fit"),
            ("shoulder_breadth", 0.8, True, "Important for shoulder fit"),
            ("arm_length", 0.6, False, "For sleeve length"),
            ("waist", 0.4, False, "For overall fit"),
        ],
        "T-Shirt_Women": [
            ("chest", 1.0, True, "Primary measurement for bust fit"),
            ("waist", 0.8, True, "Important for body fit"),
            ("shoulder_breadth", 0.7, True, "Important for shoulder fit"),
            ("hip", 0.5, False, "For overall fit"),
        ],
        "Dress Shirt_Men": [
            ("chest", 1.0, True, "Primary measurement"),
            ("shoulder_breadth", 0.9, True, "Critical for fit"),
            ("arm_length", 0.9, True, "For sleeve length"),
            ("waist", 0.7, True, "For body fit"),
        ],
        "Jeans_Men": [
            ("waist", 1.0, True, "Primary measurement"),
            ("hip", 0.9, True, "For hip fit"),
            ("leg_length", 0.9, True, "For inseam"),
            ("thigh", 0.7, False, "For thigh fit"),
        ],
        "Jeans_Women": [
            ("waist", 1.0, True, "Primary measurement"),
            ("hip", 1.0, True, "Critical for women's jeans"),
            ("leg_length", 0.9, True, "For inseam"),
            ("thigh", 0.7, False, "For thigh fit"),
        ],
        "Dress_Women": [
            ("chest", 1.0, True, "Bust measurement"),
            ("waist", 1.0, True, "Waist measurement"),
            ("hip", 1.0, True, "Hip measurement"),
            ("shoulder_breadth", 0.6, False, "For shoulder fit"),
        ],
        "Jacket_Men": [
            ("chest", 1.0, True, "Primary measurement"),
            ("shoulder_breadth", 0.9, True, "Critical for shoulder fit"),
            ("arm_length", 0.8, True, "For sleeve length"),
            ("waist", 0.6, False, "For overall fit"),
        ],
    }
    
    for cat_key, requirements in category_requirements.items():
        if cat_key in categories:
            for meas_type, weight, required, desc in requirements:
                db_manager.insert_category_measurement_mapping(
                    categories[cat_key], meas_type, weight, required, desc
                )
    
    # =========================================================================
    # STEP 4: Add Size Charts - Nike Men's T-Shirts
    # =========================================================================
    logger.info("📊 Adding Nike Men's T-Shirt size chart...")
    
    chart_id = db_manager.insert_size_chart(
        brands["Nike"], 
        categories["T-Shirt_Men"],
        "Nike Men's Athletic T-Shirts",
        "Regular"
    )
    
    # Nike Men's T-Shirt sizes (measurements in cm)
    nike_mens_tshirt = [
        ("XS", 1, {"chest": (81, 86), "shoulder_breadth": (40, 42), "waist": (71, 76)}),
        ("S", 2, {"chest": (86, 91), "shoulder_breadth": (42, 44), "waist": (76, 81)}),
        ("M", 3, {"chest": (91, 97), "shoulder_breadth": (44, 46), "waist": (81, 86)}),
        ("L", 4, {"chest": (97, 104), "shoulder_breadth": (46, 48), "waist": (86, 94)}),
        ("XL", 5, {"chest": (104, 114), "shoulder_breadth": (48, 51), "waist": (94, 104)}),
        ("2XL", 6, {"chest": (114, 124), "shoulder_breadth": (51, 54), "waist": (104, 114)}),
    ]
    
    for size_label, order, measurements in nike_mens_tshirt:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            db_manager.insert_size_measurement(
                size_id, meas_type, min_val, max_val, optimal, tolerance=2.5
            )
    
    # =========================================================================
    # STEP 5: Add Size Charts - Zara Women's Dresses
    # =========================================================================
    logger.info("📊 Adding Zara Women's Dress size chart...")
    
    chart_id = db_manager.insert_size_chart(
        brands["Zara"],
        categories["Dress_Women"],
        "Zara Women's Dresses",
        "Regular"
    )
    
    # Zara Women's Dress sizes (measurements in cm)
    zara_womens_dress = [
        ("XS", 1, {"chest": (80, 84), "waist": (60, 64), "hip": (86, 90)}),
        ("S", 2, {"chest": (84, 88), "waist": (64, 68), "hip": (90, 94)}),
        ("M", 3, {"chest": (88, 92), "waist": (68, 72), "hip": (94, 98)}),
        ("L", 4, {"chest": (92, 98), "waist": (72, 78), "hip": (98, 104)}),
        ("XL", 5, {"chest": (98, 104), "waist": (78, 84), "hip": (104, 110)}),
    ]
    
    for size_label, order, measurements in zara_womens_dress:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            # Women's garments often have tighter tolerance
            db_manager.insert_size_measurement(
                size_id, meas_type, min_val, max_val, optimal, tolerance=2.0,
                weight=1.0 if meas_type in ['chest', 'waist', 'hip'] else 0.8
            )
    
    # =========================================================================
    # STEP 6: Add Size Charts - Levi's Men's Jeans
    # =========================================================================
    logger.info("📊 Adding Levi's Men's Jeans size chart...")
    
    chart_id = db_manager.insert_size_chart(
        brands["Levi's"],
        categories["Jeans_Men"],
        "Levi's Men's 501 Jeans",
        "Regular"
    )
    
    # Levi's Men's Jeans - numeric waist sizes (measurements in cm)
    levis_mens_jeans = [
        ("28", 1, {"waist": (71, 73), "hip": (88, 91), "leg_length": (76, 81)}),
        ("30", 2, {"waist": (76, 78), "hip": (93, 96), "leg_length": (76, 81)}),
        ("32", 3, {"waist": (81, 83), "hip": (99, 102), "leg_length": (81, 86)}),
        ("34", 4, {"waist": (86, 89), "hip": (104, 107), "leg_length": (81, 86)}),
        ("36", 5, {"waist": (91, 94), "hip": (109, 112), "leg_length": (81, 86)}),
        ("38", 6, {"waist": (97, 99), "hip": (114, 117), "leg_length": (81, 86)}),
    ]
    
    for size_label, order, measurements in levis_mens_jeans:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            db_manager.insert_size_measurement(
                size_id, meas_type, min_val, max_val, optimal, tolerance=2.0
            )
    
    # =========================================================================
    # STEP 7: Add Size Charts - H&M Women's T-Shirts
    # =========================================================================
    logger.info("📊 Adding H&M Women's T-Shirt size chart...")
    
    chart_id = db_manager.insert_size_chart(
        brands["H&M"],
        categories["T-Shirt_Women"],
        "H&M Women's Basic T-Shirts",
        "Regular"
    )
    
    # H&M Women's T-Shirt sizes (measurements in cm)
    hm_womens_tshirt = [
        ("XS", 1, {"chest": (78, 82), "waist": (62, 66), "hip": (84, 88), "shoulder_breadth": (36, 38)}),
        ("S", 2, {"chest": (82, 86), "waist": (66, 70), "hip": (88, 92), "shoulder_breadth": (38, 40)}),
        ("M", 3, {"chest": (86, 90), "waist": (70, 74), "hip": (92, 96), "shoulder_breadth": (40, 42)}),
        ("L", 4, {"chest": (90, 96), "waist": (74, 80), "hip": (96, 102), "shoulder_breadth": (42, 44)}),
        ("XL", 5, {"chest": (96, 102), "waist": (80, 86), "hip": (102, 108), "shoulder_breadth": (44, 46)}),
    ]
    
    for size_label, order, measurements in hm_womens_tshirt:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            db_manager.insert_size_measurement(
                size_id, meas_type, min_val, max_val, optimal, tolerance=2.0
            )
    
    # =========================================================================
    # STEP 8: Add Size Charts - Uniqlo Men's Dress Shirts
    # =========================================================================
    logger.info("📊 Adding Uniqlo Men's Dress Shirt size chart...")
    
    chart_id = db_manager.insert_size_chart(
        brands["Uniqlo"],
        categories["Dress Shirt_Men"],
        "Uniqlo Men's Formal Shirts",
        "Regular"
    )
    
    # Uniqlo Men's Dress Shirt sizes (measurements in cm)
    uniqlo_mens_shirt = [
        ("S", 1, {"chest": (88, 92), "shoulder_breadth": (42, 44), "arm_length": (58, 60), "waist": (76, 80)}),
        ("M", 2, {"chest": (92, 96), "shoulder_breadth": (44, 46), "arm_length": (60, 62), "waist": (80, 84)}),
        ("L", 3, {"chest": (96, 102), "shoulder_breadth": (46, 48), "arm_length": (62, 64), "waist": (84, 90)}),
        ("XL", 4, {"chest": (102, 108), "shoulder_breadth": (48, 50), "arm_length": (64, 66), "waist": (90, 96)}),
        ("2XL", 5, {"chest": (108, 114), "shoulder_breadth": (50, 52), "arm_length": (66, 68), "waist": (96, 102)}),
    ]
    
    for size_label, order, measurements in uniqlo_mens_shirt:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            db_manager.insert_size_measurement(
                size_id, meas_type, min_val, max_val, optimal, tolerance=2.0,
                weight=1.0 if meas_type in ['chest', 'shoulder_breadth'] else 0.8
            )
    
    logger.info("✅ Sample data population completed!")
    logger.info(f"   - {len(brands_data)} brands")
    logger.info(f"   - {len(categories_data)} garment categories")
    logger.info(f"   - 6 size charts with multiple sizes")
    

def print_database_summary():
    """Print a summary of the database contents"""
    logger.info("\n📊 Database Summary:")
    
    brands = db_manager.get_brands()
    logger.info(f"\nBrands ({len(brands)}):")
    for brand in brands:
        logger.info(f"  - {brand['brand_name']} ({brand['size_system']})")
    
    categories = db_manager.get_categories()
    logger.info(f"\nGarment Categories ({len(categories)}):")
    for cat in categories:
        logger.info(f"  - {cat['category_name']} ({cat['gender']})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate database with sample brand size chart data"
    )
    parser.add_argument(
        "--reset", 
        action="store_true",
        help="Clear all existing data before populating"
    )
    args = parser.parse_args()
    
    populate_sample_data(reset=args.reset)
    print_database_summary()
    logger.info("\n✅ Database is ready for size matching!")
