"""
Re-extract colors with enhanced light color detection
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

print("=" * 70)
print(f"RE-EXTRACTING COLORS WITH LIGHT COLOR DETECTION ({len(items)} items)")
print("=" * 70)

success = 0
errors = 0
by_color = {}
color_changes = []

for i, item in enumerate(items, 1):
    try:
        image_path = item['url'].replace('/uploads/', '')
        full_path = UPLOADS_DIR / image_path
        
        if not full_path.exists():
            errors += 1
            if i % 10 == 0:
                print(f"[{i}/{len(items)}] Processed... ({success} ✓, {errors} ✗)")
            continue
        
        img = Image.open(full_path)
        color_data = extract_dominant_color(img, n_colors=3)
        
        old_color = item.get('primaryColor', 'None')
        new_color = color_data['primary_color']
        
        update_item_colors(
            item_id=item['id'],
            primary_color=new_color,
            color_rgb=color_data['rgb'],
            all_colors=color_data['all_colors']
        )
        
        success += 1
        by_color[new_color] = by_color.get(new_color, 0) + 1
        
        # Track color changes
        if old_color != new_color and old_color != 'None':
            color_changes.append((item['id'], item['type'], old_color, new_color))
        
        if i % 10 == 0 or i == len(items):
            print(f"[{i}/{len(items)}] Processed... ({success} ✓, {errors} ✗)")
        
    except Exception as e:
        errors += 1
        if i % 10 == 0:
            print(f"[{i}/{len(items)}] Processed... ({success} ✓, {errors} ✗)")

print("\n" + "=" * 70)
print(f"COMPLETE!")
print(f"  ✓ Success: {success}")
print(f"  ✗ Errors:  {errors}")

print("\n📊 New Color Distribution:")
for color, count in sorted(by_color.items(), key=lambda x: x[1], reverse=True):
    print(f"  {color:20s}: {count:3d} items")

if color_changes:
    print(f"\n🎨 Color Changes Detected ({len(color_changes)} items):")
    for item_id, item_type, old, new in color_changes[:10]:
        print(f"  ID {item_id:3d} {item_type:15s}: {old:15s} → {new}")
    if len(color_changes) > 10:
        print(f"  ... and {len(color_changes) - 10} more")

print("\n" + "=" * 70)
print("✅ Enhanced color detection complete!")
print("   Now detects: Light Blue, Light Purple, Light Pink, Light Green,")
print("                Peach, Light Yellow, Navy, Dark colors, etc.")
print("=" * 70)
