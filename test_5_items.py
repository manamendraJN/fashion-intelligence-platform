"""
Test color extraction on first 5 items (demo)
"""

import sys
sys.path.append('backend')

import database
import sqlite3
import json
from pathlib import Path
from PIL import Image
from utils.color_utils import extract_dominant_color

DB_PATH = Path('backend/fashion_wardrobe.db')
UPLOADS_DIR = Path('backend/uploads')

def update_item_colors(item_id, primary_color, color_rgb, all_colors):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE wardrobe_items 
        SET primary_color = ?, color_rgb = ?, all_colors = ?
        WHERE id = ?
    ''', (primary_color, json.dumps(color_rgb), json.dumps(all_colors), item_id))
    conn.commit()
    conn.close()

items = database.get_all_wardrobe_items()
items_to_process = [item for item in items if not item.get('primaryColor')][:5]

print("=" * 60)
print(f"TESTING COLOR EXTRACTION (First 5 items)")
print("=" * 60)

for i, item in enumerate(items_to_process, 1):
    try:
        image_path = item['url'].replace('/uploads/', '')
        full_path = UPLOADS_DIR / image_path
        
        if not full_path.exists():
            print(f"✗ [{i}/5] ID {item['id']}: Image not found")
            continue
        
        img = Image.open(full_path)
        color_data = extract_dominant_color(img, n_colors=3)
        
        update_item_colors(
            item_id=item['id'],
            primary_color=color_data['primary_color'],
            color_rgb=color_data['rgb'],
            all_colors=color_data['all_colors']
        )
        
        print(f"✓ [{i}/5] ID {item['id']:3d}: {item['type']:15s} → {color_data['primary_color']}")
        
    except Exception as e:
        print(f"✗ [{i}/5] ID {item['id']}: {str(e)}")

print("=" * 60)
print("✅ Test complete! Check results with: python check_colors.py")
