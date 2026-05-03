"""Add new garment categories to the database"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager

def add_new_categories():
    """Add new garment categories"""
    
    print("\n" + "="*70)
    print("ADDING NEW GARMENT CATEGORIES")
    print("="*70)
    
    new_categories = [
        ('Jacket', 'Men'),
        ('Jacket', 'Women'),
        ('Hoodie', 'Men'),
        ('Hoodie', 'Women'),
        ('Shorts', 'Men'),
        ('Shorts', 'Women'),
        ('Skirt', 'Women'),
        ('Polo', 'Men'),
        ('Sweater', 'Men'),
        ('Sweater', 'Women'),
    ]
    
    added = 0
    skipped = 0
    
    for category_name, gender in new_categories:
        try:
            # Check if category already exists
            categories = db_manager.get_categories()
            exists = any(c['category_name'] == category_name and c['gender'] == gender for c in categories)
            
            if exists:
                print(f"⏭️  {category_name} ({gender}) - Already exists")
                skipped += 1
            else:
                cat_id = db_manager.get_or_create_category(category_name, gender)
                print(f"✅ {category_name} ({gender}) - Added (ID: {cat_id})")
                added += 1
        except Exception as e:
            print(f"❌ {category_name} ({gender}) - Error: {e}")
    
    print("\n" + "="*70)
    print(f"✅ Added: {added} new categories")
    print(f"⏭️  Skipped: {skipped} (already existed)")
    print("="*70)
    
    # Show all categories
    print("\n📂 All Categories in Database:")
    print("-" * 70)
    categories = db_manager.get_categories()
    for cat in sorted(categories, key=lambda c: (c['gender'], c['category_name'])):
        print(f"   • {cat['category_name']} ({cat['gender']}) - ID: {cat['category_id']}")
    
    print(f"\nTotal categories: {len(categories)}")


if __name__ == "__main__":
    add_new_categories()
