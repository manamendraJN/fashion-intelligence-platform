"""
color_utils.py
==============
Outfit pairing logic — answers "what should I pair with item X for occasion Y?"

PAIRING RULES SUMMARY
---------------------
Office / Office Meeting  → formal tops ↔ formal bottoms ONLY
                           blazers over formal tops
                           avoid: t-shirts, jeans, hoodies, shorts, leggings

Casual                   → casual tops ↔ jeans/shorts/casual bottoms
                           avoid: pencil skirts, formal trousers, blazers

Family Gathering         → kurtas, casual shirts, sweaters, polo shirts
                           ↔ chinos, salwars, jeans, midi skirts, maxi dresses
                           avoid: formal office wear

Tamil Wedding            → silk kurtas, sherwanis, lehengas, sarees
                           avoid: western casual

Western Wedding          → formal dresses, gowns, blazers, formal trousers

Party                    → cocktail dresses, lehengas, jumpsuits
                           tops + skirts / jeans

Date Night               → midi/maxi dresses, formal dresses, blouses + skirts

Gym / Sports             → athletic items ONLY

Beach                    → swimwear, shorts, sundresses

Funeral                  → black/dark tops ↔ black/dark bottoms
                           formal items preferred
                           avoid: bright colours, casual items
"""

import cv2
import numpy as np
import colorsys
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter


# ─── Color Extraction Functions ───────────────────────────────────────────────

def rgb_to_color_name(rgb):
    """
    Convert RGB values to human-readable color names
    
    Args:
        rgb: Tuple of (R, G, B) values (0-255)
    
    Returns:
        Color name as string
    """
    r, g, b = rgb
    
    # Convert to HSV for better color identification
    hsv = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    h, s, v = hsv[0] * 360, hsv[1] * 100, hsv[2] * 100
    
    # Check for neutral colors first (low saturation)
    if s < 10:
        if v < 20:
            return "Black"
        elif v > 90:
            return "White"
        elif v > 60:
            return "Light Gray"
        else:
            return "Gray"
    
    # Special case for very light colors (pastels with low saturation)
    if s < 30 and v > 80:
        if 200 <= h < 280:
            return "Light Purple"
        elif 280 <= h < 360 or h < 15:
            return "Light Pink"
        elif 160 <= h < 240:
            return "Light Blue"
        elif 75 <= h < 160:
            return "Light Green"
        elif 45 <= h < 75:
            return "Light Yellow"
        elif 15 <= h < 45:
            return "Peach"
    
    # Check for browns (special case)
    if 20 <= h <= 40 and s > 20 and 20 < v < 70:
        return "Brown"
    
    # Check if color is light/pastel or dark
    is_light = v > 70 and 30 <= s < 60
    is_dark = v < 45
    
    # Color detection by hue
    if h < 15 or h >= 345:
        if is_light:
            return "Light Pink"
        elif is_dark:
            return "Dark Red"
        else:
            return "Red"
    elif 15 <= h < 45:
        if s > 60 and v > 60:
            return "Orange"
        elif v > 70 and s < 40:
            return "Peach"
        else:
            return "Brown"
    elif 45 <= h < 75:
        if is_light:
            return "Light Yellow"
        elif is_dark:
            return "Olive"
        else:
            return "Yellow"
    elif 75 <= h < 155:
        if is_light:
            return "Light Green"
        elif is_dark:
            return "Dark Green"
        else:
            return "Green"
    elif 155 <= h < 185:
        if is_light:
            return "Light Cyan"
        else:
            return "Cyan"
    elif 185 <= h < 260:
        if is_light:
            return "Light Blue"
        elif is_dark or (v < 55 and s > 70):
            return "Navy"
        else:
            return "Blue"
    elif 260 <= h < 290:
        if is_light:
            return "Light Purple"
        elif is_dark:
            return "Dark Purple"
        else:
            return "Purple"
    elif 290 <= h < 320:
        if is_light:
            return "Light Pink"
        else:
            return "Magenta"
    elif 320 <= h < 345:
        if v > 75:
            return "Light Pink"
        else:
            return "Pink"
    
    return "Unknown"


