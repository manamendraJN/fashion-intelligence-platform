"""Check size chart coverage across brands and categories"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager

def check_coverage():
    """Check which brand/category combinations have size charts"""
    
    brands = db_manager.get_brands()
    categories = db_manager.get_categories()
    
    print("\n" + "="*70)
    print("SIZE CHART COVERAGE ANALYSIS")
    print("="*70)
    
    print(f"\n📋 Total Brands: {len(brands)}")
    for brand in brands:
        print(f"   • {brand['brand_name']}")
    
    print(f"\n📂 Total Categories: {len(categories)}")
    for cat in categories:
        print(f"   • {cat['category_name']} ({cat['gender']})")
    
    print("\n📊 Coverage Matrix:")
    print("-" * 70)
    
    # Create coverage matrix
    coverage = {}
    for brand in brands:
        coverage[brand['brand_name']] = {}
        for cat in categories:
            cat_key = f"{cat['category_name']} ({cat['gender']})"
            # Check if size chart exists
            with db_manager.get_connection() as conn:
                charts = conn.execute(
                    "SELECT chart_id FROM size_charts WHERE brand_id=? AND category_id=?",
                    (brand['brand_id'], cat['category_id'])
                ).fetchall()
            coverage[brand['brand_name']][cat_key] = len(charts) > 0
    
    # Print matrix
    print(f"\n{'Brand':<15} ", end='')
    for cat in categories:
        cat_short = f"{cat['category_name'][0]}{cat['gender'][0]}"
        print(f"{cat_short:>4}", end=' ')
    print()
    print("-" * 70)
    
    for brand_name in sorted(coverage.keys()):
        print(f"{brand_name:<15} ", end='')
        for cat in categories:
            cat_key = f"{cat['category_name']} ({cat['gender']})"
            has_chart = coverage[brand_name][cat_key]
            symbol = "✓" if has_chart else "✗"
            print(f"{symbol:>4}", end=' ')
        print()
    
    # Calculate statistics
    total_combinations = len(brands) * len(categories)
    filled = sum(1 for brand in coverage.values() for has_chart in brand.values() if has_chart)
    missing = total_combinations - filled
    
    print("\n" + "="*70)
    print(f"📊 Coverage: {filled}/{total_combinations} ({filled*100//total_combinations}%)")
    print(f"❌ Missing: {missing} brand/category combinations")
    print("="*70)
    
    # List missing combinations
    if missing > 0:
        print("\n❌ Missing Size Charts:")
        print("-" * 70)
        for brand_name in sorted(coverage.keys()):
            missing_cats = [cat for cat, has in coverage[brand_name].items() if not has]
            if missing_cats:
                print(f"\n{brand_name}:")
                for cat in missing_cats:
                    print(f"   • {cat}")

if __name__ == "__main__":
    check_coverage()
