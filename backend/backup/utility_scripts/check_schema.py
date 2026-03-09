import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[2] / "database" / "fashion_db.sqlite"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get brands table schema
cursor.execute("PRAGMA table_info(brands)")
brands_schema = cursor.fetchall()

print("Brands table schema:")
for col in brands_schema:
    print(f"  {col[1]} ({col[2]})")

# Get garment_categories table schema
cursor.execute("PRAGMA table_info(garment_categories)")
categories_schema = cursor.fetchall()

print("\nGarment Categories table schema:")
for col in categories_schema:
    print(f"  {col[1]} ({col[2]})")

conn.close()
