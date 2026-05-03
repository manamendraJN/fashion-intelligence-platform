"""
Database Diagnostic Tool
Checks for missing data: tolerance, optimal values, weights, and brand coverage
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager
import sqlite3

def diagnose_database():
    """Run comprehensive database diagnostics"""
    
    print("\n" + "="*70)
    print("DATABASE DIAGNOSTIC REPORT")
    print("="*70 + "\n")
    
    # Check brands
    print("📋 BRANDS IN DATABASE:")
    print("-" * 70)
    brands = db_manager.get_brands()
    if brands:
        for brand in brands:
            print(f"  • {brand['brand_name']} (ID: {brand['brand_id']})")
    else:
        print("  ❌ NO BRANDS FOUND!")
    print(f"\nTotal Brands: {len(brands)}\n")
    
    # Check categories
    print("📂 GARMENT CATEGORIES:")
    print("-" * 70)
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM garment_categories ORDER BY category_name")
        categories = cursor.fetchall()
        
        if categories:
            for cat in categories:
                print(f"  • {cat['category_name']} ({cat['gender']}) - ID: {cat['category_id']}")
        else:
            print("  ❌ NO CATEGORIES FOUND!")
    print(f"\nTotal Categories: {len(categories)}\n")
    
    # Check size charts
    print("📊 SIZE CHARTS:")
    print("-" * 70)
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sc.chart_id, b.brand_name, gc.category_name, gc.gender, sc.fit_type,
                   COUNT(s.size_id) as size_count
            FROM size_charts sc
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            LEFT JOIN sizes s ON sc.chart_id = s.chart_id
            GROUP BY sc.chart_id
        """)
        charts = cursor.fetchall()
        
        if charts:
            for chart in charts:
                print(f"  • Chart {chart['chart_id']}: {chart['brand_name']} - "
                      f"{chart['category_name']} ({chart['gender']}, {chart['fit_type']}) "
                      f"- {chart['size_count']} sizes")
        else:
            print("  ❌ NO SIZE CHARTS FOUND!")
    print(f"\nTotal Charts: {len(charts)}\n")
    
    # Check sizes and measurements
    print("📏 SIZE MEASUREMENT ANALYSIS:")
    print("-" * 70)
    
    issues = []
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check for sizes
        cursor.execute("SELECT COUNT(*) as count FROM sizes")
        size_count = cursor.fetchone()['count']
        print(f"Total Sizes: {size_count}")
        
        if size_count == 0:
            print("  ❌ NO SIZES IN DATABASE!\n")
            return
        
        # Check columns in sizes table
        cursor.execute("PRAGMA table_info(sizes)")
        columns = cursor.fetchall()
        column_names = [col['name'] for col in columns]
        
        print(f"\nColumns in sizes table: {len(column_names)}")
        
        # Check for optimal and tolerance columns
        has_optimal = any('optimal' in col for col in column_names)
        has_tolerance = any('tolerance' in col for col in column_names)
        has_weight = any('weight' in col for col in column_names)
        
        print(f"  • Has optimal columns: {'✅' if has_optimal else '❌'}")
        print(f"  • Has tolerance columns: {'✅' if has_tolerance else '❌'}")
        print(f"  • Has weight columns: {'✅' if has_weight else '❌'}")
        
        if not has_optimal:
            issues.append("Missing optimal value columns")
        if not has_tolerance:
            issues.append("Missing tolerance columns")
        if not has_weight:
            issues.append("Missing weight columns")
        
        # Sample some sizes to check data
        cursor.execute("""
            SELECT s.*, sc.chart_id, b.brand_name, gc.category_name
            FROM sizes s
            JOIN size_charts sc ON s.chart_id = sc.chart_id
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            LIMIT 5
        """)
        sample_sizes = cursor.fetchall()
        
        print("\n📋 SAMPLE SIZES (First 5):")
        print("-" * 70)
        for size in sample_sizes:
            print(f"\n  {size['brand_name']} - {size['category_name']} - {size['size_label']}")
            print(f"    Chart ID: {size['chart_id']}")
            print(f"    Chest: {size['chest_min']}-{size['chest_max']}")
            print(f"    Waist: {size['waist_min']}-{size['waist_max']}")
            
            # Check for optimal/tolerance/weight
            if has_optimal:
                chest_opt = size.get('chest_optimal', 'N/A')
                print(f"    Chest Optimal: {chest_opt}")
            if has_tolerance:
                chest_tol = size.get('chest_tolerance', 'N/A')
                print(f"    Chest Tolerance: {chest_tol}")
            if has_weight:
                chest_weight = size.get('chest_weight', 'N/A')
                print(f"    Chest Weight: {chest_weight}")
    
    # Check what the algorithm needs
    print("\n\n🔍 ALGORITHM REQUIREMENTS CHECK:")
    print("-" * 70)
    
    print("\nThe size_matching_service.py expects from get_sizes_for_chart():")
    print("  • measurements array with:")
    print("    - type (e.g., 'chest', 'waist')")
    print("    - min")
    print("    - max")
    print("    - optimal (can be None)")
    print("    - tolerance")
    print("    - weight")
    
    # Test actual output
    if charts:
        chart_id = charts[0]['chart_id']
        print(f"\n📊 Testing get_sizes_for_chart({chart_id}):")
        print("-" * 70)
        
        try:
            sizes = db_manager.get_sizes_for_chart(chart_id)
            if sizes:
                first_size = sizes[0]
                print(f"\nSize: {first_size.get('size_label', 'Unknown')}")
                print(f"Keys in response: {list(first_size.keys())}")
                
                if 'measurements' in first_size:
                    print(f"\nMeasurements found: {len(first_size['measurements'])}")
                    for meas in first_size['measurements']:
                        print(f"  • {meas.get('type', 'unknown')}: "
                              f"min={meas.get('min')}, max={meas.get('max')}, "
                              f"optimal={meas.get('optimal')}, "
                              f"tolerance={meas.get('tolerance')}, "
                              f"weight={meas.get('weight')}")
                else:
                    print("  ❌ NO 'measurements' KEY FOUND!")
                    issues.append("get_sizes_for_chart() doesn't return measurements array")
            else:
                print("  ❌ No sizes returned!")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            issues.append(f"Error calling get_sizes_for_chart: {str(e)}")
    
    # Summary
    print("\n\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if issues:
        print("\n❌ ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n💡 RECOMMENDED ACTIONS:")
        print("  1. Run fix_database_schema.py to add missing columns")
        print("  2. Run populate_size_charts.py to add brand data")
        print("  3. Verify db_manager.get_sizes_for_chart() returns correct format")
    else:
        print("\n✅ All checks passed!")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    diagnose_database()
