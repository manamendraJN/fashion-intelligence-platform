"""
Improve Database Schema - Add Tolerance and Weight Columns
This makes the algorithm more flexible and accurate
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import db_manager
import sqlite3


def add_missing_columns():
    """Add optimal, tolerance, and weight columns to sizes table"""
    print("\n" + "="*70)
    print("UPGRADING DATABASE SCHEMA")
    print("="*70 + "\n")
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Get existing columns
        cursor.execute("PRAGMA table_info(sizes)")
        existing_columns = [col['name'] for col in cursor.fetchall()]
        
        print("📋 Current columns in 'sizes' table:")
        print(f"  Total: {len(existing_columns)} columns\n")
        
        # Define columns to add
        measurement_types = ['chest', 'waist', 'hip', 'shoulder_breadth', 
                           'arm_length', 'leg_length', 'height']
        
        columns_to_add = []
        
        for mtype in measurement_types:
            # Optimal value columns
            optimal_col = f"{mtype}_optimal"
            if optimal_col not in existing_columns:
                columns_to_add.append((optimal_col, "REAL"))
            
            # Tolerance columns
            tolerance_col = f"{mtype}_tolerance"
            if tolerance_col not in existing_columns:
                columns_to_add.append((tolerance_col, "REAL DEFAULT 2.0"))
            
            # Weight columns
            weight_col = f"{mtype}_weight"
            if weight_col not in existing_columns:
                columns_to_add.append((weight_col, "REAL DEFAULT 1.0"))
        
        if not columns_to_add:
            print("✅ All columns already exist!")
            return
        
        print(f"📌 Adding {len(columns_to_add)} new columns:\n")
        
        # Add each column
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE sizes ADD COLUMN {col_name} {col_type}")
                print(f"  ✅ Added: {col_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column" in str(e).lower():
                    print(f"  ⏭️  Already exists: {col_name}")
                else:
                    raise
        
        print(f"\n✅ Schema upgrade complete!")
        
        # Now populate the new columns with smart defaults
        print("\n" + "-"*70)
        print("POPULATING DEFAULT VALUES")
        print("-"*70 + "\n")
        
        populate_default_values(cursor)
        
        conn.commit()
        
    print("\n" + "="*70)
    print("✅ DATABASE UPGRADE SUCCESSFUL")
    print("="*70 + "\n")


def populate_default_values(cursor):
    """Populate optimal, tolerance, and weight with smart defaults"""
    
    # Get all sizes
    cursor.execute("SELECT size_id, chart_id FROM sizes")
    sizes = cursor.fetchall()
    
    print(f"Updating {len(sizes)} sizes with default values...\n")
    
    measurement_types = ['chest', 'waist', 'hip', 'shoulder_breadth', 
                        'arm_length', 'leg_length', 'height']
    
    updated_count = 0
    
    for size in sizes:
        size_id = size['size_id']
        
        for mtype in measurement_types:
            min_col = f"{mtype}_min"
            max_col = f"{mtype}_max"
            optimal_col = f"{mtype}_optimal"
            tolerance_col = f"{mtype}_tolerance"
            weight_col = f"{mtype}_weight"
            
            # Get current values
            cursor.execute(f"""
                SELECT {min_col}, {max_col}, {optimal_col}, {tolerance_col}, {weight_col}
                FROM sizes WHERE size_id = ?
            """, (size_id,))
            
            row = cursor.fetchone()
            if not row:
                continue
            
            min_val = row[min_col]
            max_val = row[max_col]
            current_optimal = row[optimal_col] if optimal_col in row.keys() else None
            current_tolerance = row[tolerance_col] if tolerance_col in row.keys() else None
            current_weight = row[weight_col] if weight_col in row.keys() else None
            
            # Skip if no min/max data
            if min_val is None or max_val is None:
                continue
            
            updates = {}
            
            # Calculate optimal as midpoint if not set
            if current_optimal is None:
                updates[optimal_col] = (min_val + max_val) / 2
            
            # Set tolerance based on range width if not set
            if current_tolerance is None:
                range_width = max_val - min_val
                # Larger ranges get more tolerance
                if range_width <= 4:
                    tolerance = 2.0  # Tight fit garments
                elif range_width <= 8:
                    tolerance = 3.0  # Normal garments
                else:
                    tolerance = 4.0  # Loose fit garments
                updates[tolerance_col] = tolerance
            
            # Set default weight if not set
            if current_weight is None:
                # Default weight of 1.0, will be multiplied by category importance
                updates[weight_col] = 1.0
            
            # Update if there are changes
            if updates:
                update_sql = "UPDATE sizes SET " + ", ".join([f"{k} = ?" for k in updates.keys()])
                update_sql += " WHERE size_id = ?"
                cursor.execute(update_sql, list(updates.values()) + [size_id])
                updated_count += 1
    
    print(f"✅ Updated {updated_count} size entries with default values")


def verify_upgrade():
    """Verify the upgrade was successful"""
    print("\n" + "-"*70)
    print("VERIFICATION")
    print("-"*70 + "\n")
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check schema
        cursor.execute("PRAGMA table_info(sizes)")
        columns = cursor.fetchall()
        
        has_optimal = any('optimal' in col['name'] for col in columns)
        has_tolerance = any('tolerance' in col['name'] for col in columns)
        has_weight = any('weight' in col['name'] for col in columns)
        
        print("Schema Check:")
        print(f"  • Optimal columns: {'✅' if has_optimal else '❌'}")
        print(f"  • Tolerance columns: {'✅' if has_tolerance else '❌'}")
        print(f"  • Weight columns: {'✅' if has_weight else '❌'}")
        
        # Sample data check
        cursor.execute("""
            SELECT chest_min, chest_max, chest_optimal, chest_tolerance, chest_weight
            FROM sizes
            WHERE chest_min IS NOT NULL
            LIMIT 1
        """)
        
        sample = cursor.fetchone()
        if sample:
            print("\nSample Data:")
            print(f"  Chest range: {sample['chest_min']}-{sample['chest_max']} cm")
            if 'chest_optimal' in sample.keys():
                print(f"  Optimal: {sample['chest_optimal']} cm")
            if 'chest_tolerance' in sample.keys():
                print(f"  Tolerance: {sample['chest_tolerance']} cm")
            if 'chest_weight' in sample.keys():
                print(f"  Weight: {sample['chest_weight']}")


def update_db_manager():
    """Show how to update db_manager.py to use the new columns"""
    print("\n" + "="*70)
    print("NEXT STEP: UPDATE DB_MANAGER.PY")
    print("="*70 + "\n")
    
    print("The database now has optimal/tolerance/weight columns!")
    print("Update db_manager.py get_sizes_for_chart() method to use them:\n")
    
    print("""
# OLD CODE (lines ~270-275):
measurements.append({
    'type': mtype,
    'min': min_val,
    'max': max_val,
    'optimal': (min_val + max_val) / 2 if min_val and max_val else None,
    'tolerance': 2.0,  # Default tolerance
    'weight': 1.0      # Default weight
})

# NEW CODE:
optimal_key = f"{mtype}_optimal"
tolerance_key = f"{mtype}_tolerance"
weight_key = f"{mtype}_weight"

measurements.append({
    'type': mtype,
    'min': min_val,
    'max': max_val,
    'optimal': size_dict.get(optimal_key) or ((min_val + max_val) / 2 if min_val and max_val else None),
    'tolerance': size_dict.get(tolerance_key) or 2.0,
    'weight': size_dict.get(weight_key) or 1.0
})
""")
    
    print("\nThis change is OPTIONAL but recommended for more control.")


if __name__ == "__main__":
    try:
        add_missing_columns()
        verify_upgrade()
        update_db_manager()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
