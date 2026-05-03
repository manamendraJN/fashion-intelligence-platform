"""Complete all missing size charts for all brands and categories"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager


# Standard size templates for each category
SIZE_TEMPLATES = {
    'T-Shirt (Men)': [
        {'label': 'XS', 'order': 1, 'chest': (84, 89), 'waist': (70, 75), 'shoulder_breadth': (42, 44)},
        {'label': 'S', 'order': 2, 'chest': (89, 94), 'waist': (75, 80), 'shoulder_breadth': (44, 46)},
        {'label': 'M', 'order': 3, 'chest': (94, 99), 'waist': (80, 85), 'shoulder_breadth': (46, 48)},
        {'label': 'L', 'order': 4, 'chest': (99, 104), 'waist': (85, 90), 'shoulder_breadth': (48, 50)},
        {'label': 'XL', 'order': 5, 'chest': (104, 109), 'waist': (90, 95), 'shoulder_breadth': (50, 52)},
        {'label': 'XXL', 'order': 6, 'chest': (109, 116), 'waist': (95, 102), 'shoulder_breadth': (52, 54)},
    ],
    'T-Shirt (Women)': [
        {'label': 'XS', 'order': 1, 'chest': (78, 82), 'waist': (60, 64), 'shoulder_breadth': (36, 38)},
        {'label': 'S', 'order': 2, 'chest': (82, 86), 'waist': (64, 68), 'shoulder_breadth': (38, 40)},
        {'label': 'M', 'order': 3, 'chest': (86, 90), 'waist': (68, 72), 'shoulder_breadth': (40, 42)},
        {'label': 'L', 'order': 4, 'chest': (90, 96), 'waist': (72, 78), 'shoulder_breadth': (42, 44)},
        {'label': 'XL', 'order': 5, 'chest': (96, 102), 'waist': (78, 84), 'shoulder_breadth': (44, 46)},
    ],
    'Shirt (Men)': [
        {'label': 'S', 'order': 1, 'chest': (88, 92), 'waist': (76, 80), 'shoulder_breadth': (44, 46), 'sleeve_length': (60, 62)},
        {'label': 'M', 'order': 2, 'chest': (92, 96), 'waist': (80, 84), 'shoulder_breadth': (46, 48), 'sleeve_length': (62, 64)},
        {'label': 'L', 'order': 3, 'chest': (96, 100), 'waist': (84, 88), 'shoulder_breadth': (48, 50), 'sleeve_length': (64, 66)},
        {'label': 'XL', 'order': 4, 'chest': (100, 106), 'waist': (88, 94), 'shoulder_breadth': (50, 52), 'sleeve_length': (66, 68)},
        {'label': 'XXL', 'order': 5, 'chest': (106, 112), 'waist': (94, 100), 'shoulder_breadth': (52, 54), 'sleeve_length': (68, 70)},
    ],
    'Dress (Women)': [
        {'label': 'XS', 'order': 1, 'chest': (80, 84), 'waist': (62, 66), 'hip': (88, 92)},
        {'label': 'S', 'order': 2, 'chest': (84, 88), 'waist': (66, 70), 'hip': (92, 96)},
        {'label': 'M', 'order': 3, 'chest': (88, 92), 'waist': (70, 74), 'hip': (96, 100)},
        {'label': 'L', 'order': 4, 'chest': (92, 98), 'waist': (74, 80), 'hip': (100, 106)},
        {'label': 'XL', 'order': 5, 'chest': (98, 104), 'waist': (80, 86), 'hip': (106, 112)},
    ],
    'Jeans (Men)': [
        {'label': '28', 'order': 1, 'waist': (71, 74), 'hip': (86, 89), 'leg_length': (81, 84)},
        {'label': '30', 'order': 2, 'waist': (76, 79), 'hip': (91, 94), 'leg_length': (81, 84)},
        {'label': '32', 'order': 3, 'waist': (81, 84), 'hip': (97, 99), 'leg_length': (81, 84)},
        {'label': '34', 'order': 4, 'waist': (86, 89), 'hip': (102, 104), 'leg_length': (81, 84)},
        {'label': '36', 'order': 5, 'waist': (91, 94), 'hip': (107, 109), 'leg_length': (81, 84)},
        {'label': '38', 'order': 6, 'waist': (97, 99), 'hip': (112, 114), 'leg_length': (81, 84)},
    ],
    'Jeans (Women)': [
        {'label': '25', 'order': 1, 'waist': (61, 64), 'hip': (86, 89), 'leg_length': (76, 79)},
        {'label': '26', 'order': 2, 'waist': (64, 66), 'hip': (89, 91), 'leg_length': (76, 79)},
        {'label': '27', 'order': 3, 'waist': (66, 69), 'hip': (91, 94), 'leg_length': (76, 79)},
        {'label': '28', 'order': 4, 'waist': (69, 71), 'hip': (94, 97), 'leg_length': (76, 79)},
        {'label': '29', 'order': 5, 'waist': (71, 74), 'hip': (97, 99), 'leg_length': (76, 79)},
        {'label': '30', 'order': 6, 'waist': (74, 76), 'hip': (99, 102), 'leg_length': (76, 79)},
    ],
    'Pants (Men)': [
        {'label': '28', 'order': 1, 'waist': (71, 74), 'hip': (86, 89), 'leg_length': (81, 84)},
        {'label': '30', 'order': 2, 'waist': (76, 79), 'hip': (91, 94), 'leg_length': (81, 84)},
        {'label': '32', 'order': 3, 'waist': (81, 84), 'hip': (97, 99), 'leg_length': (81, 84)},
        {'label': '34', 'order': 4, 'waist': (86, 89), 'hip': (102, 104), 'leg_length': (81, 84)},
        {'label': '36', 'order': 5, 'waist': (91, 94), 'hip': (107, 109), 'leg_length': (81, 84)},
        {'label': '38', 'order': 6, 'waist': (97, 99), 'hip': (112, 114), 'leg_length': (81, 84)},
    ],
    'Jacket (Men)': [
        {'label': 'S', 'order': 1, 'chest': (90, 94), 'waist': (78, 82), 'shoulder_breadth': (44, 46), 'sleeve_length': (62, 64)},
        {'label': 'M', 'order': 2, 'chest': (94, 98), 'waist': (82, 86), 'shoulder_breadth': (46, 48), 'sleeve_length': (64, 66)},
        {'label': 'L', 'order': 3, 'chest': (98, 102), 'waist': (86, 90), 'shoulder_breadth': (48, 50), 'sleeve_length': (66, 68)},
        {'label': 'XL', 'order': 4, 'chest': (102, 108), 'waist': (90, 96), 'shoulder_breadth': (50, 52), 'sleeve_length': (68, 70)},
        {'label': 'XXL', 'order': 5, 'chest': (108, 114), 'waist': (96, 102), 'shoulder_breadth': (52, 54), 'sleeve_length': (70, 72)},
    ],
    'Jacket (Women)': [
        {'label': 'XS', 'order': 1, 'chest': (82, 86), 'waist': (64, 68), 'shoulder_breadth': (38, 40), 'sleeve_length': (58, 60)},
        {'label': 'S', 'order': 2, 'chest': (86, 90), 'waist': (68, 72), 'shoulder_breadth': (40, 42), 'sleeve_length': (60, 62)},
        {'label': 'M', 'order': 3, 'chest': (90, 94), 'waist': (72, 76), 'shoulder_breadth': (42, 44), 'sleeve_length': (62, 64)},
        {'label': 'L', 'order': 4, 'chest': (94, 100), 'waist': (76, 82), 'shoulder_breadth': (44, 46), 'sleeve_length': (64, 66)},
        {'label': 'XL', 'order': 5, 'chest': (100, 106), 'waist': (82, 88), 'shoulder_breadth': (46, 48), 'sleeve_length': (66, 68)},
    ],
    'Hoodie (Men)': [
        {'label': 'S', 'order': 1, 'chest': (92, 96), 'waist': (80, 84), 'shoulder_breadth': (45, 47)},
        {'label': 'M', 'order': 2, 'chest': (96, 100), 'waist': (84, 88), 'shoulder_breadth': (47, 49)},
        {'label': 'L', 'order': 3, 'chest': (100, 104), 'waist': (88, 92), 'shoulder_breadth': (49, 51)},
        {'label': 'XL', 'order': 4, 'chest': (104, 110), 'waist': (92, 98), 'shoulder_breadth': (51, 53)},
        {'label': 'XXL', 'order': 5, 'chest': (110, 116), 'waist': (98, 104), 'shoulder_breadth': (53, 55)},
    ],
    'Hoodie (Women)': [
        {'label': 'XS', 'order': 1, 'chest': (84, 88), 'waist': (66, 70), 'shoulder_breadth': (39, 41)},
        {'label': 'S', 'order': 2, 'chest': (88, 92), 'waist': (70, 74), 'shoulder_breadth': (41, 43)},
        {'label': 'M', 'order': 3, 'chest': (92, 96), 'waist': (74, 78), 'shoulder_breadth': (43, 45)},
        {'label': 'L', 'order': 4, 'chest': (96, 102), 'waist': (78, 84), 'shoulder_breadth': (45, 47)},
        {'label': 'XL', 'order': 5, 'chest': (102, 108), 'waist': (84, 90), 'shoulder_breadth': (47, 49)},
    ],
    'Shorts (Men)': [
        {'label': 'S', 'order': 1, 'waist': (74, 78), 'hip': (88, 92), 'leg_length': (45, 48)},
        {'label': 'M', 'order': 2, 'waist': (78, 82), 'hip': (92, 96), 'leg_length': (45, 48)},
        {'label': 'L', 'order': 3, 'waist': (82, 86), 'hip': (96, 100), 'leg_length': (45, 48)},
        {'label': 'XL', 'order': 4, 'waist': (86, 92), 'hip': (100, 106), 'leg_length': (45, 48)},
        {'label': 'XXL', 'order': 5, 'waist': (92, 98), 'hip': (106, 112), 'leg_length': (45, 48)},
    ],
    'Shorts (Women)': [
        {'label': 'XS', 'order': 1, 'waist': (62, 66), 'hip': (88, 92), 'leg_length': (38, 41)},
        {'label': 'S', 'order': 2, 'waist': (66, 70), 'hip': (92, 96), 'leg_length': (38, 41)},
        {'label': 'M', 'order': 3, 'waist': (70, 74), 'hip': (96, 100), 'leg_length': (38, 41)},
        {'label': 'L', 'order': 4, 'waist': (74, 80), 'hip': (100, 106), 'leg_length': (38, 41)},
        {'label': 'XL', 'order': 5, 'waist': (80, 86), 'hip': (106, 112), 'leg_length': (38, 41)},
    ],
    'Skirt (Women)': [
        {'label': 'XS', 'order': 1, 'waist': (62, 66), 'hip': (88, 92), 'length': (45, 55)},
        {'label': 'S', 'order': 2, 'waist': (66, 70), 'hip': (92, 96), 'length': (45, 55)},
        {'label': 'M', 'order': 3, 'waist': (70, 74), 'hip': (96, 100), 'length': (45, 55)},
        {'label': 'L', 'order': 4, 'waist': (74, 80), 'hip': (100, 106), 'length': (45, 55)},
        {'label': 'XL', 'order': 5, 'waist': (80, 86), 'hip': (106, 112), 'length': (45, 55)},
    ],
    'Polo (Men)': [
        {'label': 'S', 'order': 1, 'chest': (88, 92), 'waist': (76, 80), 'shoulder_breadth': (44, 46)},
        {'label': 'M', 'order': 2, 'chest': (92, 96), 'waist': (80, 84), 'shoulder_breadth': (46, 48)},
        {'label': 'L', 'order': 3, 'chest': (96, 100), 'waist': (84, 88), 'shoulder_breadth': (48, 50)},
        {'label': 'XL', 'order': 4, 'chest': (100, 106), 'waist': (88, 94), 'shoulder_breadth': (50, 52)},
        {'label': 'XXL', 'order': 5, 'chest': (106, 112), 'waist': (94, 100), 'shoulder_breadth': (52, 54)},
    ],
    'Sweater (Men)': [
        {'label': 'S', 'order': 1, 'chest': (90, 94), 'waist': (78, 82), 'shoulder_breadth': (44, 46), 'sleeve_length': (62, 64)},
        {'label': 'M', 'order': 2, 'chest': (94, 98), 'waist': (82, 86), 'shoulder_breadth': (46, 48), 'sleeve_length': (64, 66)},
        {'label': 'L', 'order': 3, 'chest': (98, 102), 'waist': (86, 90), 'shoulder_breadth': (48, 50), 'sleeve_length': (66, 68)},
        {'label': 'XL', 'order': 4, 'chest': (102, 108), 'waist': (90, 96), 'shoulder_breadth': (50, 52), 'sleeve_length': (68, 70)},
        {'label': 'XXL', 'order': 5, 'chest': (108, 114), 'waist': (96, 102), 'shoulder_breadth': (52, 54), 'sleeve_length': (70, 72)},
    ],
    'Sweater (Women)': [
        {'label': 'XS', 'order': 1, 'chest': (82, 86), 'waist': (64, 68), 'shoulder_breadth': (38, 40), 'sleeve_length': (58, 60)},
        {'label': 'S', 'order': 2, 'chest': (86, 90), 'waist': (68, 72), 'shoulder_breadth': (40, 42), 'sleeve_length': (60, 62)},
        {'label': 'M', 'order': 3, 'chest': (90, 94), 'waist': (72, 76), 'shoulder_breadth': (42, 44), 'sleeve_length': (62, 64)},
        {'label': 'L', 'order': 4, 'chest': (94, 100), 'waist': (76, 82), 'shoulder_breadth': (44, 46), 'sleeve_length': (64, 66)},
        {'label': 'XL', 'order': 5, 'chest': (100, 106), 'waist': (82, 88), 'shoulder_breadth': (46, 48), 'sleeve_length': (66, 68)},
    ],
}


def add_size_chart_if_missing(brand_name, category_name, gender):
    """Add size chart if it doesn't exist"""
    
    # Get brand and category IDs
    brands = db_manager.get_brands()
    brand = next((b for b in brands if b['brand_name'] == brand_name), None)
    if not brand:
        print(f"   ⚠️  Brand '{brand_name}' not found, skipping")
        return False
    
    categories = db_manager.get_categories()
    category = next((c for c in categories if c['category_name'] == category_name and c['gender'] == gender), None)
    if not category:
        print(f"   ⚠️  Category '{category_name} ({gender})' not found, skipping")
        return False
    
    # Check if chart already exists
    with db_manager.get_connection() as conn:
        existing = conn.execute(
            "SELECT chart_id FROM size_charts WHERE brand_id=? AND category_id=?",
            (brand['brand_id'], category['category_id'])
        ).fetchone()
    
    if existing:
        return False  # Already exists
    
    # Create size chart
    cat_key = f"{category_name} ({gender})"
    if cat_key not in SIZE_TEMPLATES:
        print(f"   ⚠️  No template for '{cat_key}', skipping")
        return False
    
    try:
        chart_id = db_manager.insert_size_chart(brand['brand_id'], category['category_id'], fit_type="Regular")
        
        # Add sizes
        sizes = SIZE_TEMPLATES[cat_key]
        for size in sizes:
            measurements = {}
            for key, value in size.items():
                if key not in ['label', 'order']:
                    measurements[key] = value
            
            db_manager.insert_size(
                chart_id=chart_id,
                size_label=size['label'],
                size_order=size['order'],
                measurements=measurements
            )
        
        print(f"   ✅ Added {category_name} ({gender}) - {len(sizes)} sizes")
        return True
    except Exception as e:
        print(f"   ❌ Error adding {category_name} ({gender}): {e}")
        return False


