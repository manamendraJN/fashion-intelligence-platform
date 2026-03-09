import sqlite3

db_path = 'D:/Github-Projects-Research/fashion-intelligence-platform/backend/database/fashion_db.sqlite'
conn = sqlite3.connect(db_path)
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
