"""
Auto-process ALL items without color data
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
items_to_process = [item for item in items if not item.get('primaryColor')]

print("=" * 70)
print(f"AUTO-PROCESSING COLOR EXTRACTION FOR {len(items_to_process)} ITEMS")
print("=" * 70)

success = 0
errors = 0
by_color = {}

for i, item in enumerate(items_to_process, 1):
    try:
        image_path = item['url'].replace('/uploads/', '')
        full_path = UPLOADS_DIR / image_path
        
        if not full_path.exists():
            errors += 1
            if i % 10 == 0:
                print(f"[{i}/{len(items_to_process)}] Processed... ({success} ✓, {errors} ✗)")
            continue
        
        img = Image.open(full_path)
        color_data = extract_dominant_color(img, n_colors=3)
        
        update_item_colors(
            item_id=item['id'],
            primary_color=color_data['primary_color'],
            color_rgb=color_data['rgb'],
            all_colors=color_data['all_colors']
        )
        
        success += 1
        color = color_data['primary_color']
        by_color[color] = by_color.get(color, 0) + 1
        
        if i % 10 == 0 or i == len(items_to_process):
            print(f"[{i}/{len(items_to_process)}] Processed... ({success} ✓, {errors} ✗)")
        
    except Exception as e:
        errors += 1
        if i % 10 == 0:
            print(f"[{i}/{len(items_to_process)}] Processed... ({success} ✓, {errors} ✗)")

print("\n" + "=" * 70)
print(f"COMPLETE!")
print(f"  ✓ Success: {success}")
print(f"  ✗ Errors:  {errors}")
print("\nColor Distribution:")
for color, count in sorted(by_color.items(), key=lambda x: x[1], reverse=True):
    print(f"  {color:15s}: {count:3d} items")
print("=" * 70)
print("\n✅ All colors extracted! Refresh your browser to see the updates.")
