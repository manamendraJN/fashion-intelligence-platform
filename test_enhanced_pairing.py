"""
Test enhanced color pairing with comprehensive fashion rules
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.color_utils import get_matching_colors, get_complementary_items
from backend.database import get_connection

def test_color_matches():
    """Test the enhanced color matching for various colors"""
    print("🎨 ENHANCED COLOR PAIRING TEST 🎨")
    print("=" * 80)
    
    # Test colors from your wardrobe
    test_colors = [
        "White", "Light Gray", "Peach", "Light Pink", "Brown",
        "Navy", "Light Blue", "Light Purple", "Dark Red"
    ]
    
    for color in test_colors:
        matches = get_matching_colors(color)
        print(f"\n{color.upper()} matches with:")
        print(f"  → {', '.join(matches[:10])}")  # Show first 10
        if len(matches) > 10:
            print(f"  → ... and {len(matches) - 10} more colors")
        print(f"  Total matches: {len(matches)}")

def test_pairing_examples():
    """Show real pairing examples from your database"""
    print("\n\n" + "=" * 80)
    print("🔗 REAL WARDROBE PAIRING EXAMPLES 🔗")
    print("=" * 80)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get sample items from each category
    categories = ['Top', 'Bottom', 'Outerwear', 'Dress']
    
    for category in categories:
        cursor.execute('''
            SELECT id, clothing_type, primary_color, all_colors
            FROM wardrobe_items 
            WHERE clothing_type LIKE ?
            LIMIT 3
        ''', (f'%{category}%',))
        
        items = cursor.fetchall()
        
        if items:
            print(f"\n📁 {category.upper()} CATEGORY:")
            print("-" * 80)
            
            for item in items:
                item_dict = dict(item)
                item_id = item_dict['id']
                item_type = item_dict['clothing_type']
                primary_color = item_dict['primary_color']
                
                print(f"\n  Item ID {item_id}: {primary_color} {item_type}")
                
                # Get complementary items
                complementary = get_complementary_items(item_type, primary_color)
                
                if complementary:
                    print(f"    ✓ Matching Types: {', '.join(complementary['matching_types'][:5])}")
                    print(f"    ✓ Matching Colors: {', '.join(complementary['matching_colors'][:8])}")
                    
                    # Check database for actual matches
                    matching_types_str = "', '".join(complementary['matching_types'])
                    matching_colors_str = "', '".join(complementary['matching_colors'])
                    
                    cursor.execute(f'''
                        SELECT COUNT(*) as count
                        FROM wardrobe_items 
                        WHERE id != ?
                        AND clothing_type IN ('{matching_types_str}')
                        AND primary_color IN ('{matching_colors_str}')
                    ''', (item_id,))
                    
                    match_count = cursor.fetchone()['count']
                    print(f"    📊 Found {match_count} matching items in your wardrobe")
    
    conn.close()

def test_fashion_color_theory():
    """Test color theory principles"""
    print("\n\n" + "=" * 80)
    print("🎭 FASHION COLOR THEORY VERIFICATION 🎭")
    print("=" * 80)
    
    # Test complementary colors
    print("\n1️⃣ COMPLEMENTARY COLORS (Color Wheel Opposites):")
    complementary_pairs = [
        ("Blue", "Orange"),
        ("Red", "Green"),
        ("Yellow", "Purple"),
        ("Navy", "Coral")
    ]
    
    for color1, color2 in complementary_pairs:
        matches1 = get_matching_colors(color1)
        matches2 = get_matching_colors(color2)
        check1 = "✓" if color2.lower() in matches1 else "✗"
        check2 = "✓" if color1.lower() in matches2 else "✗"
        print(f"  {check1} {color1} ↔ {color2} {check2}")
    
    # Test neutral versatility
    print("\n2️⃣ NEUTRAL VERSATILITY (Should match many colors):")
    neutrals = ["White", "Black", "Gray", "Beige"]
    
    for neutral in neutrals:
        matches = get_matching_colors(neutral)
        print(f"  {neutral}: {len(matches)} matching colors")
    
    # Test monochromatic families
    print("\n3️⃣ MONOCHROMATIC FAMILIES (Same color, different shades):")
    families = [
        ["Blue", "Light Blue", "Navy"],
        ["Red", "Light Pink", "Dark Red"],
        ["Green", "Light Green", "Dark Green"]
    ]
    
    for family in families:
        print(f"\n  {family[0]} Family:")
        for color in family:
            matches = get_matching_colors(color)
            family_matches = [c for c in family if c.lower() in matches and c.lower() != color.lower()]
            print(f"    {color} matches: {', '.join(family_matches) if family_matches else 'None'}")

if __name__ == "__main__":
    test_color_matches()
    test_pairing_examples()
    test_fashion_color_theory()
    
    print("\n\n" + "=" * 80)
    print("✅ ENHANCED COLOR PAIRING TEST COMPLETE!")
    print("=" * 80)
