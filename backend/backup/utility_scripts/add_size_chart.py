"""
Simple Script to Add a New Size Chart
Copy and modify this template to add your own size charts
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_size_chart_example():
    """
    Example: Add a Gap Men's T-Shirt size chart
    Modify the values below for your own brand and measurements
    """
    
    print("\n" + "="*70)
    print("Adding Custom Size Chart")
    print("="*70 + "\n")
    
    # =========================================================================
    # STEP 1: Define Brand Information
    # =========================================================================
    BRAND_NAME = "Gap"                    # Change this to your brand
    BRAND_COUNTRY = "USA"
    SIZE_SYSTEM = "US"                    # US, UK, EU, Asia, International
    BRAND_WEBSITE = "https://www.gap.com"
    BRAND_NOTES = "Casual clothing"
    
    # Get or create the brand
    brand_id = db_manager.get_or_create_brand(
        BRAND_NAME, BRAND_COUNTRY, SIZE_SYSTEM, BRAND_WEBSITE, BRAND_NOTES
    )
    logger.info(f"✅ Brand: {BRAND_NAME} (ID: {brand_id})")
    
    # =========================================================================
    # STEP 2: Define Category
    # =========================================================================
    CATEGORY_NAME = "T-Shirt"           # T-Shirt, Dress Shirt, Jeans, Dress, Jacket, etc.
    GENDER = "Men"                       # Men, Women, Unisex
    CATEGORY_DESCRIPTION = "Casual t-shirts"
    
    # Get or create the category
    category_id = db_manager.get_or_create_category(
        CATEGORY_NAME, GENDER, CATEGORY_DESCRIPTION
    )
    logger.info(f"✅ Category: {CATEGORY_NAME} {GENDER} (ID: {category_id})")
    
    # =========================================================================
    # STEP 3: Define Measurement Requirements (if not already set)
    # =========================================================================
    # These define which body measurements are important for this garment type
    measurement_requirements = [
        # (measurement_type, importance_weight, is_required, description)
        ("chest", 1.0, True, "Primary measurement for upper body fit"),
        ("shoulder_breadth", 0.8, True, "Important for shoulder fit"),
        ("waist", 0.5, False, "For overall fit"),
        # Add more measurements as needed: arm_length, hip, etc.
    ]
    
    for meas_type, weight, required, desc in measurement_requirements:
        try:
            db_manager.insert_category_measurement_mapping(
                category_id, meas_type, weight, required, desc
            )
            logger.info(f"  ✓ Added requirement: {meas_type}")
        except Exception as e:
            # Requirement might already exist, skip
            pass
    
    # =========================================================================
    # STEP 4: Create Size Chart
    # =========================================================================
    CHART_NAME = "Gap Men's Essential T-Shirts"
    FIT_TYPE = "Regular"                 # Regular, Slim, Relaxed, Athletic, Oversized
    
    try:
        chart_id = db_manager.insert_size_chart(
            brand_id, category_id, CHART_NAME, FIT_TYPE
        )
        logger.info(f"✅ Size Chart: {CHART_NAME} (ID: {chart_id})")
    except Exception as e:
        logger.error(f"❌ Error creating size chart: {e}")
        logger.info("💡 Tip: This brand+category+fit combination might already exist")
        return
    
    # =========================================================================
    # STEP 5: Add Sizes with Measurements
    # =========================================================================
    # All measurements in CENTIMETERS
    # Format: (size_label, size_order, {measurement_type: (min_cm, max_cm)})
    
    sizes_data = [
        ("XS", 1, {
            "chest": (84, 89),
            "shoulder_breadth": (41, 43),
            "waist": (74, 79)
        }),
        ("S", 2, {
            "chest": (89, 94),
            "shoulder_breadth": (43, 45),
            "waist": (79, 84)
        }),
        ("M", 3, {
            "chest": (94, 99),
            "shoulder_breadth": (45, 47),
            "waist": (84, 89)
        }),
        ("L", 4, {
            "chest": (99, 107),
            "shoulder_breadth": (47, 50),
            "waist": (89, 97)
        }),
        ("XL", 5, {
            "chest": (107, 117),
            "shoulder_breadth": (50, 53),
            "waist": (97, 107)
        }),
        ("2XL", 6, {
            "chest": (117, 127),
            "shoulder_breadth": (53, 56),
            "waist": (107, 117)
        }),
    ]
    
    logger.info("📏 Adding sizes and measurements...")
    
    for size_label, size_order, measurements in sizes_data:
        # Insert the size
        size_id = db_manager.insert_size(chart_id, size_label, size_order)
        
        # Insert measurements for this size
        for meas_type, (min_val, max_val) in measurements.items():
            optimal_val = (min_val + max_val) / 2  # Calculate middle value
            
            db_manager.insert_size_measurement(
                size_id=size_id,
                measurement_type=meas_type,
                min_value=min_val,
                max_value=max_val,
                optimal_value=optimal_val,
                tolerance=2.5,      # Acceptable deviation in cm
                weight=1.0          # Importance of this measurement
            )
        
        logger.info(f"  ✓ Size {size_label}: {len(measurements)} measurements")
    
    # =========================================================================
    # SUCCESS!
    # =========================================================================
    print("\n" + "="*70)
    print("✅ SUCCESS! Size chart added to database")
    print("="*70)
    print(f"\nSummary:")
    print(f"  Brand ID: {brand_id} ({BRAND_NAME})")
    print(f"  Category ID: {category_id} ({CATEGORY_NAME} {GENDER})")
    print(f"  Size Chart ID: {chart_id}")
    print(f"  Sizes added: {len(sizes_data)}")
    print(f"\nYou can now use this size chart in the Size Recommendation feature!")
    print(f"\nAPI Test:")
    print(f'  curl http://localhost:5000/api/size/size-chart/{brand_id}/{category_id}')
    print()


# ============================================================================
# CUSTOM TEMPLATES
# ============================================================================

def add_womens_dress():
    """Template for adding women's dress size chart"""
    
    brand_id = db_manager.get_or_create_brand("Zara", "Spain", "EU")
    category_id = db_manager.get_or_create_category("Dress", "Women", "One-piece garments")
    
    # Women's dresses need: chest (bust), waist, hip measurements
    chart_id = db_manager.insert_size_chart(brand_id, category_id, "Zara Women's Dresses", "Regular")
    
    sizes_data = [
        ("XS", 1, {"chest": (80, 84), "waist": (60, 64), "hip": (86, 90)}),
        ("S", 2, {"chest": (84, 88), "waist": (64, 68), "hip": (90, 94)}),
        ("M", 3, {"chest": (88, 92), "waist": (68, 72), "hip": (94, 98)}),
        ("L", 4, {"chest": (92, 98), "waist": (72, 78), "hip": (98, 104)}),
        ("XL", 5, {"chest": (98, 104), "waist": (78, 84), "hip": (104, 110)}),
    ]
    
    for size_label, order, measurements in sizes_data:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            db_manager.insert_size_measurement(size_id, meas_type, min_val, max_val, optimal, 2.0)
    
    print(f"✅ Added women's dress size chart (Chart ID: {chart_id})")