def extract_dominant_color(image_input, n_colors=3):
    """
    Extract dominant colors from an image
    
    Args:
        image_input: PIL Image, numpy array, or file path
        n_colors: Number of dominant colors to extract
    
    Returns:
        Dictionary with primary color name, RGB values, and all colors
    """
    # Convert to PIL Image if needed
    if isinstance(image_input, str):
        img = Image.open(image_input)
    elif isinstance(image_input, np.ndarray):
        img = Image.fromarray(image_input)
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise ValueError("Invalid image input")
    
    # Convert to RGB
    img = img.convert('RGB')
    
    # Resize for faster processing
    img_small = img.resize((150, 150))
    
    # Convert to numpy array
    img_array = np.array(img_small)
    pixels = img_array.reshape(-1, 3)
    
    # Remove very dark pixels (likely background/shadows)
    mask = np.mean(pixels, axis=1) > 20
    pixels = pixels[mask]
    
    if len(pixels) == 0:
        return {"primary_color": "Black", "rgb": [0, 0, 0], "all_colors": []}
    
    # Use KMeans to find dominant colors
    kmeans = KMeans(n_clusters=min(n_colors, len(pixels)), random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get color frequencies
    labels = kmeans.labels_
    label_counts = Counter(labels)
    
    # Sort by frequency
    dominant_colors = []
    for label in label_counts.most_common(n_colors):
        rgb = kmeans.cluster_centers_[label[0]].astype(int)
        color_name = rgb_to_color_name(tuple(rgb))
        percentage = (label[1] / len(labels)) * 100
        dominant_colors.append({
            "color": color_name,
            "rgb": rgb.tolist(),
            "percentage": round(percentage, 2)
        })
    
    # Primary color is the most frequent
    primary = dominant_colors[0] if dominant_colors else {"color": "Unknown", "rgb": [0, 0, 0], "percentage": 0}
    
    return {
        "primary_color": primary["color"],
        "rgb": primary["rgb"],
        "all_colors": dominant_colors
    }


# ─── Clothing type buckets ────────────────────────────────────────────────────

FORMAL_TOPS = [
    "Blouse", "Formal Shirt", "Dress Shirt", "Button-Down Shirt",
    "Button Down Shirt", "Blazers", "Blazer",
]

FORMAL_BOTTOMS = [
    "Pencil Skirt", "A-Line Skirt", "Cigarette Pants",
    "Formal Trousers", "Dress Pants", "Formal Pants", "Chinos",
]

CASUAL_TOPS = [
    "T-Shirts", "T-Shirt", "Tank Top", "Crop Top", "Casual Shirt",
    "Hoodies", "Hoodie", "Sweatshirt", "Sweaters", "Cardigan",
    "Polo Shirt", "Polo", "Tops", "Tunic",
]

CASUAL_BOTTOMS = [
    "Jeans", "Shorts", "Denim Shorts", "Bermuda Shorts",
    "Leggings", "Midi Skirt", "Maxi Skirt", "Denim Skirt",
    "Mini Skirt", "Cargo Pants", "Trousers", "Chinos",
]

ATHLETIC = [
    "Gym Wear", "Sports Bra", "Yoga Pants", "Athletic Shorts",
    "Tracksuit", "Track Pants", "Joggers", "Leggings",
]

PARTY_TOPS = [
    "Blouse", "Crop Top", "Tank Top", "Blazers", "Blazer", "Tops",
]

PARTY_BOTTOMS = [
    "Mini Skirt", "Pencil Skirt", "Cigarette Pants", "Jeans",
    "Formal Trousers",
]

FORMAL_DRESSES = [
    "Formal Dress", "Evening Gown", "Gown", "Cocktail Dress",
    "Maxi Dress", "Midi Dress",
]

CASUAL_DRESSES = [
    "Casual Dress", "Sundress", "Shirt Dress", "Shirtdress",
    "Maxi Dress", "Midi Dress",
]

ETHNIC_TOPS = [
    "Silk Kurta", "Traditional Kurta", "Kurta", "Kurti", "Cotton Kurta",
    "Casual Kurta", "Blouse",   # sari blouse
    "Sherwani",
]

ETHNIC_BOTTOMS = [
    "Wedding Saree", "Bridal Saree", "Silk Saree", "Traditional Saree",
    "Cotton Saree", "Casual Saree", "Office Saree", "Saree", "Sari",
    "Lehenga", "Wedding Lehenga", "Bridal Lehenga",
    "Salwar", "Patiala", "Churidar", "Formal Trousers",
]

DARK_APPROPRIATE = [
    "Black", "Dark Gray", "Gray", "Charcoal", "Navy", "Dark Blue",
    "Dark Navy", "Dark Grey", "Charcoal Gray", "White", "Cream",
    "Off White", "Light Gray", "Light Grey", "Dark Purple",
    "Burgundy", "Dark Red", "Dark Brown", "Dark Green",
]


# ─── Colour compatibility ─────────────────────────────────────────────────────

COLOR_COMPATIBILITY = {
    "black":   ["white", "grey", "gray", "red", "blue", "pink", "beige", "navy", "cream",
                "silver", "gold", "burgundy", "purple", "any"],
    "white":   ["black", "navy", "blue", "grey", "gray", "beige", "pink", "red",
                "brown", "green", "any"],
    "navy":    ["white", "light blue", "grey", "gray", "beige", "cream", "red",
                "light pink", "gold"],
    "grey":    ["black", "white", "navy", "blue", "pink", "purple", "red", "any"],
    "gray":    ["black", "white", "navy", "blue", "pink", "purple", "red", "any"],
    "beige":   ["white", "black", "brown", "navy", "olive", "cream", "gold"],
    "cream":   ["navy", "black", "brown", "beige", "gold", "burgundy", "olive"],
    "blue":    ["white", "grey", "gray", "beige", "navy", "light blue", "cream"],
    "brown":   ["beige", "cream", "white", "olive", "gold", "tan", "camel"],
    "red":     ["black", "white", "navy", "grey", "gray"],
    "pink":    ["white", "grey", "navy", "black", "beige", "cream"],
    "green":   ["white", "beige", "cream", "navy", "brown", "olive"],
    "olive":   ["white", "beige", "cream", "brown", "navy", "camel"],
    "purple":  ["white", "grey", "black", "lavender", "cream"],
    "yellow":  ["white", "navy", "grey", "black"],
    "orange":  ["white", "navy", "black", "brown"],
    "gold":    ["black", "navy", "white", "cream", "brown"],
    "silver":  ["black", "white", "grey", "navy", "blue"],
    "burgundy":["white", "black", "grey", "cream", "beige"],
    "camel":   ["white", "black", "navy", "burgundy", "cream"],
    "tan":     ["white", "navy", "blue", "cream", "brown"],
}

NEUTRAL_COLORS = {"black", "white", "grey", "gray", "beige", "cream", "navy", "camel", "tan"}


def are_colors_compatible(color1, color2):
    if not color1 or not color2:
        return True
    c1, c2 = color1.lower().strip(), color2.lower().strip()
    if c1 == c2:
        return True
    if c1 in NEUTRAL_COLORS or c2 in NEUTRAL_COLORS:
        return True
    compatible = COLOR_COMPATIBILITY.get(c1, [])
    if c2 in compatible or "any" in compatible:
        return True
    compatible2 = COLOR_COMPATIBILITY.get(c2, [])
    if c1 in compatible2 or "any" in compatible2:
        return True
    return False


def get_matching_colors(primary_color):
    if not primary_color:
        return ["black", "white", "navy", "grey", "beige"]
    color = primary_color.lower().strip()
    return COLOR_COMPATIBILITY.get(color, ["black", "white", "navy", "grey", "beige"])


# ─── Category matching helpers ────────────────────────────────────────────────

def is_same_category(item_type1, item_type2):
    """
    Checks if two items belong to the same category (both tops, both bottoms, etc.)
    to prevent tops from pairing with tops, bottoms with bottoms, etc.
    
    Returns:
        True if both items are in the same category (should not pair)
        False if items are in different categories (can pair)
    """
    t1 = item_type1.lower().strip()
    t2 = item_type2.lower().strip()
    
    # Define category groups
    TOPS = ["shirt", "blouse", "top", "sweater", "hoodie", "sweatshirt", "blazer", 
            "jacket", "cardigan", "coat", "polo", "tunic", "tank top", "crop top",
            "t-shirt", "tshirt", "tee"]
    
    BOTTOMS = ["jean", "trouser", "pants", "skirt", "short", "legging", "chino",
               "pant", "patiala", "salwar", "churidar", "cargo"]
    
    DRESSES = ["dress", "gown", "jumpsuit", "romper", "maxi dress", "midi dress",
               "sundress", "cocktail dress"]
    
    ETHNIC_FULL = ["saree", "sari", "lehenga"]
    
    # Check if both are tops
    is_t1_top = any(top in t1 for top in TOPS)
    is_t2_top = any(top in t2 for top in TOPS)
    if is_t1_top and is_t2_top:
        return True  # Both are tops, don't pair
    
    # Check if both are bottoms
    is_t1_bottom = any(bot in t1 for bot in BOTTOMS)
    is_t2_bottom = any(bot in t2 for bot in BOTTOMS)
    if is_t1_bottom and is_t2_bottom:
        return True  # Both are bottoms, don't pair
    
    # Check if both are dresses
    is_t1_dress = any(dress in t1 for dress in DRESSES)
    is_t2_dress = any(dress in t2 for dress in DRESSES)
    if is_t1_dress and is_t2_dress:
        return True  # Both are dresses, don't pair
    
    # Check if both are full ethnic garments
    is_t1_ethnic = any(eth in t1 for eth in ETHNIC_FULL)
    is_t2_ethnic = any(eth in t2 for eth in ETHNIC_FULL)
    if is_t1_ethnic and is_t2_ethnic:
        return True  # Both are full garments, don't pair
    
    return False  # Different categories, can pair


# ─── Event-based pairing ──────────────────────────────────────────────────────

def get_event_based_pairing(item_type, item_color, event_type="casual"):
    """
    Returns pairing recommendations for a given item and event.

    Returns dict:
        matching_types   – list of clothing types that pair well
        matching_colors  – list of compatible colours
        avoid_types      – list of types that should NEVER appear in results
        pairing_note     – human-readable style tip
        pairing_category – short category label shown in UI header
    """
    t = item_type.lower().strip()
    ev = (event_type or "casual").lower().strip()

    colors = get_matching_colors(item_color)

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _is_formal_top(x):
        return any(ft.lower() in x or x in ft.lower() for ft in FORMAL_TOPS)

    def _is_formal_bottom(x):
        return any(fb.lower() in x or x in fb.lower() for fb in FORMAL_BOTTOMS)

    def _is_casual_top(x):
        return any(ct.lower() in x or x in ct.lower() for ct in CASUAL_TOPS)

    def _is_casual_bottom(x):
        return any(cb.lower() in x or x in cb.lower() for cb in CASUAL_BOTTOMS)

    def _is_ethnic(x):
        return any(e.lower() in x or x in e.lower() for e in ETHNIC_TOPS + ETHNIC_BOTTOMS)

    def _is_athletic(x):
        return any(a.lower() in x or x in a.lower() for a in ATHLETIC)

    # ─── OFFICE / OFFICE MEETING ─────────────────────────────────────────────
    if ev in ("office", "office meeting"):
        # For blazers, pair with formal bottoms
        if "blazer" in t:
            return {
                "matching_types":  FORMAL_BOTTOMS,
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Leggings",
                                    "Hoodies", "Sweatshirt", "Gym Wear", "Sports Bra",
                                    "Blazers", "Blazer", "Cardigan"],
                "pairing_note":    "Pair blazers with formal trousers or pencil skirts for the office.",
                "pairing_category": "Office Wear",
            }
        if _is_formal_top(t):
            return {
                "matching_types":  FORMAL_BOTTOMS,
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Leggings",
                                    "Hoodies", "Sweatshirt", "Gym Wear", "Sports Bra"],
                "pairing_note":    "Pair formal tops with tailored trousers, chinos, or pencil skirts only.",
                "pairing_category": "Office Wear",
            }
        if _is_formal_bottom(t):
            return {
                "matching_types":  FORMAL_TOPS + ["Blazers"],
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Leggings",
                                    "Hoodies", "Sweatshirt", "Gym Wear"],
                "pairing_note":    "Formal trousers and skirts pair with blouses, formal shirts, or blazers.",
                "pairing_category": "Office Wear",
            }
        # Fall through to smart casual for anything else
        return {
            "matching_types":  FORMAL_TOPS + FORMAL_BOTTOMS,
            "matching_colors": colors,
            "avoid_types":     ["T-Shirts", "Shorts", "Leggings", "Gym Wear", "Sports Bra"],
            "pairing_note":    "For the office, stick to formal or smart-casual combinations.",
            "pairing_category": "Office Wear",
        }

    # ─── FUNERAL ─────────────────────────────────────────────────────────────
    if ev == "funeral":
        dark_colors = ["black", "dark gray", "charcoal", "navy", "dark navy", "white",
                       "cream", "gray", "light gray", "dark purple", "burgundy"]
        if _is_formal_top(t) or _is_formal_bottom(t):
            return {
                "matching_types":  FORMAL_TOPS + FORMAL_BOTTOMS + ["Formal Dress"],
                "matching_colors": dark_colors,
                "avoid_types":     ["T-Shirts", "Shorts", "Leggings", "Gym Wear",
                                    "Sundress", "Mini Skirt", "Crop Top", "Tank Top",
                                    "Jeans", "Casual Dress"],
                "pairing_note":    "Funerals require dark, subdued clothing — black, navy, grey or white only.",
                "pairing_category": "Funeral Attire",
            }
        return {
            "matching_types":  FORMAL_TOPS + FORMAL_BOTTOMS + FORMAL_DRESSES,
            "matching_colors": dark_colors,
            "avoid_types":     ["Shorts", "Leggings", "Gym Wear", "Sports Bra", "Bikini",
                                "Swimwear", "Sundress", "Crop Top", "Mini Skirt"],
            "pairing_note":    "Wear dark, respectful clothing — black, navy, charcoal, or white.",
            "pairing_category": "Funeral Attire",
        }

    # ─── CASUAL ──────────────────────────────────────────────────────────────
    if ev in ("casual", "shopping", "lunch", "travel"):
        # Sweaters, cardigans, hoodies pair with bottoms
        if "sweater" in t or "cardigan" in t or "hoodie" in t or "sweatshirt" in t:
            return {
                "matching_types":  ["Jeans", "Trousers", "Chinos", "Leggings",
                                    "Midi Skirt", "Maxi Skirt", "Cargo Pants"],
                "matching_colors": colors,
                "avoid_types":     ["Formal Trousers", "Pencil Skirt", "Formal Dress",
                                    "Evening Gown", "Gown", "Sweaters", "Cardigan",
                                    "Hoodies", "Blazers"],
                "pairing_note":    "Layer pieces like sweaters and cardigans pair with casual bottoms.",
                "pairing_category": "Casual Wear",
            }
        if _is_casual_top(t) or "t-shirt" in t or "tank top" in t or "crop top" in t:
            return {
                "matching_types":  ["Jeans", "Shorts", "Denim Shorts", "Denim Skirt",
                                    "Mini Skirt", "Leggings", "Chinos", "Midi Skirt",
                                    "Cargo Pants", "Bermuda Shorts"],
                "matching_colors": colors,
                "avoid_types":     ["Formal Trousers", "Pencil Skirt", "Formal Dress",
                                    "Evening Gown", "Gown", "Cigarette Pants"],
                "pairing_note":    "Keep it relaxed — jeans, shorts, or casual skirts work best.",
                "pairing_category": "Casual Wear",
            }
        if "jean" in t or "shorts" in t or "legging" in t or "cargo" in t or "skirt" in t:
            return {
                "matching_types":  CASUAL_TOPS + ["Casual Shirt", "Polo Shirt"],
                "matching_colors": colors,
                "avoid_types":     ["Blazers", "Formal Shirt", "Dress Shirt",
                                    "Formal Dress", "Evening Gown"],
                "pairing_note":    "Jeans and casual bottoms pair best with relaxed tops.",
                "pairing_category": "Casual Wear",
            }

    # ─── FAMILY GATHERING ────────────────────────────────────────────────────
    if ev == "family gathering":
        if _is_ethnic(t):
            return {
                "matching_types":  ETHNIC_TOPS + ETHNIC_BOTTOMS + ["Chinos", "Salwar", "Churidar"],
                "matching_colors": colors,
                "avoid_types":     ["Shorts", "Mini Skirt", "Gym Wear", "Sports Bra",
                                    "Swimwear", "Blazers", "Formal Trousers", "Pencil Skirt"],
                "pairing_note":    "Family gatherings call for modest, traditional or smart-casual outfits.",
                "pairing_category": "Family Gathering",
            }
        if "kurta" in t or "kurti" in t or "salwar" in t:
            return {
                "matching_types":  ["Salwar", "Churidar", "Leggings", "Chinos",
                                    "Casual Trousers", "Midi Skirt"],
                "matching_colors": colors,
                "avoid_types":     ["Shorts", "Mini Skirt", "Gym Wear", "Blazers"],
                "pairing_note":    "Pair kurtas with churidars, salwars, or chinos for a family event.",
                "pairing_category": "Family Gathering",
            }
        # Smart casual
        return {
            "matching_types":  ["Chinos", "Casual Shirt", "Polo Shirt", "Sweaters", "Cardigan",
                                 "Midi Skirt", "Maxi Skirt", "Jeans", "Salwar", "Kurta",
                                 "Casual Dress", "Maxi Dress", "Midi Dress", "Trousers"],
            "matching_colors": colors,
            "avoid_types":     ["Shorts", "Mini Skirt", "Gym Wear", "Sports Bra",
                                 "Swimwear", "Blazers", "Pencil Skirt",
                                 "Formal Trousers", "Cigarette Pants"],
            "pairing_note":    "Family gatherings = smart casual. Kurtas, midi dresses, chinos, sweaters — avoid office wear.",
            "pairing_category": "Family Gathering",
        }

    # ─── PARTY ───────────────────────────────────────────────────────────────
    if ev == "party":
        if "dress" in t or "gown" in t or "jumpsuit" in t or "lehenga" in t:
            return {
                "matching_types":  ["Blazers", "Blazer", "Formal Coat"],
                "matching_colors": colors,
                "avoid_types":     ["Gym Wear", "Sports Bra", "Tracksuit", "Hoodies", "Sweatshirt"],
                "pairing_note":    "Dresses and jumpsuits look great with a blazer for a party.",
                "pairing_category": "Party Wear",
            }
        if "blazer" in t:
            return {
                "matching_types":  PARTY_BOTTOMS + ["Party Dress", "Cocktail Dress"],
                "matching_colors": colors,
                "avoid_types":     ["Gym Wear", "Tracksuit", "Blazers", "Blazer"],
                "pairing_note":    "Blazers pair with party skirts, pants, or over a dress.",
                "pairing_category": "Party Wear",
            }
        if _is_formal_top(t) or "crop top" in t:
            return {
                "matching_types":  PARTY_BOTTOMS + ["Jeans"],
                "matching_colors": colors,
                "avoid_types":     ["Gym Wear", "Tracksuit"],
                "pairing_note":    "Party tops pair with mini skirts, pencil skirts, or jeans.",
                "pairing_category": "Party Wear",
            }
        return {
            "matching_types":  PARTY_TOPS + PARTY_BOTTOMS + FORMAL_DRESSES,
            "matching_colors": colors,
            "avoid_types":     ["Gym Wear", "Sports Bra", "Tracksuit"],
            "pairing_note":    "For a party, keep it fun and glam.",
            "pairing_category": "Party Wear",
        }

    # ─── DATE NIGHT ──────────────────────────────────────────────────────────
    if ev in ("date", "date night"):
        if "dress" in t or "jumpsuit" in t:
            return {
                "matching_types":  ["Blazers", "Blazer", "Formal Coat"],
                "matching_colors": colors,
                "avoid_types":     ["Gym Wear", "Tracksuit", "Sports Bra"],
                "pairing_note":    "A blazer over a dress elevates any date night look.",
                "pairing_category": "Date Night",
            }
        if "blazer" in t:
            return {
                "matching_types":  ["Pencil Skirt", "A-Line Skirt", "Cigarette Pants",
                                    "Midi Skirt", "Maxi Skirt"],
                "matching_colors": colors,
                "avoid_types":     ["Gym Wear", "Shorts", "Leggings", "Blazers", "Blazer"],
                "pairing_note":    "Blazers pair elegantly with skirts or trousers for date night.",
                "pairing_category": "Date Night",
            }
        if _is_formal_top(t):
            return {
                "matching_types":  ["Pencil Skirt", "A-Line Skirt", "Cigarette Pants",
                                    "Midi Skirt", "Jeans"],
                "matching_colors": colors,
                "avoid_types":     ["Gym Wear", "Shorts", "Leggings"],
                "pairing_note":    "A blouse or formal top with a midi skirt or slim trousers is elegant.",
                "pairing_category": "Date Night",
            }
        return {
            "matching_types":  FORMAL_DRESSES + FORMAL_TOPS + ["Midi Skirt", "Maxi Skirt",
                                "A-Line Skirt", "Pencil Skirt", "Cigarette Pants"],
            "matching_colors": colors,
            "avoid_types":     ["Gym Wear", "Sports Bra", "Tracksuit"],
            "pairing_note":    "Date night = effortlessly elegant.",
            "pairing_category": "Date Night",
        }

    # ─── TAMIL WEDDING ───────────────────────────────────────────────────────
    if ev == "tamil wedding":
        if "saree" in t or "sari" in t:
            return {
                "matching_types":  ["Silk Kurta", "Traditional Kurta", "Blouse"],
                "matching_colors": colors,
                "avoid_types":     ["Shorts", "Jeans", "T-Shirts", "Gym Wear", "Casual Dress"],
                "pairing_note":    "Traditional sarees pair with silk blouses or kurtas.",
                "pairing_category": "Tamil Wedding",
            }
        if "kurta" in t or "kurti" in t or "sherwani" in t:
            return {
                "matching_types":  ETHNIC_BOTTOMS,
                "matching_colors": colors,
                "avoid_types":     ["Shorts", "Jeans", "T-Shirts", "Gym Wear"],
                "pairing_note":    "Silk kurtas and sherwanis pair with ethnic bottoms only.",
                "pairing_category": "Tamil Wedding",
            }
        return {
            "matching_types":  ETHNIC_TOPS + ETHNIC_BOTTOMS,
            "matching_colors": colors,
            "avoid_types":     ["Shorts", "Jeans", "T-Shirts", "Gym Wear",
                                 "Hoodies", "Sweatshirt", "Casual Dress", "Sundress"],
            "pairing_note":    "Traditional wear only — sarees, lehengas, silk kurtas.",
            "pairing_category": "Tamil Wedding",
        }

    # ─── WESTERN WEDDING ─────────────────────────────────────────────────────
    if ev == "western wedding":
        # For blazers, pair with formal bottoms
        if "blazer" in t:
            return {
                "matching_types":  FORMAL_BOTTOMS + ["Formal Dress", "Pencil Skirt", "Cigarette Pants"],
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Gym Wear",
                                    "Hoodies", "Casual Dress", "Sundress", "Blazers", "Blazer"],
                "pairing_note":    "Pair blazers with formal trousers or elegant skirts for a wedding.",
                "pairing_category": "Western Wedding",
            }
        # For formal tops, pair with formal bottoms
        if _is_formal_top(t):
            return {
                "matching_types":  FORMAL_BOTTOMS + ["Blazers"],
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Gym Wear",
                                    "Hoodies", "Casual Dress", "Sundress"],
                "pairing_note":    "Formal tops pair with tailored bottoms or add a blazer for weddings.",
                "pairing_category": "Western Wedding",
            }
        # For formal bottoms, pair with formal tops
        if _is_formal_bottom(t):
            return {
                "matching_types":  FORMAL_TOPS + ["Blazers"],
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Gym Wear",
                                    "Hoodies", "Casual Dress"],
                "pairing_note":    "Elegant trousers or skirts pair with formal tops and blazers.",
                "pairing_category": "Western Wedding",
            }
        # For dresses, pair with blazers/coats only
        if "dress" in t or "gown" in t:
            return {
                "matching_types":  ["Blazers", "Blazer", "Formal Coat"],
                "matching_colors": colors,
                "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Gym Wear",
                                    "Hoodies", "Casual Dress", "Sundress"],
                "pairing_note":    "A formal dress or gown is perfect for a wedding — add a blazer if needed.",
                "pairing_category": "Western Wedding",
            }
        # Default for western wedding
        return {
            "matching_types":  FORMAL_DRESSES + FORMAL_TOPS + FORMAL_BOTTOMS,
            "matching_colors": colors,
            "avoid_types":     ["T-Shirts", "Jeans", "Shorts", "Gym Wear",
                                 "Hoodies", "Casual Dress", "Sundress"],
            "pairing_note":    "Western weddings call for formal dresses, gowns, or elegant separates.",
            "pairing_category": "Western Wedding",
        }

    # ─── RELIGIOUS ───────────────────────────────────────────────────────────
    if ev == "religious":
        return {
            "matching_types":  ETHNIC_TOPS + ETHNIC_BOTTOMS + FORMAL_TOPS + FORMAL_BOTTOMS,
            "matching_colors": colors,
            "avoid_types":     ["Shorts", "Mini Skirt", "Gym Wear", "Sports Bra",
                                 "Swimwear", "Crop Top", "Tank Top"],
            "pairing_note":    "Dress modestly and traditionally for religious events.",
            "pairing_category": "Religious / Traditional",
        }

    # ─── GYM / SPORTS ────────────────────────────────────────────────────────
    if ev in ("gym", "sports", "running", "yoga"):
        return {
            "matching_types":  ATHLETIC + ["Leggings", "Yoga Pants", "Athletic Shorts",
                                            "Sports Bra", "T-Shirts", "Tank Top"],
            "matching_colors": colors,
            "avoid_types":     ["Blazers", "Formal Shirt", "Dress Shirt", "Formal Trousers",
                                 "Jeans", "Formal Dress", "Evening Gown", "Saree", "Lehenga"],
            "pairing_note":    "Gym and sports require breathable, stretch-friendly athletic wear only.",
            "pairing_category": "Athletic Wear",
        }

    # ─── BEACH ───────────────────────────────────────────────────────────────
    if ev == "beach":
        if "swimwear" in t or "bikini" in t or "swimsuit" in t:
            return {
                "matching_types":  ["Shorts", "Denim Shorts", "Sundress", "Casual Dress",
                                    "Cover-Up", "Sarong"],
                "matching_colors": colors,
                "avoid_types":     ["Blazers", "Formal Shirt", "Formal Trousers",
                                    "Formal Dress", "Evening Gown"],
                "pairing_note":    "Swimwear pairs with shorts or a breezy cover-up at the beach.",
                "pairing_category": "Beach Wear",
            }
        return {
            "matching_types":  ["Swimwear", "Shorts", "Denim Shorts", "Sundress",
                                 "Casual Dress", "T-Shirts", "Tank Top"],
            "matching_colors": colors,
            "avoid_types":     ["Blazers", "Formal Shirt", "Formal Trousers",
                                 "Formal Dress", "Evening Gown"],
            "pairing_note":    "Light, casual and breezy for the beach.",
            "pairing_category": "Beach Wear",
        }

    # ─── DEFAULT (general smart match) ───────────────────────────────────────
    return get_complementary_items(item_type, item_color)


