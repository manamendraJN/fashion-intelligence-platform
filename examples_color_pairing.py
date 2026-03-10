"""
Practical Examples: Color Extraction & Pairing Usage
Shows how to use the new color-based pairing system
"""

# ============================================================
# EXAMPLE 1: Extract Color from an Image
# ============================================================

from backend.utils.color_utils import extract_dominant_color
from PIL import Image

# Load an image
image = Image.open("path/to/clothing.jpg")

# Extract colors
color_data = extract_dominant_color(image, n_colors=3)

print("Color Analysis:")
print(f"Primary Color: {color_data['primary_color']}")
print(f"RGB Values: {color_data['rgb']}")
print(f"All Colors: {color_data['all_colors']}")

# Output example:
# Primary Color: Blue
# RGB Values: [45, 85, 165]
# All Colors: [
#   {'color': 'Blue', 'rgb': [45, 85, 165], 'percentage': 65.4},
#   {'color': 'White', 'rgb': [240, 240, 240], 'percentage': 25.1},
#   {'color': 'Black', 'rgb': [20, 20, 20], 'percentage': 9.5}
# ]


# ============================================================
# EXAMPLE 2: Check Color Compatibility
# ============================================================

from backend.utils.color_utils import are_colors_compatible, get_matching_colors

# Check if two colors match
print(are_colors_compatible("Blue", "White"))  # True
print(are_colors_compatible("Blue", "Denim"))  # True
print(are_colors_compatible("Red", "Green"))   # False

# Get all matching colors for a color
matches = get_matching_colors("Blue")
print(f"Blue matches with: {matches}")
# Output: ['white', 'black', 'gray', 'beige', 'yellow', 'orange', 'brown', 'denim', 'navy']


# ============================================================
# EXAMPLE 3: Get Pairing Recommendations
# ============================================================

from backend.utils.color_utils import get_complementary_items

# For a blue blouse
recommendations = get_complementary_items("Blouse", "Blue")
print(recommendations)

# Output:
# {
#   'matching_types': ['Bottoms', 'Jeans', 'Trousers', 'Skirts', 'Pencil Skirts'],
#   'matching_colors': ['white', 'black', 'gray', 'beige', 'yellow', 'orange', 'brown', 'denim', 'navy']
# }


# ============================================================
# EXAMPLE 4: Complete Wardrobe Upload Flow
# ============================================================

# In your upload code:
from backend.services.wardrobe_model_service import WardrobeModelService
from backend import database

# 1. User uploads image
image_file = request.files['image']
img = Image.open(image_file)

# 2. Analyze image (type + color + events)
service = WardrobeModelService(model_dir)
result = service.full_analysis(img)

# 3. Save to database with color data
item_id = database.add_wardrobe_item(
    filename="blouse.jpg",
    image_path="/uploads/blouse.jpg",
    clothing_type=result["clothing_type"],       # "Blouse"
    confidence=result["confidence"],             # 0.98
    top_5=result["top_5"],
    event_scores=result["event_scores"],
    best_event=result["best_event"],
    primary_color=result["primary_color"],       # "Blue"
    color_rgb=result["color_rgb"],               # [45, 85, 165]
    all_colors=result["all_colors"]
)

print(f"Saved: {result['primary_color']} {result['clothing_type']} (ID: {item_id})")
# Output: Saved: Blue Blouse (ID: 123)


# ============================================================
# EXAMPLE 5: Get Pairing Recommendations via API
# ============================================================

# Frontend JavaScript example:
"""
// User clicks on a blue blouse (item_id = 5)
async function getPairings(itemId) {
  const response = await fetch(`/api/outfit-pairing/${itemId}`);
  const data = await response.json();
  
  if (data.success) {
    console.log(`Item: ${data.item.color} ${data.item.type}`);
    console.log(`Found ${data.matches.length} matching items:`);
    
    data.matches.forEach(match => {
      console.log(`
        - ${match.primaryColor} ${match.type}
        - Compatibility: ${match.compatibilityScore}/100
        - Why: ${match.reasons.join(', ')}
      `);
    });
  }
}

// Example output:
// Item: Blue Blouse
// Found 6 matching items:
//   - White Trousers
//   - Compatibility: 100/100
//   - Why: Pairs well with Blouse, White matches Blue
//
//   - Black Skirts
//   - Compatibility: 100/100
//   - Why: Pairs well with Blouse, Black matches Blue
//
//   - Denim Jeans
//   - Compatibility: 100/100
//   - Why: Pairs well with Blouse, Denim matches Blue
"""


