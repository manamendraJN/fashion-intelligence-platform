"""
Interactive database query tool
Quickly run custom queries on the database
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import db_manager


def run_query(query: str):
    """Execute a query and display results"""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Get results
        results = cursor.fetchall()
        
        if not results:
            print("No results found.")
            return
        
        # Print header
        header = " | ".join(f"{col:15s}" for col in columns)
        print("\n" + header)
        print("-" * len(header))
        
        # Print rows
        for row in results:
            row_dict = dict(row)
            values = [str(row_dict[col])[:15] for col in columns]
            print(" | ".join(f"{val:15s}" for val in values))
        
        print(f"\nTotal: {len(results)} rows\n")


if __name__ == "__main__":
    print("="*80)
    print("DATABASE QUERY TOOL")
    print("="*80)
    print("\nUseful queries:")
    print("  1. View all brands")
    print("  2. View all categories") 
    print("  3. View all size charts")
    print("  4. Nike size chart details")
    print("  5. Custom query")
    print("  6. Exit")
    
    queries = {
        "1": "SELECT * FROM brands ORDER BY brand_name",
        "2": "SELECT * FROM garment_categories ORDER BY category_name",
        "3": """
            SELECT sc.chart_id, b.brand_name, gc.category_name, gc.gender, 
                   COUNT(s.size_id) as num_sizes
            FROM size_charts sc
            JOIN brands b ON sc.brand_id = b.brand_id
            JOIN garment_categories gc ON sc.category_id = gc.category_id
            LEFT JOIN sizes s ON sc.chart_id = s.chart_id
            GROUP BY sc.chart_id
        """,
        "4": """
            SELECT s.size_label, sm.measurement_type, sm.min_value, 
                   sm.max_value, sm.optimal_value
            FROM sizes s
            JOIN size_measurements sm ON s.size_id = sm.size_id
            JOIN size_charts sc ON s.chart_id = sc.chart_id
            JOIN brands b ON sc.brand_id = b.brand_id
            WHERE b.brand_name = 'Nike'
            ORDER BY s.size_order, sm.measurement_type
        """
    }
    
    while True:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "6":
            print("Goodbye!")
            break
        
        if choice == "5":
            custom_query = input("Enter SQL query: ")
            try:
                run_query(custom_query)
            except Exception as e:
                print(f"Error: {e}")
        elif choice in queries:
            run_query(queries[choice])
        else:
            print("Invalid choice. Try again.")