def get_complementary_items(item_type, item_color):
    """
    Fallback pairing — used when no event-specific rule matches.
    Type-to-type mapping based on garment category.
    """
    t = item_type.lower().strip()
    colors = get_matching_colors(item_color)

    # Blazers / Jackets / Cardigans → bottoms or dresses
    if any(x in t for x in ['blazer', 'jacket', 'cardigan', 'coat']):
        return {
            "matching_types":  ["Jeans", "Trousers", "Chinos", "Skirt", "Shorts",
                                 "Leggings", "Formal Trousers", "Dress"],
            "matching_colors": colors,
            "avoid_types":     ["Blazers", "Blazer", "Jacket", "Cardigan", "Coat",
                                 "Sweaters", "Hoodie"],
            "pairing_note":    "Layer pieces pair with bottoms or over dresses.",
            "pairing_category": "Outfit",
        }

    # Tops → bottoms (but not other tops)
    if any(x in t for x in ['shirt', 'blouse', 'top', 'sweater', 'hoodie', 'tee', 't-shirt']):
        avoid = ["Blazers", "Blazer", "Jacket", "Cardigan", "Coat",
                 "Shirt", "Blouse", "Sweaters", "Hoodie", "Top", "T-Shirt"]
        return {
            "matching_types":  ["Jeans", "Trousers", "Chinos", "Skirt", "Shorts",
                                 "Leggings", "Formal Trousers", "Pants"],
            "matching_colors": colors,
            "avoid_types":     avoid,
            "pairing_note":    "Tops pair with bottoms.",
            "pairing_category": "Outfit",
        }

    # Bottoms → tops (but not other bottoms)
    if any(x in t for x in ['jean', 'trouser', 'skirt', 'short', 'legging', 'pant', 'chino']):
        avoid = ["Jeans", "Trousers", "Skirt", "Shorts", "Leggings", "Pants",
                 "Chinos", "Formal Trousers"]
        return {
            "matching_types":  ["T-Shirts", "Casual Shirt", "Blouse", "Tops",
                                 "Sweaters", "Hoodies", "Formal Shirt", "Blazers"],
            "matching_colors": colors,
            "avoid_types":     avoid,
            "pairing_note":    "Bottoms pair with tops.",
            "pairing_category": "Outfit",
        }

    # Dresses / jumpsuits → only layer pieces
    if any(x in t for x in ['dress', 'jumpsuit', 'romper']):
        return {
            "matching_types":  ["Blazers", "Blazer", "Cardigan", "Jacket"],
            "matching_colors": colors,
            "avoid_types":     ["Dress", "Gown", "Jumpsuit", "Romper"],
            "pairing_note":    "Add a blazer or cardigan over a dress.",
            "pairing_category": "Outfit",
        }

    # Traditional → traditional only
    if any(x in t for x in ['saree', 'sari', 'kurta', 'lehenga', 'sherwani', 'salwar']):
        return {
            "matching_types":  ETHNIC_TOPS + ETHNIC_BOTTOMS,
            "matching_colors": colors,
            "avoid_types":     ["Saree", "Sari"] if "saree" in t or "sari" in t else [],
            "pairing_note":    "Traditional items pair with other ethnic pieces.",
            "pairing_category": "Traditional Wear",
        }

    # Default fallback
    return {
        "matching_types":  ["T-Shirts", "Jeans", "Casual Shirt", "Trousers", "Skirt"],
        "matching_colors": colors,
        "avoid_types":     [],
        "pairing_note":    "A versatile piece — pair with most wardrobe staples.",
        "pairing_category": "Outfit",
    }