# ============================================================
# EXAMPLE 6: Query Database for Matches
# ============================================================

from backend import database

# Get a specific item
item = database.get_wardrobe_item(item_id=5)
print(f"Item: {item['primaryColor']} {item['type']}")

# Get matching items
matching_types = ["Jeans", "Trousers", "Skirts"]
matching_colors = ["white", "black", "denim"]
matches = database.get_matching_items(
    item_id=5,
    matching_types=matching_types,
    matching_colors=matching_colors
)

print(f"Found {len(matches)} matching items")
for match in matches:
    print(f"  - {match['primaryColor']} {match['type']} ({match['matchReason']})")

# Output:
# Found 5 matching items
#   - White Trousers (Type: Trousers | Color: White)
#   - Black Skirts (Type: Skirts | Color: Black)
#   - Denim Jeans (Type: Jeans | Color: Denim)
#   - Gray Trousers (Type: Trousers)
#   - Navy Bottoms (Color: Navy)


# ============================================================
# EXAMPLE 7: Practical Pairing Scenarios
# ============================================================

print("\n=== OUTFIT PAIRING EXAMPLES ===\n")

scenarios = [
    {
        "item": "Blue Blouse",
        "pairs_with": [
            "White Pencil Skirt - Professional office look",
            "Black Trousers - Classic combination",
            "Denim Jeans - Casual everyday outfit",
        ]
    },
    {
        "item": "Black Trousers",
        "pairs_with": [
            "White Blouse - Timeless formal look",
            "Red Top - Bold statement outfit",
            "Pink Shirt - Modern professional style",
        ]
    },
    {
        "item": "Denim Jeans",
        "pairs_with": [
            "White T-Shirt - Classic casual",
            "Red Blouse - Eye-catching combo",
            "Black Hoodie - Comfortable street style",
        ]
    }
]

for scenario in scenarios:
    print(f"🔹 {scenario['item']}")
    for pairing in scenario['pairs_with']:
        print(f"   ✓ {pairing}")
    print()

# Output:
# 🔹 Blue Blouse
#    ✓ White Pencil Skirt - Professional office look
#    ✓ Black Trousers - Classic combination
#    ✓ Denim Jeans - Casual everyday outfit
#
# 🔹 Black Trousers
#    ✓ White Blouse - Timeless formal look
#    ✓ Red Top - Bold statement outfit
#    ✓ Pink Shirt - Modern professional style
#
# 🔹 Denim Jeans
#    ✓ White T-Shirt - Classic casual
#    ✓ Red Blouse - Eye-catching combo
#    ✓ Black Hoodie - Comfortable street style


# ============================================================
# EXAMPLE 8: Building a Complete Outfit
# ============================================================

def build_outfit(top_id):
    """Get complete outfit recommendations for a top"""
    import backend.database as db
    from backend.utils.color_utils import get_complementary_items
    
    # Get the top
    top = db.get_wardrobe_item(top_id)
    print(f"\nBuilding outfit for: {top['primaryColor']} {top['type']}")
    print("=" * 50)
    
    # Get recommendations
    recs = get_complementary_items(top['type'], top['primaryColor'])
    
    # Find bottoms
    matches = db.get_matching_items(
        item_id=top_id,
        matching_types=recs['matching_types'],
        matching_colors=recs['matching_colors']
    )
    
    if matches:
        best_match = matches[0]
        print(f"\n👕 Top: {top['primaryColor']} {top['type']}")
        print(f"👖 Bottom: {best_match['primaryColor']} {best_match['type']}")
        print(f"💯 Compatibility: {best_match.get('compatibilityScore', 'N/A')}/100")
        print(f"📍 Reason: {best_match.get('matchReason', 'Good match!')}")
        print(f"\n✨ Perfect for: {top['bestEvent']}")
    else:
        print("No matching bottoms found. Consider adding more items!")

# Usage:
# build_outfit(top_id=5)

# Output:
# Building outfit for: Blue Blouse
# ==================================================
#
# 👕 Top: Blue Blouse
# 👖 Bottom: White Trousers
# 💯 Compatibility: 100/100
# 📍 Reason: Type: Trousers | Color: White
#
# ✨ Perfect for: Office Meeting