def add_mens_jeans():
    """Template for adding men's jeans size chart"""
    
    brand_id = db_manager.get_or_create_brand("Levi's", "USA", "US")
    category_id = db_manager.get_or_create_category("Jeans", "Men", "Denim pants")
    
    # Jeans need: waist, hip, leg_length measurements
    chart_id = db_manager.insert_size_chart(brand_id, category_id, "Levi's 501 Jeans", "Regular")
    
    # Jeans often use numeric waist sizes
    sizes_data = [
        ("28", 1, {"waist": (71, 73), "hip": (88, 91), "leg_length": (76, 81)}),
        ("30", 2, {"waist": (76, 78), "hip": (93, 96), "leg_length": (76, 81)}),
        ("32", 3, {"waist": (81, 83), "hip": (99, 102), "leg_length": (81, 86)}),
        ("34", 4, {"waist": (86, 89), "hip": (104, 107), "leg_length": (81, 86)}),
        ("36", 5, {"waist": (91, 94), "hip": (109, 112), "leg_length": (81, 86)}),
    ]
    
    for size_label, order, measurements in sizes_data:
        size_id = db_manager.insert_size(chart_id, size_label, order)
        for meas_type, (min_val, max_val) in measurements.items():
            optimal = (min_val + max_val) / 2
            db_manager.insert_size_measurement(size_id, meas_type, min_val, max_val, optimal, 2.0)
    
    print(f"✅ Added men's jeans size chart (Chart ID: {chart_id})")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n🔧 Custom Size Chart Addition Tool\n")
    print("Options:")
    print("  1. Add example: Gap Men's T-Shirt (default)")
    print("  2. Add example: Women's Dress template")
    print("  3. Add example: Men's Jeans template")
    print()
    
    choice = input("Enter your choice (1-3) or press Enter for option 1: ").strip()
    
    if choice == "2":
        print("\n👗 Adding Women's Dress example...")
        add_womens_dress()
    elif choice == "3":
        print("\n👖 Adding Men's Jeans example...")
        add_mens_jeans()
    else:
        print("\n👕 Adding Men's T-Shirt example...")
        add_size_chart_example()
    
    print("\n💡 To add your own size chart:")
    print("   1. Copy this file: add_size_chart.py")
    print("   2. Modify the brand, category, and measurement values")
    print("   3. Run: python your_custom_script.py")
    print()
