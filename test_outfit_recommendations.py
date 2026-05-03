"""
Generate practical outfit recommendations from your actual wardrobe
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.color_utils import get_matching_colors, are_colors_compatible
from backend.database import get_connection
import json

def generate_outfit_recommendations():
    """Generate complete outfit recommendations from wardrobe"""
    print("👗 OUTFIT RECOMMENDATIONS FROM YOUR WARDROBE 👗")
    print("=" * 80)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all items
    cursor.execute('SELECT id, clothing_type, primary_color, all_colors FROM wardrobe_items ORDER BY primary_color')
    all_items = [dict(row) for row in cursor.fetchall()]
    
    # Organize by type
    tops = [i for i in all_items if 'Top' in i['clothing_type'] or 'Blouse' in i['clothing_type'] or 'Shirt' in i['clothing_type']]
    bottoms = [i for i in all_items if any(x in i['clothing_type'] for x in ['Bottom', 'Skirt', 'Jean', 'Trouser', 'Pant'])]
    dresses = [i for i in all_items if 'Dress' in i['clothing_type']]
    outerwear = [i for i in all_items if any(x in i['clothing_type'] for x in ['Jacket', 'Blazer', 'Cardigan', 'Coat'])]
    
    print(f"\n📊 Your Wardrobe:")
    print(f"  - Tops/Blouses: {len(tops)}")
    print(f"  - Bottoms: {len(bottoms)}")
    print(f"  - Dresses: {len(dresses)}")
    print(f"  - Outerwear: {len(outerwear)}")
    print(f"  - Total: {len(all_items)}")
    
    # Generate Top + Bottom combinations
    print("\n\n🎨 RECOMMENDED OUTFITS (Top + Bottom)")
    print("=" * 80)
    
    outfit_count = 0
    for top in tops[:10]:  # Test first 10 tops
        top_color = top['primary_color']
        matching_colors = get_matching_colors(top_color)
        
        # Find matching bottoms
        matches = []
        for bottom in bottoms:
            bottom_color = bottom['primary_color']
            if are_colors_compatible(top_color, bottom_color):
                matches.append(bottom)
        
        if matches:
            outfit_count += 1
            print(f"\n{outfit_count}. {top_color} {top['clothing_type']} (ID: {top['id']})")
            print(f"   Match with:")
            
            for match in matches[:3]:  # Show top 3 matches
                print(f"   ✓ {match['primary_color']} {match['clothing_type']} (ID: {match['id']})")
            
            if len(matches) > 3:
                print(f"   ... and {len(matches) - 3} more bottoms")
            
            print(f"   Total matches: {len(matches)}")
    
    # Generate Dress + Outerwear combinations
    if dresses and outerwear:
        print("\n\n👗 DRESS + OUTERWEAR COMBINATIONS")
        print("=" * 80)
        
        combo_count = 0
        for dress in dresses[:8]:  # Test first 8 dresses
            dress_color = dress['primary_color']
            
            # Find matching outerwear
            matches = []
            for outer in outerwear:
                outer_color = outer['primary_color']
                if are_colors_compatible(dress_color, outer_color):
                    matches.append(outer)
            
            if matches:
                combo_count += 1
                print(f"\n{combo_count}. {dress_color} {dress['clothing_type']} (ID: {dress['id']})")
                print(f"   Pair with:")
                
                for match in matches[:2]:
                    print(f"   ✓ {match['primary_color']} {match['clothing_type']} (ID: {match['id']})")
                
                if len(matches) > 2:
                    print(f"   ... and {len(matches) - 2} more options")
    
    # Color statistics
    print("\n\n📈 COLOR COMPATIBILITY MATRIX")
    print("=" * 80)
    
    # Get unique colors in wardrobe
    all_colors = list(set([item['primary_color'] for item in all_items if item['primary_color']]))
    all_colors.sort()
    
    print(f"\nYour wardrobe has {len(all_colors)} unique colors:")
    print(", ".join(all_colors))
    
    # Show top color combinations
    print("\n🌟 MOST VERSATILE COLORS IN YOUR WARDROBE:")
    color_match_counts = {}
    
    for color in all_colors:
        matching_colors = get_matching_colors(color)
        # Count how many of YOUR colors match this color
        your_matches = [c for c in all_colors if c.lower() in matching_colors]
        color_match_counts[color] = len(your_matches)
    
    # Sort by versatility
    sorted_colors = sorted(color_match_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (color, match_count) in enumerate(sorted_colors[:10], 1):
        item_count = len([item for item in all_items if item['primary_color'] == color])
        print(f"{i:2d}. {color:15s} - Matches {match_count:2d}/{len(all_colors)} of your colors ({item_count} items)")
    
    conn.close()

def show_color_pairing_tips():
    """Show practical color pairing tips"""
    print("\n\n💡 COLOR PAIRING TIPS")
    print("=" * 80)
    
    tips = [
        ("Safe Bet", "White, Black, Gray, Beige go with EVERYTHING"),
        ("Classic Combo", "Navy + White = timeless elegance"),
        ("Pastel Power", "Light Pink + Light Blue = soft sophistication"),
        ("Earth Tones", "Brown + Blue = casual elegance"),
        ("Bold Contrast", "Navy + Coral/Orange = modern chic"),
        ("Monochromatic", "Light Blue + Navy = coordinated style"),
        ("Complementary", "Blue + Orange OR Red + Green = eye-catching"),
        ("Warm + Cool", "Peach + Navy = balanced outfit"),
        ("Neutral Base", "Start with neutral bottom, add colorful top"),
        ("One Statement", "Bold color on one piece, neutral on other")
    ]
    
    for i, (tip_type, tip_text) in enumerate(tips, 1):
        print(f"{i:2d}. [{tip_type:15s}] {tip_text}")

if __name__ == "__main__":
    generate_outfit_recommendations()
    show_color_pairing_tips()
    
    print("\n\n" + "=" * 80)
    print("✅ COMPLETE! Use these combinations to create stylish outfits!")
    print("=" * 80)
