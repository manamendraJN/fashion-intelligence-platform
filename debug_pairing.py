"""
Debug script - Check why pairing returns 0 items
"""
import sys
sys.path.append('backend')

from utils.color_utils import get_event_based_pairing
import database

def debug_pairing():
    """Debug the pairing issue"""
    
    print("\n" + "="*80)
    print("🔍 DEBUGGING PAIRING ISSUE")
    print("="*80)
    
    # Get all wardrobe items
    items = database.get_all_wardrobe_items()
    print(f"\n📊 Total items in database: {len(items)}")
    
    # Find a pencil skirt
    pencil_skirts = [item for item in items if 'pencil' in item['type'].lower()]
    
    if not pencil_skirts:
        print("\n❌ No pencil skirts found in database!")
        return
    
    pencil_skirt = pencil_skirts[0]
    print(f"\n👗 Testing with: {pencil_skirt['type']} (ID: {pencil_skirt['id']})")
    print(f"   Color: {pencil_skirt.get('primaryColor', 'Unknown')}")
    
    # Test Office pairing
    print(f"\n{'─'*80}")
    print("TEST 1: Office Event Context")
    print(f"{'─'*80}")
    
    pairing = get_event_based_pairing(
        pencil_skirt['type'], 
        pencil_skirt.get('primaryColor', 'Black'), 
        'Office'
    )
    
    print(f"\n✅ Recommended Types:")
    for t in pairing['matching_types']:
        print(f"   • {t}")
    
    print(f"\n❌ Avoid Types:")
    for t in pairing.get('avoid_types', []):
        print(f"   • {t}")
    
    print(f"\n🎨 Matching Colors:")
    for c in pairing['matching_colors'][:10]:
        print(f"   • {c}")
    
    # Check if we have any items that match the types
    print(f"\n{'─'*80}")
    print("Checking Database for Matching Items...")
    print(f"{'─'*80}")
    
    matching_types = pairing['matching_types']
    matching_colors = [c.lower() for c in pairing['matching_colors']]
    
    type_matches = []
    color_matches = []
    both_matches = []
    
    for item in items:
        if item['id'] == pencil_skirt['id']:
            continue  # Skip the item itself
        
        item_type = item['type']
        item_color = (item.get('primaryColor') or '').lower()
        
        type_match = any(mt.lower() in item_type.lower() for mt in matching_types)
        color_match = item_color in matching_colors
        
        if type_match and color_match:
            both_matches.append(item)
        elif type_match:
            type_matches.append(item)
        elif color_match:
            color_matches.append(item)
    
    print(f"\n✅ Items matching BOTH type AND color: {len(both_matches)}")
    for item in both_matches[:5]:
        print(f"   • {item['type']} - {item.get('primaryColor', 'Unknown')}")
    
    print(f"\n⚠️  Items matching TYPE only: {len(type_matches)}")
    for item in type_matches[:5]:
        print(f"   • {item['type']} - {item.get('primaryColor', 'Unknown')}")
    
    print(f"\n⚠️  Items matching COLOR only: {len(color_matches)}")
    for item in color_matches[:5]:
        print(f"   • {item['type']} - {item.get('primaryColor', 'Unknown')}")
    
    # Test what the database query returns
    print(f"\n{'─'*80}")
    print("TEST 2: Actual Database Query")
    print(f"{'─'*80}")
    
    db_matches = database.get_matching_items(
        pencil_skirt['id'], 
        matching_types, 
        matching_colors
    )
    
    print(f"\n📊 Database returned: {len(db_matches)} matches")
    for match in db_matches[:10]:
        print(f"   • {match['type']} - {match.get('primaryColor', 'Unknown')} - Reason: {match.get('matchReason', 'N/A')}")
    
    # Test Office Meeting
    print(f"\n{'─'*80}")
    print("TEST 3: Office Meeting Event Context")
    print(f"{'─'*80}")
    
    pairing2 = get_event_based_pairing(
        pencil_skirt['type'], 
        pencil_skirt.get('primaryColor', 'Black'), 
        'Office Meeting'
    )
    
    print(f"\n✅ Recommended Types:")
    for t in pairing2['matching_types']:
        print(f"   • {t}")
    
    print(f"\n❌ Avoid Types:")
    for t in pairing2.get('avoid_types', []):
        print(f"   • {t}")
    
    print("\n" + "="*80)
    print("✅ DEBUG COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    debug_pairing()
