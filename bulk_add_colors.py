"""
Bulk Color Extraction for Existing Wardrobe Items
Adds color data to items that don't have it yet
"""

import sys
sys.path.append('backend')

import database
import sqlite3
import json
from pathlib import Path
from PIL import Image
from utils.color_utils import extract_dominant_color

# Database path
DB_PATH = Path('backend/fashion_wardrobe.db')
UPLOADS_DIR = Path('backend/uploads')

def update_item_colors(item_id, primary_color, color_rgb, all_colors):
    """Update color fields for a specific item"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE wardrobe_items 
        SET primary_color = ?, color_rgb = ?, all_colors = ?
        WHERE id = ?
    ''', (
        primary_color,
        json.dumps(color_rgb) if color_rgb else None,
        json.dumps(all_colors) if all_colors else None,
        item_id
    ))
    
    conn.commit()
    conn.close()

def process_items():
    """Process all items without color data"""
    
    items = database.get_all_wardrobe_items()
    
    # Filter items without color
    items_to_process = [item for item in items if not item.get('primaryColor')]
    
    print("=" * 60)
    print(f"BULK COLOR EXTRACTION")
    print("=" * 60)
    print(f"Total items: {len(items)}")
    print(f"Items needing colors: {len(items_to_process)}")
    print("=" * 60)
    
    if not items_to_process:
        print("\n✅ All items already have color data!")
        return
    
    proceed = input(f"\nExtract colors for {len(items_to_process)} items? (y/n): ")
    if proceed.lower() != 'y':
        print("Cancelled.")
        return
    
    print("\nProcessing items...\n")
    
    success_count = 0
    error_count = 0
    
    for i, item in enumerate(items_to_process, 1):
        try:
            # Get image path
            image_path = item['url'].replace('/uploads/', '')
            full_path = UPLOADS_DIR / image_path
            
            if not full_path.exists():
                print(f"✗ [{i}/{len(items_to_process)}] ID {item['id']}: Image not found - {image_path}")
                error_count += 1
                continue
            
            # Load image
            img = Image.open(full_path)
            
            # Extract color
            color_data = extract_dominant_color(img, n_colors=3)
            
            # Update database
            update_item_colors(
                item_id=item['id'],
                primary_color=color_data['primary_color'],
                color_rgb=color_data['rgb'],
                all_colors=color_data['all_colors']
            )
            
            print(f"✓ [{i}/{len(items_to_process)}] ID {item['id']:3d}: {item['type']:20s} → {color_data['primary_color']}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ [{i}/{len(items_to_process)}] ID {item['id']}: Error - {str(e)}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS:")
    print(f"  ✓ Success: {success_count}")
    print(f"  ✗ Errors:  {error_count}")
    print("=" * 60)
    
    if success_count > 0:
        print("\n✅ Colors extracted! Refresh your browser to see updates.")

if __name__ == "__main__":
    process_items()
