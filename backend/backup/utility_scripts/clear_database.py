"""
Clear all data from the database while preserving the schema
"""
import sqlite3
import sys

db_path = 'D:/Github-Projects-Research/fashion-intelligence-platform/backend/database/fashion_db.sqlite'

def clear_database():
    """Delete all data from all tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("CLEARING DATABASE")
    print("="*80 + "\n")
    
    try:
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print("Tables to clear:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} rows")
        
        print("\n" + "-"*80)
        response = input("\nAre you sure you want to delete ALL data? (yes/no): ")
        
        if response.lower() != 'yes':
            print("\n❌ Operation cancelled")
            return
        
        print("\nDeleting data...")
        
        # Delete from all tables in correct order (respecting foreign keys)
        delete_order = [
            'sizes',
            'size_charts',
            'user_measurements',
            'garment_categories',
            'brands'
        ]
        
        for table in delete_order:
            if table in tables:
                cursor.execute(f"DELETE FROM {table}")
                print(f"  ✓ Cleared {table}")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        print(f"  ✓ Reset auto-increment counters")
        
        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        conn.commit()
        
        print("\n" + "="*80)
        print("✅ DATABASE CLEARED SUCCESSFULLY")
        print("="*80)
        
        # Show final state
        print("\nFinal state:")
        for table in tables:
            if table != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  - {table}: {count} rows")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    clear_database()
