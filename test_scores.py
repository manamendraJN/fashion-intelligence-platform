"""
Test script to verify event scores for different clothing types
Run this to check if the rule-based scoring is working correctly
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'backend'))

from core.event_constants import get_default_event_scores

def test_clothing_type(clothing_type):
    """Test and display event scores for a clothing type"""
    scores = get_default_event_scores(clothing_type)
    
    print(f"\n{'='*60}")
    print(f"🔍 Testing: {clothing_type}")
    print(f"{'='*60}")
    
    # Sort scores by value (highest first)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Event':<20} {'Score':<10} {'Bar'}")
    print(f"{'-'*60}")
    
    for event, score in sorted_scores:
        bar = '█' * int(score * 50)
        percentage = int(score * 100)
        
        # Color coding
        if score >= 0.8:
            emoji = "🟢"  # High score - Perfect match
        elif score >= 0.6:
            emoji = "🟡"  # Good score
        elif score >= 0.4:
            emoji = "🟠"  # Moderate score
        else:
            emoji = "🔴"  # Low score - Not recommended
            
        print(f"{emoji} {event:<18} {percentage:>3}%  {bar}")
    
    # Best event
    best_event = max(scores, key=scores.get)
    best_score = scores[best_event]
    print(f"\n✨ Best Event: {best_event} ({int(best_score * 100)}%)")
    
    return best_event, best_score

def main():
    """Test various clothing types"""
    
    print("\n" + "="*60)
    print("🧪 FASHION INTELLIGENCE PLATFORM - EVENT SCORE TESTING")
    print("="*60)
    
    # Test cases that should show office-appropriate
    office_items = [
        "Pencil Skirt",
        "Cigarette Pants",
        "Formal Trousers",
        "Blazers",
        "Blouse",
        "Office Saree"
    ]
    
    # Test cases that should show casual
    casual_items = [
        "Denim Skirt",
        "Jeans",
        "T-shirts",
        "Casual Dress",
        "Cargo Pants"
    ]
    
    # Test cases for beach
    beach_items = [
        "Swimwear",
        "Bikini",
        "One-piece Swimsuit"
    ]
    
    print("\n" + "🏢 " + "="*55)
    print("OFFICE-APPROPRIATE ITEMS (Should score high for Office)")
    print("="*60)
    
    for item in office_items:
        best_event, score = test_clothing_type(item)
        if best_event != "Office" and score < 0.85:
            print(f"\n⚠️  WARNING: {item} should prioritize Office event!")
    
    print("\n" + "👕 " + "="*55)
    print("CASUAL ITEMS (Should score high for Casual)")
    print("="*60)
    
    for item in casual_items:
        best_event, score = test_clothing_type(item)
        if best_event != "Casual" and score < 0.85:
            print(f"\n⚠️  WARNING: {item} should prioritize Casual event!")
    
    print("\n" + "🏖️ " + "="*55)
    print("BEACH/SWIM ITEMS (Should score high for Beach)")
    print("="*60)
    
    for item in beach_items:
        best_event, score = test_clothing_type(item)
        if best_event != "Beach" and score < 0.90:
            print(f"\n⚠️  WARNING: {item} should prioritize Beach event!")
    
    print("\n" + "="*60)
    print("✅ Testing Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
