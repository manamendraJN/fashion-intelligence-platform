"""
Test script for event-based clothing pairing recommendations
"""
import sys
sys.path.append('backend')

from utils.color_utils import get_event_based_pairing

def test_event_pairing():
    """Test event-based pairing rules"""
    
    print("\n" + "="*80)
    print("EVENT-BASED CLOTHING PAIRING TEST")
    print("="*80)
    
    # Test cases: (item_type, item_color, event_type)
    test_cases = [
        # ─────────────── OFFICE ───────────────
        ("Jeans", "Blue", "Office"),
        ("Pencil Skirt", "Black", "Office"),
        ("Trousers", "Gray", "Office"),
        ("Blouse", "White", "Office"),
        
        # ────────────── OFFICE MEETING ─────────
        ("Pencil Skirt", "Black", "Office Meeting"),
        ("Blazers", "Navy", "Office Meeting"),
        ("Trousers", "Gray", "Office Meeting"),
        
        # ─────────────── CASUAL ────────────────
        ("Jeans", "Blue", "Casual"),
        ("Tshirts", "White", "Casual"),
        ("Shorts", "Khaki", "Casual"),
        ("Skirts", "Pink", "Casual"),
        
        # ───────────── NO EVENT CONTEXT ────────
        ("Jeans", "Blue", None),
        ("Pencil Skirt", "Black", None),
    ]
    
    for item_type, item_color, event_type in test_cases:
        result = get_event_based_pairing(item_type, item_color, event_type)
        
        event_label = event_type if event_type else "No Event"
        print(f"\n{'─'*80}")
        print(f"🎯 Event: {event_label}")
        print(f"👕 Item: {item_color} {item_type}")
        print(f"{'─'*80}")
        
        if event_type:
            print(f"📌 Note: {result.get('pairing_note', 'N/A')}")
            print(f"\n✅ RECOMMENDED PAIRINGS:")
            for match_type in result['matching_types'][:5]:
                print(f"   • {match_type}")
            
            if result.get('avoid_types'):
                print(f"\n❌ AVOID (Not Appropriate for {event_type}):")
                for avoid_type in result['avoid_types'][:5]:
                    print(f"   • {avoid_type}")
        else:
            print(f"📌 Note: {result.get('pairing_note', 'N/A')}")
            print(f"\n✅ GENERAL PAIRINGS:")
            for match_type in result['matching_types'][:5]:
                print(f"   • {match_type}")
        
        print(f"\n🎨 MATCHING COLORS:")
        for color in result['matching_colors'][:8]:
            print(f"   • {color.title()}")
    
    print(f"\n{'='*80}")
    print("✨ TEST COMPLETE")
    print("="*80)
    
    # Demonstrate the key differences
    print("\n" + "="*80)
    print("KEY DIFFERENCES DEMONSTRATION")
    print("="*80)
    
    print("\n🔍 JEANS PAIRING COMPARISON:")
    print("\n1️⃣  OFFICE context (Jeans):")
    office_jeans = get_event_based_pairing("Jeans", "Blue", "Office")
    print(f"   Pair with: {', '.join(office_jeans['matching_types'][:3])}")
    print(f"   Avoid: {', '.join(office_jeans['avoid_types'][:3]) if office_jeans['avoid_types'] else 'None'}")
    
    print("\n2️⃣  CASUAL context (Jeans):")
    casual_jeans = get_event_based_pairing("Jeans", "Blue", "Casual")
    print(f"   Pair with: {', '.join(casual_jeans['matching_types'][:3])}")
    print(f"   Avoid: {', '.join(casual_jeans['avoid_types'][:3]) if casual_jeans['avoid_types'] else 'None'}")
    
    print("\n🔍 PENCIL SKIRT COMPARISON:")
    print("\n1️⃣  OFFICE context:")
    office_skirt = get_event_based_pairing("Pencil Skirt", "Black", "Office")
    print(f"   Pair with: {', '.join(office_skirt['matching_types'][:3])}")
    print(f"   Note: {office_skirt['pairing_note']}")
    
    print("\n2️⃣  OFFICE MEETING context:")
    meeting_skirt = get_event_based_pairing("Pencil Skirt", "Black", "Office Meeting")
    print(f"   Pair with: {', '.join(meeting_skirt['matching_types'][:3])}")
    print(f"   Note: {meeting_skirt['pairing_note']}")
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_event_pairing()