def complete_all_charts():
    """Add all missing size charts"""
    
    print("\n" + "="*70)
    print("COMPLETING ALL SIZE CHARTS")
    print("="*70)
    
    brands = db_manager.get_brands()
    categories = db_manager.get_categories()
    
    print(f"\n📋 Processing {len(brands)} brands × {len(categories)} categories = {len(brands) * len(categories)} combinations")
    
    added_count = 0
    skipped_count = 0
    
    for brand in sorted(brands, key=lambda b: b['brand_name']):
        brand_added = 0
        print(f"\n🏷️  {brand['brand_name']}")
        
        for category in sorted(categories, key=lambda c: (c['gender'], c['category_name'])):
            if add_size_chart_if_missing(brand['brand_name'], category['category_name'], category['gender']):
                brand_added += 1
                added_count += 1
            else:
                skipped_count += 1
        
        if brand_added == 0:
            print(f"   ⏭️  All charts already exist")
    
    print("\n" + "="*70)
    print(f"✅ COMPLETE!")
    print(f"   Added: {added_count} new size charts")
    print(f"   Skipped: {skipped_count} (already existed)")
    print(f"   Total: {added_count + skipped_count} brand/category combinations")
    print("="*70)
    
    # Show final coverage
    print("\n📊 Running coverage check...")
    os.system("python check_coverage.py")


if __name__ == "__main__":
    complete_all_charts()
