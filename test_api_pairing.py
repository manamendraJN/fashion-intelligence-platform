"""
Test the actual API endpoint response for pairing
"""
import sys
sys.path.append('backend')

import database
from utils.color_utils import get_event_based_pairing, are_colors_compatible

def test_api_logic():
    """Test the exact logic used in the API endpoint"""
    
    print("\n" + "="*80)
    print("🧪 TESTING API ENDPOINT LOGIC")
    print("="*80)
    
    # Get pencil skirt
    items = database.get_all_wardrobe_items()
    pencil_skirts = [item for item in items if 'pencil' in item['type'].lower()]
    
    if not pencil_skirts:
        print("\n❌ No pencil skirts found!")
        return
    
    item = pencil_skirts[0]
    item_id = item['id']
    item_type = item['type']
    item_color = item.get('primaryColor', 'Unknown')
    
    print(f"\n👗 Testing with: {item_type} (ID: {item_id})")
    print(f"   Color: {item_color}")
    
    # Simulate API logic
    event_type = "Office"
    print(f"\n📅 Event Context: {event_type}")
    
    # Get event-based pairing recommendations
    recommendations = get_event_based_pairing(item_type, item_color, event_type)
    matching_types = recommendations['matching_types']
    matching_colors = recommendations['matching_colors']
    avoid_types = recommendations.get('avoid_types', [])
    pairing_note = recommendations.get('pairing_note', '')
    
    print(f"\n✅ Matching Types: {matching_types}")
    print(f"❌ Avoid Types: {avoid_types}")
    print(f"🎨 Matching Colors: {matching_colors[:10]}")
    
    # Query database
    matches = database.get_matching_items(item_id, matching_types, matching_colors)
    print(f"\n📊 Database returned: {len(matches)} potential matches")
    
    # Filter out avoided types
    if avoid_types:
        matches = [m for m in matches if m['type'] not in avoid_types]
    print(f"📊 After filtering avoided types: {len(matches)} matches")
    
    # Enhanced filtering (API logic)
    enhanced_matches = []
    for match in matches:
        match_color = (match.get('primaryColor') or 'Unknown').lower()
        match_type = match.get('type', 'Unknown')
        item_color_lower = item_color.lower()
        matching_colors_lower = [c.lower() for c in matching_colors]
        
        print(f"\n  🔍 Checking: {match_type} - {match.get('primaryColor', 'Unknown')}")
        print(f"     Type in list? {match_type in matching_types}")
        print(f"     Color '{match_color}' in matching colors? {match_color in matching_colors_lower}")
        
        compatibility_score = 0
        reasons = []
        
        # Type match
        if match_type in matching_types:
            if event_type:
                compatibility_score += 80
                reasons.append(f"Perfect for {event_type}: {match_type} pairs with {item_type}")
            else:
                compatibility_score += 70
                reasons.append(f"Pairs well with {item_type}")
            print(f"     ✅ Type match! Score: {compatibility_score}")
        
        # Color match
        if match_color in matching_colors_lower or are_colors_compatible(item_color, match.get('primaryColor', 'Unknown')):
            compatibility_score += 20
            reasons.append(f"{match.get('primaryColor', 'Unknown')} matches {item_color}")
            print(f"     ✅ Color match! Score: {compatibility_score}")
        
        if compatibility_score > 0:
            match['compatibilityScore'] = compatibility_score
            match['reasons'] = reasons
            enhanced_matches.append(match)
            print(f"     ✅ ADDED TO RESULTS (score: {compatibility_score})")
        else:
            print(f"     ❌ REJECTED (score: 0)")
    
    # Sort by score
    enhanced_matches.sort(key=lambda x: x['compatibilityScore'], reverse=True)
    
    print(f"\n{'─'*80}")
    print(f"📊 FINAL RESULTS: {len(enhanced_matches)} matches")
    print(f"{'─'*80}")
    
    for i, match in enumerate(enhanced_matches[:10], 1):
        print(f"\n{i}. {match['type']} - {match.get('primaryColor', 'Unknown')}")
        print(f"   Score: {match['compatibilityScore']}")
        print(f"   Reasons:")
        for reason in match['reasons']:
            print(f"     • {reason}")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_api_logic()
