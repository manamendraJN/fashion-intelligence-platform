import sqlite3
import json

conn = sqlite3.connect('backend/fashion_wardrobe.db')
cursor = conn.cursor()

# Find all skirt items
cursor.execute("SELECT id, clothing_type FROM wardrobe_items WHERE clothing_type LIKE '%kirt%'")
skirts = cursor.fetchall()

print(f"\n{'='*60}")
print(f"Found {len(skirts)} skirt items in database:")
print(f"{'='*60}")

for skirt_id, clothing_type in skirts[:20]:
    print(f"  ID {skirt_id}: {clothing_type}")

# Check if any pencil skirts exist
cursor.execute("SELECT COUNT(*) FROM wardrobe_items WHERE clothing_type LIKE '%Pencil%'")
pencil_count = cursor.fetchone()[0]
print(f"\n{'='*60}")
print(f"Pencil Skirts specifically: {pencil_count}")
print(f"{'='*60}\n")

conn.close()
