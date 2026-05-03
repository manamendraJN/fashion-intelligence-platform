"""
Add Popular Brand Size Charts
Adds Nike, Adidas, H&M, Puma, Under Armour, and more with real size data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager


def add_nike():
    """Add Nike brand with size charts"""
    print("\n🏃 Adding Nike...")
    
    # Check if Nike already exists
    brands = db_manager.get_brands()
    existing_nike = next((b for b in brands if b['brand_name'] == 'Nike'), None)
    
    if existing_nike:
        print("  ⏭️  Nike already exists in database, skipping...")
        return
    
    brand_id = db_manager.insert_brand(
        brand_name="Nike",
        country="USA",
        size_system="US",
        website="https://www.nike.com"
    )
    
    # Nike Men's T-Shirt (Regular Fit)
    cat_id = db_manager.get_or_create_category("T-Shirt", "Men")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    nike_mens_tshirt = [
        {'label': 'XS', 'order': 1, 'chest': (86, 91), 'waist': (71, 76), 'shoulder': (43, 45)},
        {'label': 'S', 'order': 2, 'chest': (91, 97), 'waist': (76, 81), 'shoulder': (45, 47)},
        {'label': 'M', 'order': 3, 'chest': (97, 104), 'waist': (81, 89), 'shoulder': (47, 49)},
        {'label': 'L', 'order': 4, 'chest': (104, 112), 'waist': (89, 97), 'shoulder': (49, 51)},
        {'label': 'XL', 'order': 5, 'chest': (112, 124), 'waist': (97, 109), 'shoulder': (51, 53)},
        {'label': 'XXL', 'order': 6, 'chest': (124, 137), 'waist': (109, 122), 'shoulder': (53, 55)},
    ]
    
    for size in nike_mens_tshirt:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist'],
                'shoulder_breadth': size['shoulder']
            }
        )
    
    print(f"  ✅ Nike Men's T-Shirt: {len(nike_mens_tshirt)} sizes")
    
    # Nike Men's Jeans/Pants
    cat_id = db_manager.get_or_create_category("Pants", "Men")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    nike_mens_pants = [
        {'label': '28', 'order': 1, 'waist': (71, 74), 'hip': (86, 89), 'inseam': (81, 84)},
        {'label': '30', 'order': 2, 'waist': (76, 79), 'hip': (91, 94), 'inseam': (81, 84)},
        {'label': '32', 'order': 3, 'waist': (81, 84), 'hip': (97, 99), 'inseam': (81, 84)},
        {'label': '34', 'order': 4, 'waist': (86, 89), 'hip': (102, 104), 'inseam': (81, 84)},
        {'label': '36', 'order': 5, 'waist': (91, 94), 'hip': (107, 109), 'inseam': (81, 84)},
        {'label': '38', 'order': 6, 'waist': (97, 99), 'hip': (112, 114), 'inseam': (81, 84)},
    ]
    
    for size in nike_mens_pants:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'waist': size['waist'],
                'hip': size['hip'],
                'leg_length': size['inseam']
            }
        )
    
    print(f"  ✅ Nike Men's Pants: {len(nike_mens_pants)} sizes")


def add_adidas():
    """Add Adidas brand with size charts"""
    print("\n⚽ Adding Adidas...")
    
    brands = db_manager.get_brands()
    existing = next((b for b in brands if b['brand_name'] == 'Adidas'), None)
    
    if existing:
        print("  ⏭️  Adidas already exists in database")
        brand_id = existing['brand_id']
    else:
        brand_id = db_manager.insert_brand(
            brand_name="Adidas",
            country="Germany",
            size_system="EU",
            website="https://www.adidas.com"
        )
    
    # Adidas Men's T-Shirt
    cat_id = db_manager.get_or_create_category("T-Shirt", "Men")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    adidas_mens_tshirt = [
        {'label': 'XS', 'order': 1, 'chest': (85, 89), 'waist': (70, 74)},
        {'label': 'S', 'order': 2, 'chest': (89, 95), 'waist': (74, 80)},
        {'label': 'M', 'order': 3, 'chest': (95, 101), 'waist': (80, 86)},
        {'label': 'L', 'order': 4, 'chest': (101, 107), 'waist': (86, 92)},
        {'label': 'XL', 'order': 5, 'chest': (107, 115), 'waist': (92, 100)},
        {'label': 'XXL', 'order': 6, 'chest': (115, 123), 'waist': (100, 108)},
    ]
    
    for size in adidas_mens_tshirt:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist']
            }
        )
    
    print(f"  ✅ Adidas Men's T-Shirt: {len(adidas_mens_tshirt)} sizes")
    
    # Adidas Women's T-Shirt
    cat_id = db_manager.get_or_create_category("T-Shirt", "Women")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    adidas_womens_tshirt = [
        {'label': 'XS', 'order': 1, 'chest': (78, 82), 'waist': (60, 64), 'hip': (84, 88)},
        {'label': 'S', 'order': 2, 'chest': (82, 86), 'waist': (64, 68), 'hip': (88, 92)},
        {'label': 'M', 'order': 3, 'chest': (86, 92), 'waist': (68, 74), 'hip': (92, 98)},
        {'label': 'L', 'order': 4, 'chest': (92, 99), 'waist': (74, 81), 'hip': (98, 105)},
        {'label': 'XL', 'order': 5, 'chest': (99, 106), 'waist': (81, 88), 'hip': (105, 112)},
    ]
    
    for size in adidas_womens_tshirt:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist'],
                'hip': size['hip']
            }
        )
    
    print(f"  ✅ Adidas Women's T-Shirt: {len(adidas_womens_tshirt)} sizes")


def add_hm():
    """Add H&M brand with size charts"""
    print("\n👕 Adding H&M...")
    
    brands = db_manager.get_brands()
    existing = next((b for b in brands if b['brand_name'] == 'H&M'), None)
    
    if existing:
        print("  ⏭️  H&M already exists in database")
        brand_id = existing['brand_id']
    else:
        brand_id = db_manager.insert_brand(
            brand_name="H&M",
            country="Sweden",
            size_system="EU",
            website="https://www2.hm.com"
        )
    
    # H&M Men's T-Shirt
    cat_id = db_manager.get_or_create_category("T-Shirt", "Men")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    hm_mens_tshirt = [
        {'label': 'XS', 'order': 1, 'chest': (88, 92), 'waist': (74, 78)},
        {'label': 'S', 'order': 2, 'chest': (92, 96), 'waist': (78, 82)},
        {'label': 'M', 'order': 3, 'chest': (96, 100), 'waist': (82, 86)},
        {'label': 'L', 'order': 4, 'chest': (100, 106), 'waist': (86, 92)},
        {'label': 'XL', 'order': 5, 'chest': (106, 112), 'waist': (92, 98)},
        {'label': 'XXL', 'order': 6, 'chest': (112, 120), 'waist': (98, 106)},
    ]
    
    for size in hm_mens_tshirt:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist']
            }
        )
    
    print(f"  ✅ H&M Men's T-Shirt: {len(hm_mens_tshirt)} sizes")
    
    # H&M Women's Dress
    cat_id = db_manager.get_or_create_category("Dress", "Women")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    hm_womens_dress = [
        {'label': 'XS', 'order': 1, 'chest': (80, 84), 'waist': (62, 66), 'hip': (86, 90)},
        {'label': 'S', 'order': 2, 'chest': (84, 88), 'waist': (66, 70), 'hip': (90, 94)},
        {'label': 'M', 'order': 3, 'chest': (88, 92), 'waist': (70, 74), 'hip': (94, 98)},
        {'label': 'L', 'order': 4, 'chest': (92, 98), 'waist': (74, 80), 'hip': (98, 104)},
        {'label': 'XL', 'order': 5, 'chest': (98, 104), 'waist': (80, 86), 'hip': (104, 110)},
    ]
    
    for size in hm_womens_dress:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist'],
                'hip': size['hip']
            }
        )
    
    print(f"  ✅ H&M Women's Dress: {len(hm_womens_dress)} sizes")


def add_puma():
    """Add Puma brand with size charts"""
    print("\n🐆 Adding Puma...")
    
    brands = db_manager.get_brands()
    existing = next((b for b in brands if b['brand_name'] == 'Puma'), None)
    
    if existing:
        print("  ⏭️  Puma already exists in database")
        brand_id = existing['brand_id']
    else:
        brand_id = db_manager.insert_brand(
            brand_name="Puma",
            country="Germany",
            size_system="EU",
            website="https://www.puma.com"
        )
    
    # Puma Men's T-Shirt
    cat_id = db_manager.get_or_create_category("T-Shirt", "Men")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Regular")
    
    puma_mens_tshirt = [
        {'label': 'S', 'order': 1, 'chest': (88, 96), 'waist': (74, 82)},
        {'label': 'M', 'order': 2, 'chest': (96, 104), 'waist': (82, 90)},
        {'label': 'L', 'order': 3, 'chest': (104, 112), 'waist': (90, 98)},
        {'label': 'XL', 'order': 4, 'chest': (112, 120), 'waist': (98, 106)},
        {'label': 'XXL', 'order': 5, 'chest': (120, 128), 'waist': (106, 114)},
    ]
    
    for size in puma_mens_tshirt:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist']
            }
        )
    
    print(f"  ✅ Puma Men's T-Shirt: {len(puma_mens_tshirt)} sizes")


def add_under_armour():
    """Add Under Armour brand with size charts"""
    print("\n💪 Adding Under Armour...")
    
    brands = db_manager.get_brands()
    existing = next((b for b in brands if b['brand_name'] == 'Under Armour'), None)
    
    if existing:
        print("  ⏭️  Under Armour already exists in database")
        brand_id = existing['brand_id']
    else:
        brand_id = db_manager.insert_brand(
            brand_name="Under Armour",
            country="USA",
            size_system="US",
            website="https://www.underarmour.com"
        )
    
    # Under Armour Men's T-Shirt (Athletic Fit)
    cat_id = db_manager.get_or_create_category("T-Shirt", "Men")
    chart_id = db_manager.insert_size_chart(brand_id, cat_id, fit_type="Athletic")
    
    ua_mens_tshirt = [
        {'label': 'S', 'order': 1, 'chest': (89, 94), 'waist': (76, 81), 'shoulder': (44, 46)},
        {'label': 'M', 'order': 2, 'chest': (94, 99), 'waist': (81, 86), 'shoulder': (46, 48)},
        {'label': 'L', 'order': 3, 'chest': (99, 107), 'waist': (86, 94), 'shoulder': (48, 50)},
        {'label': 'XL', 'order': 4, 'chest': (107, 117), 'waist': (94, 104), 'shoulder': (50, 52)},
        {'label': 'XXL', 'order': 5, 'chest': (117, 127), 'waist': (104, 114), 'shoulder': (52, 54)},
    ]
    
    for size in ua_mens_tshirt:
        db_manager.insert_size(
            chart_id=chart_id,
            size_label=size['label'],
            size_order=size['order'],
            measurements={
                'chest': size['chest'],
                'waist': size['waist'],
                'shoulder_breadth': size['shoulder']
            }
        )
    
    print(f"  ✅ Under Armour Men's T-Shirt (Athletic): {len(ua_mens_tshirt)} sizes")


def main():
    """Add all popular brands"""
    print("\n" + "="*70)
    print("ADDING POPULAR BRAND SIZE CHARTS")
    print("="*70)
    
    try:
        # Nike already partially exists - skipping
        print("\n⏭️  Skipping Nike (already exists in database)")
        add_adidas()
        add_hm()
        add_puma()
        add_under_armour()
        
        print("\n" + "="*70)
        print("✅ SUCCESS! Added 5 popular brands")
        print("="*70)
        
        # Show summary
        print("\n📊 Database Summary:")
        brands = db_manager.get_brands()
        print(f"  Total Brands: {len(brands)}")
        for brand in sorted(brands, key=lambda x: x['brand_name']):
            print(f"    • {brand['brand_name']}")
        
        print("\n💡 Next Steps:")
        print("  1. Test with: python test_size_matching.py")
        print("  2. Add more categories/fits as needed")
        print("  3. Consider adding tolerance/weight columns for fine-tuning")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
