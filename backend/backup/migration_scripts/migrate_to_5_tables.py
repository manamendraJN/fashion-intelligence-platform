"""
Migration Script: 8-Table Schema → 5-Table Simplified Schema
==============================================================

This script migrates your database from the complex 8-table schema
to the simplified 5-table schema.

WHAT CHANGES:
  ✅ brands → copied as-is
  ✅ garment_categories → copied as-is  
  ✅ size_charts → copied as-is
  ✅ user_measurements → copied as-is
  🔄 sizes + size_measurements → merged into new denormalized sizes table
  ❌ category_measurements → removed (not needed)
  ❌ recommendation_log → removed (optional analytics table)

BEFORE RUNNING:
  - Backup your current database (automatic backup created)
  - Close any other database connections
  - Expected time: < 5 seconds

AFTER RUNNING:
  - New database: fashion_db_simplified.sqlite
  - Backup: fashion_db_backup_TIMESTAMP.sqlite
  - Old database: fashion_db.sqlite (unchanged)
"""

import sqlite3
import shutil
import os
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def backup_database(db_path):
    """Create a timestamped backup of the current database"""
    if not os.path.exists(db_path):
        print(f"⚠️  Database not found: {db_path}")
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = db_path.replace('.sqlite', f'_backup_{timestamp}.sqlite')
    shutil.copy2(db_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path

def create_new_database(new_db_path, schema_path):
    """Create new database with simplified schema"""
    # Remove if exists
    if os.path.exists(new_db_path):
        os.remove(new_db_path)
    
    # Create new database
    conn = sqlite3.connect(new_db_path)
    
    # Load and execute schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    
    print(f"✅ New database created: {new_db_path}")

def migrate_data(old_db_path, new_db_path):
    """Migrate data from old database to new database"""
    
    old_conn = sqlite3.connect(old_db_path)
    old_conn.row_factory = sqlite3.Row
    new_conn = sqlite3.connect(new_db_path)
    
    print("\n" + "="*70)
    print("MIGRATING DATA")
    print("="*70)
    
    try:
        # 1. Migrate brands (no changes)
        print("\n1️⃣  Migrating BRANDS...")
        old_cursor = old_conn.cursor()
        old_cursor.execute("SELECT * FROM brands")
        brands = old_cursor.fetchall()
        
        new_cursor = new_conn.cursor()
        for brand in brands:
            new_cursor.execute("""
                INSERT INTO brands (brand_id, brand_name, brand_country, size_system, 
                                   website_url, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (brand['brand_id'], brand['brand_name'], brand['brand_country'],
                  brand['size_system'], brand['website_url'], brand['notes'],
                  brand['created_at'], brand['updated_at']))
        new_conn.commit()
        print(f"   ✅ Migrated {len(brands)} brands")
        
        # 2. Migrate garment_categories (no changes)
        print("\n2️⃣  Migrating GARMENT CATEGORIES...")
        old_cursor.execute("SELECT * FROM garment_categories")
        categories = old_cursor.fetchall()
        
        for cat in categories:
            new_cursor.execute("""
                INSERT INTO garment_categories (category_id, category_name, gender, 
                                               description, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (cat['category_id'], cat['category_name'], cat['gender'],
                  cat['description'], cat['created_at']))
        new_conn.commit()
        print(f"   ✅ Migrated {len(categories)} categories")
        
        # 3. Migrate size_charts (no changes)
        print("\n3️⃣  Migrating SIZE CHARTS...")
        old_cursor.execute("SELECT * FROM size_charts")
        charts = old_cursor.fetchall()
        
        for chart in charts:
            new_cursor.execute("""
                INSERT INTO size_charts (chart_id, brand_id, category_id, chart_name,
                                        fit_type, notes, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (chart['chart_id'], chart['brand_id'], chart['category_id'],
                  chart['chart_name'], chart['fit_type'], chart['notes'],
                  chart['is_active'], chart['created_at'], chart['updated_at']))
        new_conn.commit()
        print(f"   ✅ Migrated {len(charts)} size charts")
        
        # 4. Migrate sizes + size_measurements (TRANSFORMATION)
        print("\n4️⃣  Migrating SIZES (merging with measurements)...")
        old_cursor.execute("SELECT * FROM sizes")
        sizes = old_cursor.fetchall()
        
        migrated_count = 0
        for size in sizes:
            size_id = size['size_id']
            
            # Get all measurements for this size
            old_cursor.execute("""
                SELECT measurement_type, min_value, max_value
                FROM size_measurements
                WHERE size_id = ?
            """, (size_id,))
            measurements = old_cursor.fetchall()
            
            # Build measurement dictionary
            meas_dict = {}
            for m in measurements:
                meas_type = m['measurement_type']
                meas_dict[f"{meas_type}_min"] = m['min_value']
                meas_dict[f"{meas_type}_max"] = m['max_value']
            
            # Insert into new sizes table with denormalized measurements
            new_cursor.execute("""
                INSERT INTO sizes (
                    size_id, chart_id, size_label, size_order,
                    chest_min, chest_max,
                    waist_min, waist_max,
                    hip_min, hip_max,
                    shoulder_breadth_min, shoulder_breadth_max,
                    arm_length_min, arm_length_max,
                    bicep_min, bicep_max,
                    leg_length_min, leg_length_max,
                    thigh_min, thigh_max,
                    height_min, height_max,
                    notes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                size_id, size['chart_id'], size['size_label'], size['size_order'],
                meas_dict.get('chest_min'), meas_dict.get('chest_max'),
                meas_dict.get('waist_min'), meas_dict.get('waist_max'),
                meas_dict.get('hip_min'), meas_dict.get('hip_max'),
                meas_dict.get('shoulder_breadth_min'), meas_dict.get('shoulder_breadth_max'),
                meas_dict.get('arm_length_min'), meas_dict.get('arm_length_max'),
                meas_dict.get('bicep_min'), meas_dict.get('bicep_max'),
                meas_dict.get('leg_length_min'), meas_dict.get('leg_length_max'),
                meas_dict.get('thigh_min'), meas_dict.get('thigh_max'),
                meas_dict.get('height_min'), meas_dict.get('height_max'),
                None,  # notes
                size['created_at']
            ))
            migrated_count += 1
        
        new_conn.commit()
        print(f"   ✅ Migrated {migrated_count} sizes with measurements merged")
        
        # 5. Migrate user_measurements (no changes)
        print("\n5️⃣  Migrating USER MEASUREMENTS...")
        old_cursor.execute("SELECT * FROM user_measurements")
        users = old_cursor.fetchall()
        
        for user in users:
            new_cursor.execute("""
                INSERT INTO user_measurements (
                    user_id, user_identifier, height, chest, waist, hip,
                    shoulder_breadth, shoulder_to_crotch, arm_length,
                    bicep, forearm, wrist, leg_length, thigh, calf, ankle,
                    gender, unit, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user['user_id'], user['user_identifier'],
                user['height'], user['chest'], user['waist'], user['hip'],
                user['shoulder_breadth'], user['shoulder_to_crotch'], user['arm_length'],
                user['bicep'], user['forearm'], user['wrist'],
                user['leg_length'], user['thigh'], user['calf'], user['ankle'],
                user['gender'], user['unit'], user['created_at'], user['updated_at']
            ))
        new_conn.commit()
        print(f"   ✅ Migrated {len(users)} user measurement records")
        
        print("\n" + "="*70)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        new_conn.rollback()
        raise
    finally:
        old_conn.close()
        new_conn.close()

def verify_migration(new_db_path):
    """Verify the migrated database"""
    print("\n" + "="*70)
    print("VERIFYING MIGRATION")
    print("="*70)
    
    conn = sqlite3.connect(new_db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]
    print(f"\n📋 Tables in new database ({len(tables)}):")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   ✅ {table}: {count} records")
    
    # Sample query
    print("\n🔍 Sample query (first 3 sizes with measurements):")
    cursor.execute("""
        SELECT s.size_label, b.brand_name, gc.category_name,
               s.chest_min, s.chest_max, s.waist_min, s.waist_max
        FROM sizes s
        JOIN size_charts sc ON s.chart_id = sc.chart_id
        JOIN brands b ON sc.brand_id = b.brand_id
        JOIN garment_categories gc ON sc.category_id = gc.category_id
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"   {row[1]} {row[2]} Size {row[0]}: chest {row[3]}-{row[4]}cm, waist {row[5]}-{row[6]}cm")
    
    conn.close()
    
    print("\n" + "="*70)
    print("✅ VERIFICATION COMPLETED")
    print("="*70)

def main():
    print("\n" + "="*70)
    print("DATABASE MIGRATION: 8 TABLES → 5 TABLES (SIMPLIFIED)")
    print("="*70)
    
    # Paths
    backend_dir = Path(__file__).parent
    db_dir = backend_dir / "database"
    
    old_db_path = db_dir / "fashion_db.sqlite"
    new_db_path = db_dir / "fashion_db_simplified.sqlite"
    schema_path = db_dir / "schema_simplified.sql"
    
    # Check if old database exists
    if not old_db_path.exists():
        print(f"\n❌ Old database not found: {old_db_path}")
        print("   Nothing to migrate. Create new database using schema_simplified.sql")
        return
    
    # Check if schema exists
    if not schema_path.exists():
        print(f"\n❌ Schema file not found: {schema_path}")
        return
    
    print(f"\nOld database: {old_db_path}")
    print(f"New database: {new_db_path}")
    print(f"Schema file:  {schema_path}")
    
    # Confirm
    print("\n⚠️  This will create a NEW simplified database.")
    print("   Your original database will NOT be modified.")
    response = input("\n   Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("\n❌ Migration cancelled.")
        return
    
    # Step 1: Backup
    print("\n" + "="*70)
    print("STEP 1: BACKING UP DATABASE")
    print("="*70)
    backup_path = backup_database(str(old_db_path))
    if not backup_path:
        print("❌ Backup failed. Aborting migration.")
        return
    
    # Step 2: Create new database
    print("\n" + "="*70)
    print("STEP 2: CREATING NEW DATABASE")
    print("="*70)
    create_new_database(str(new_db_path), str(schema_path))
    
    # Step 3: Migrate data
    print("\n" + "="*70)
    print("STEP 3: MIGRATING DATA")
    print("="*70)
    migrate_data(str(old_db_path), str(new_db_path))
    
    # Step 4: Verify
    verify_migration(str(new_db_path))
    
    # Final instructions
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
✅ Migration completed successfully!

To use the new simplified database:

1. OPTION A: Replace old database (recommended)
   - Close all applications using the database
   - Backup: mv database/fashion_db.sqlite database/fashion_db_old.sqlite
   - Rename:  mv database/fashion_db_simplified.sqlite database/fashion_db.sqlite
   - Restart your application

2. OPTION B: Update configuration
   - Update DatabaseManager to use 'fashion_db_simplified.sqlite'
   - Restart your application

3. Test the application
   - python test_sizing_systems.py
   - python diagnose_database.py

Your data is safe:
   - Original: database/fashion_db.sqlite (unchanged)
   - Backup:   """ + (backup_path if backup_path else "N/A") + """
   - New:      database/fashion_db_simplified.sqlite

Table count reduced: 8 tables → 5 tables ✅
""")
    print("="*70)

if __name__ == "__main__":
    main()
