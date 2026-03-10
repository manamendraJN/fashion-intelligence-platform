"""
event_constants.py
==================
SCORE PHILOSOPHY
----------------
Each clothing type has 1-2 "home" occasions scoring 0.90+.
All other occasions score realistically lower.
Threshold in wardrobe_routes is 0.60 — items below are NEVER shown.

WHAT SHOWS WHERE (summary):
  Family Gathering  → Kurtas, Salwars, Casual Dresses, Maxi Dresses, Chinos, Casual Shirts, Sarees
  Funeral           → Black/white/dark items only (color-filtered in routes) + formal items
  Office/Meeting    → Blazers, Blouses, Formal Shirts, Pencil Skirts, Formal Trousers
  Casual            → T-shirts, Jeans, Hoodies, Casual Dresses, Shorts
  Tamil Wedding     → Sarees, Lehengas, Kurtas, Sherwanis
  Date Night        → Cocktail Dresses, Formal Dresses, Maxi Dresses, Midi Dresses
  Party             → Formal Dresses, Lehengas, Jumpsuits
  Gym/Sports        → Athletic items ONLY
  Beach             → Swimwear, Shorts, Sundresses
"""

STANDARD_EVENTS = [
    "Casual",
    "Office",
    "Office Meeting",
    "Party",
    "Gym",
    "Beach",
    "Date",
    "Shopping",
    "Sports",
    "Religious",
    "Tamil Wedding",
    "Western Wedding",
    "Family Gathering",
    "Funeral",
]

EVENT_NAME_MAPPING = {
    # Casual
    "casual": "Casual", "casual outing": "Casual", "weekend": "Casual",
    "hangout": "Casual", "relax": "Casual", "chill": "Casual",
    "outing": "Casual", "travel": "Casual", "lunch": "Casual", "brunch": "Casual",
    # Office
    "office": "Office", "work": "Office", "professional": "Office",
    "business": "Office",
    # Office Meeting — interview maps here (most formal)
    "office meeting": "Office Meeting", "meeting": "Office Meeting",
    "business meeting": "Office Meeting", "important meeting": "Office Meeting",
    "interview": "Office Meeting",
    # Party
    "party": "Party", "celebration": "Party", "night out": "Party", "clubbing": "Party",
    # Date
    "date": "Date", "date night": "Date", "dinner": "Date", "romantic": "Date",
    # Beach
    "beach": "Beach", "beach outing": "Beach", "pool": "Beach", "swimming": "Beach",
    # Shopping
    "shopping": "Shopping", "mall": "Shopping", "shopping mall": "Shopping",
    # Gym / Sports
    "gym": "Gym", "workout": "Gym", "exercise": "Gym", "fitness": "Gym",
    "yoga": "Gym", "pilates": "Gym",
    "sports": "Sports", "running": "Sports", "jogging": "Sports",
    "hiking": "Sports", "outdoor": "Sports", "athletic": "Sports",
    # Religious
    "religious": "Religious", "temple": "Religious",
    "church": "Religious", "mosque": "Religious",
    # Weddings
    "tamil wedding": "Tamil Wedding", "traditional wedding": "Tamil Wedding",
    "indian wedding": "Tamil Wedding", "ethnic wedding": "Tamil Wedding",
    "western wedding": "Western Wedding", "church wedding": "Western Wedding",
    # Family
    "family": "Family Gathering", "family gathering": "Family Gathering",
    "family event": "Family Gathering", "reunion": "Family Gathering",
    # Funeral
    "funeral": "Funeral", "condolence": "Funeral",
    "memorial": "Funeral", "mourning": "Funeral", "wake": "Funeral",
}


def normalize_event_name(event_name):
    if not event_name:
        return "Casual"
    normalized = event_name.lower().strip()
    if normalized in EVENT_NAME_MAPPING:
        return EVENT_NAME_MAPPING[normalized]
    for standard_event in STANDARD_EVENTS:
        if standard_event.lower() == normalized:
            return standard_event
    return event_name


def find_event_score(event_scores_dict, target_event):
    if not event_scores_dict:
        return 0.0
    normalized_target = normalize_event_name(target_event)
    # Direct key match
    if normalized_target in event_scores_dict:
        return event_scores_dict[normalized_target]
    # Normalise all stored keys and compare
    for db_event_name, score in event_scores_dict.items():
        if normalize_event_name(db_event_name) == normalized_target:
            return score
    return 0.0


def _scores(
    Casual=0.0, Office=0.0, Meeting=0.0, Party=0.0,
    Gym=0.0, Beach=0.0, Date=0.0, Shopping=0.0, Sports=0.0,
    Religious=0.0, TamilWedding=0.0, WesternWedding=0.0,
    FamilyGathering=0.0, Funeral=0.0,
):
    """Helper to build score dict with named args for readability."""
    return {
        "Casual": Casual, "Office": Office, "Office Meeting": Meeting,
        "Party": Party, "Gym": Gym, "Beach": Beach,
        "Date": Date, "Shopping": Shopping, "Sports": Sports,
        "Religious": Religious, "Tamil Wedding": TamilWedding,
        "Western Wedding": WesternWedding,
        "Family Gathering": FamilyGathering, "Funeral": Funeral,
    }


def get_default_event_scores(clothing_type):
    """
    Returns {event: score} for all 14 standard events.
    Scores below 0.60 are NEVER shown to the user (filtered in wardrobe_routes).

    Key rules enforced here:
    • Blazers/Pencil Skirts/Formal Shirts  → Office only (Family Gathering = 0.25)
    • T-shirts/Jeans/Hoodies               → Casual only (Office = 0.0)
    • Sarees/Lehengas/Kurtas               → Traditional occasions only
    • Dresses (generic)                    → Date/Party (NOT Family Gathering unless Casual/Maxi)
    • Casual Dresses/Maxi/Midi             → Family Gathering ✓
    • Funeral                              → formal + dark-colored items (color filter in routes)
    """
    t = clothing_type.lower().strip()

    # ── SWIMWEAR ─────────────────────────────────────────────────────────────
    if any(w in t for w in [
        'swimwear', 'bikini', 'swimsuit', 'swim suit',
        'one-piece swim', 'swim short', 'swim trunk', 'bathing suit'
    ]):
        return _scores(Casual=0.30, Beach=0.98, Gym=0.20, Sports=0.40)

    # ── ATHLETIC / GYM WEAR ──────────────────────────────────────────────────
    if any(w in t for w in [
        'gym wear', 'sports bra', 'yoga pant', 'athletic short',
        'tracksuit', 'track pant', 'jogger'
    ]):
        return _scores(Casual=0.50, Gym=0.95, Beach=0.35, Shopping=0.40, Sports=0.95)

    # ── BLAZERS / SUIT JACKETS ───────────────────────────────────────────────
    # Home: Office, Office Meeting, Western Wedding
    # Family Gathering = 0.25 (below threshold → NEVER shown there)
    if any(w in t for w in ['blazer', 'suit jacket', 'formal coat', 'tuxedo']):
        return _scores(
            Casual=0.20, Office=0.95, Meeting=0.98,
            Party=0.60, Date=0.62, Shopping=0.22, Religious=0.50,
            TamilWedding=0.28, WesternWedding=0.95,
            FamilyGathering=0.25,   # ← BELOW threshold, won't appear
            Funeral=0.72,           # dark blazers are appropriate
        )

    # ── FORMAL / COCKTAIL / EVENING GOWN ────────────────────────────────────
    if any(w in t for w in ['formal dress', 'evening gown', 'gown', 'cocktail dress']):
        return _scores(
            Office=0.35, Meeting=0.40,
            Party=0.95, Date=0.95, Religious=0.42,
            TamilWedding=0.45, WesternWedding=0.95,
            FamilyGathering=0.40,   # borderline, below threshold
            Funeral=0.65,
        )

    # ── FORMAL SHIRT / DRESS SHIRT / BUTTON-DOWN ────────────────────────────
    if any(w in t for w in ['formal shirt', 'dress shirt', 'button-down', 'button down']):
        return _scores(
            Casual=0.38, Office=0.95, Meeting=0.95,
            Party=0.42, Date=0.52, Shopping=0.42, Religious=0.50,
            TamilWedding=0.22, WesternWedding=0.58,
            FamilyGathering=0.32,   # below threshold
            Funeral=0.65,
        )

    # ── BLOUSE ───────────────────────────────────────────────────────────────
    if 'blouse' in t:
        return _scores(
            Casual=0.48, Office=0.88, Meeting=0.90,
            Party=0.50, Date=0.62, Shopping=0.58, Religious=0.50,
            TamilWedding=0.28, WesternWedding=0.50,
            FamilyGathering=0.42,   # below threshold
            Funeral=0.55,
        )

    # ── PENCIL SKIRT ─────────────────────────────────────────────────────────
    if 'pencil skirt' in t:
        return _scores(
            Casual=0.20, Office=0.95, Meeting=0.95,
            Party=0.52, Date=0.62, Shopping=0.32, Religious=0.32,
            TamilWedding=0.10, WesternWedding=0.48,
            FamilyGathering=0.18,   # below threshold
            Funeral=0.60,
        )

    # ── A-LINE SKIRT ─────────────────────────────────────────────────────────
    if 'a-line skirt' in t or 'a line skirt' in t:
        return _scores(
            Casual=0.58, Office=0.80, Meeting=0.75,
            Party=0.62, Date=0.80, Shopping=0.75, Religious=0.45,
            TamilWedding=0.18, WesternWedding=0.52,
            FamilyGathering=0.50,   # borderline
            Funeral=0.48,
        )

    # ── MIDI / MAXI SKIRT ────────────────────────────────────────────────────
    if 'midi skirt' in t or 'maxi skirt' in t:
        return _scores(
            Casual=0.85, Office=0.52, Meeting=0.42,
            Party=0.62, Date=0.80, Shopping=0.88,
            Religious=0.60, TamilWedding=0.28, WesternWedding=0.48,
            FamilyGathering=0.82,   # ✓ great for family gathering
            Funeral=0.40,
        )

    # ── DENIM SKIRT ──────────────────────────────────────────────────────────
    if 'denim skirt' in t:
        return _scores(
            Casual=0.92, Beach=0.58, Date=0.58, Shopping=0.90,
            FamilyGathering=0.45,
        )

    # ── MINI SKIRT ───────────────────────────────────────────────────────────
    if 'mini skirt' in t:
        return _scores(
            Casual=0.88, Party=0.80, Beach=0.68, Date=0.80, Shopping=0.85,
            FamilyGathering=0.35,   # below threshold
        )

    # ── GENERIC SKIRT ────────────────────────────────────────────────────────
    if 'skirt' in t:
        return _scores(
            Casual=0.70, Office=0.52, Meeting=0.48,
            Party=0.62, Date=0.70, Shopping=0.78, Religious=0.30,
            FamilyGathering=0.58,
        )

    # ── CIGARETTE PANTS ──────────────────────────────────────────────────────
    if 'cigarette pant' in t:
        return _scores(
            Casual=0.32, Office=0.95, Meeting=0.95,
            Party=0.55, Date=0.68, Shopping=0.48,
            Religious=0.40, WesternWedding=0.62,
            FamilyGathering=0.22,   # below threshold
            Funeral=0.65,
        )

    # ── FORMAL TROUSERS / DRESS PANTS ────────────────────────────────────────
    if any(w in t for w in ['formal trouser', 'dress pant', 'formal pant']):
        return _scores(
            Casual=0.30, Office=0.95, Meeting=0.95,
            Party=0.52, Date=0.60, Shopping=0.40, Religious=0.50,
            TamilWedding=0.25, WesternWedding=0.68,
            FamilyGathering=0.22,   # below threshold
            Funeral=0.70,
        )

    # ── CHINOS ───────────────────────────────────────────────────────────────
    # Smart casual — perfect for Family Gathering
    if 'chino' in t:
        return _scores(
            Casual=0.85, Office=0.78, Meeting=0.65,
            Party=0.45, Date=0.65, Shopping=0.88, Sports=0.10,
            Religious=0.45, TamilWedding=0.15, WesternWedding=0.52,
            FamilyGathering=0.82,   # ✓
            Funeral=0.52,
        )

    # ── GENERIC TROUSERS / PANTS (not track/yoga/cargo/cigarette/formal) ────
    if (any(w in t for w in ['trouser', 'pant'])
            and not any(w in t for w in ['track', 'yoga', 'cargo', 'cigarette', 'dress pant', 'formal'])):
        return _scores(
            Casual=0.70, Office=0.70, Meeting=0.62,
            Party=0.45, Date=0.60, Shopping=0.75, Sports=0.10,
            Religious=0.45, WesternWedding=0.50,
            FamilyGathering=0.70,   # ✓
            Funeral=0.52,
        )

    # ── CARGO PANTS ──────────────────────────────────────────────────────────
    if 'cargo' in t:
        return _scores(
            Casual=0.92, Beach=0.42, Shopping=0.85, Sports=0.58,
            FamilyGathering=0.40,
        )

    # ── JEANS ────────────────────────────────────────────────────────────────
    if 'jean' in t:
        return _scores(
            Casual=0.95, Date=0.65, Shopping=0.95,
            Beach=0.32, Sports=0.12,
            FamilyGathering=0.68,   # ✓ jeans OK for casual family gathering
        )

    # ── LEGGINGS ─────────────────────────────────────────────────────────────
    if 'legging' in t:
        return _scores(
            Casual=0.80, Gym=0.88, Beach=0.30, Shopping=0.68, Sports=0.85,
            FamilyGathering=0.35,
        )

    # ── SHORTS ───────────────────────────────────────────────────────────────
    if 'short' in t:
        if 'bermuda' in t:
            return _scores(
                Casual=0.88, Beach=0.82, Shopping=0.85, Sports=0.52,
                FamilyGathering=0.55,
            )
        if 'denim' in t:
            return _scores(
                Casual=0.92, Beach=0.88, Shopping=0.90, Date=0.58,
                FamilyGathering=0.38,
            )
        # Generic shorts
        return _scores(
            Casual=0.88, Beach=0.92, Shopping=0.78, Gym=0.38, Sports=0.65,
            FamilyGathering=0.30,
        )

    # ── POLO SHIRT ───────────────────────────────────────────────────────────
    if 'polo' in t:
        return _scores(
            Casual=0.85, Office=0.62, Meeting=0.50,
            Shopping=0.82, Sports=0.65, Religious=0.38,
            FamilyGathering=0.75,   # ✓
        )

    # ── T-SHIRT / TANK TOP / CROP TOP ────────────────────────────────────────
    if any(w in t for w in ['t-shirt', 'tshirt', 'tank top', 'crop top']):
        return _scores(
            Casual=0.95, Beach=0.80, Shopping=0.92, Gym=0.38, Sports=0.52,
            FamilyGathering=0.60,   # ✓ light/plain tshirts OK
        )

    # ── CASUAL SHIRT ─────────────────────────────────────────────────────────
    if 'casual shirt' in t:
        return _scores(
            Casual=0.90, Date=0.60, Shopping=0.88, Beach=0.42, Sports=0.12,
            Religious=0.30, TamilWedding=0.10,
            FamilyGathering=0.78,   # ✓
        )

    # ── GENERIC SHIRT (not t-shirt / casual) ─────────────────────────────────
    if 'shirt' in t and not any(w in t for w in ['t-shirt', 'tshirt', 'sweat', 'casual']):
        return _scores(
            Casual=0.65, Office=0.80, Meeting=0.75,
            Party=0.42, Date=0.60, Shopping=0.70, Religious=0.48,
            WesternWedding=0.48, FamilyGathering=0.62,   # ✓
            Funeral=0.55,
        )

    # ── HOODIES / SWEATSHIRTS ────────────────────────────────────────────────
    if any(w in t for w in ['hoodie', 'sweatshirt']):
        return _scores(
            Casual=0.90, Shopping=0.80, Gym=0.30, Sports=0.32,
            FamilyGathering=0.52,
        )

    # ── SWEATERS / CARDIGANS ─────────────────────────────────────────────────
    if any(w in t for w in ['sweater', 'cardigan']):
        return _scores(
            Casual=0.88, Shopping=0.82, Date=0.45,
            FamilyGathering=0.85,   # ✓ cosy — great for family gathering
        )

    # ── TOPS / TUNICS ────────────────────────────────────────────────────────
    if any(w in t for w in ['top', 'tunic']):
        return _scores(
            Casual=0.80, Office=0.55, Meeting=0.45,
            Party=0.55, Date=0.62, Shopping=0.80,
            FamilyGathering=0.68,   # ✓
        )

    # ── MAXI DRESS / MIDI DRESS ──────────────────────────────────────────────
    if 'maxi dress' in t or 'midi dress' in t:
        return _scores(
            Casual=0.88, Party=0.70, Beach=0.62, Date=0.88, Shopping=0.88,
            Religious=0.52, TamilWedding=0.35, WesternWedding=0.58,
            FamilyGathering=0.90,   # ✓ excellent for family gathering
            Funeral=0.35,
        )

    # ── SUNDRESS ─────────────────────────────────────────────────────────────
    if 'sundress' in t:
        return _scores(
            Casual=0.92, Beach=0.85, Date=0.75, Shopping=0.90, Party=0.58,
            FamilyGathering=0.72,   # ✓
        )

    # ── SHIRT DRESS ──────────────────────────────────────────────────────────
    if 'shirt dress' in t or 'shirtdress' in t:
        return _scores(
            Casual=0.78, Office=0.78, Meeting=0.65,
            Date=0.68, Shopping=0.82,
            FamilyGathering=0.70,   # ✓
            Funeral=0.32,
        )

    # ── CASUAL DRESS ─────────────────────────────────────────────────────────
    if 'casual dress' in t:
        return _scores(
            Casual=0.92, Beach=0.60, Date=0.82, Shopping=0.88, Party=0.62,
            FamilyGathering=0.88,   # ✓ ideal for family gathering
        )

    # ── GENERIC DRESS ────────────────────────────────────────────────────────
    # NOTE: generic "Dresses" score 0.40 for Family Gathering → below threshold
    # This is intentional: user should own Casual Dress / Maxi Dress for family use
    if 'dress' in t:
        return _scores(
            Casual=0.65, Office=0.38, Meeting=0.32,
            Party=0.78, Date=0.88, Shopping=0.72, Beach=0.45,
            Religious=0.38, TamilWedding=0.28, WesternWedding=0.62,
            FamilyGathering=0.45,   # borderline – won't appear unless nothing else
            Funeral=0.38,
        )

    # ── JUMPSUIT / ROMPER ────────────────────────────────────────────────────
    if 'jumpsuit' in t or 'romper' in t:
        return _scores(
            Casual=0.82, Party=0.70, Beach=0.50, Date=0.78, Shopping=0.85,
            FamilyGathering=0.62,   # ✓
        )

    # ── DENIM / LEATHER / PUFFER JACKET ─────────────────────────────────────
    if any(w in t for w in ['denim jacket', 'leather jacket', 'puffer jacket', 'puffer']):
        return _scores(
            Casual=0.92, Party=0.55, Date=0.62, Shopping=0.88,
            FamilyGathering=0.68,   # ✓ casual jacket fine for family
        )

    # ── GENERIC JACKET / COAT (non-blazer) ──────────────────────────────────
    if any(w in t for w in ['jacket', 'coat']) and not any(w in t for w in ['blazer', 'suit']):
        return _scores(
            Casual=0.78, Office=0.48, Meeting=0.40,
            Party=0.45, Date=0.58, Shopping=0.72,
            FamilyGathering=0.65,   # ✓
            Funeral=0.42,
        )

    # ════════════════════════ TRADITIONAL ════════════════════════════════════

    # ── WEDDING / BRIDAL SAREE ───────────────────────────────────────────────
    if 'wedding saree' in t or 'bridal saree' in t:
        return _scores(
            Party=0.58, Religious=0.52,
            TamilWedding=0.98,      # ✓✓ top item
            FamilyGathering=0.65,
        )

    # ── SILK / TRADITIONAL SAREE ─────────────────────────────────────────────
    if 'traditional saree' in t or 'silk saree' in t:
        return _scores(
            Party=0.45, Religious=0.95,
            TamilWedding=0.88,
            FamilyGathering=0.88,   # ✓
        )

    # ── OFFICE / FORMAL SAREE ────────────────────────────────────────────────
    if 'office saree' in t or 'formal saree' in t:
        return _scores(
            Casual=0.40, Office=0.90, Meeting=0.85,
            Date=0.52, Shopping=0.48, Religious=0.40,
            FamilyGathering=0.58,
        )

    # ── CASUAL / COTTON SAREE ────────────────────────────────────────────────
    if 'casual saree' in t or 'cotton saree' in t:
        return _scores(
            Casual=0.82, Office=0.50, Meeting=0.40,
            Shopping=0.78, Religious=0.32,
            FamilyGathering=0.82,   # ✓
        )

    # ── GENERIC SAREE ────────────────────────────────────────────────────────
    if 'saree' in t or 'sari' in t:
        return _scores(
            Party=0.45, Religious=0.82,
            TamilWedding=0.82,
            FamilyGathering=0.80,   # ✓
        )

    # ── SILK / TRADITIONAL KURTA ─────────────────────────────────────────────
    if 'traditional kurta' in t or 'silk kurta' in t:
        return _scores(
            Party=0.50, Date=0.42, Religious=0.95,
            TamilWedding=0.85,
            FamilyGathering=0.88,   # ✓
        )

    # ── CASUAL / COTTON KURTA ────────────────────────────────────────────────
    if 'casual kurta' in t or 'cotton kurta' in t:
        return _scores(
            Casual=0.88, Office=0.50, Meeting=0.38,
            Shopping=0.82, Religious=0.32,
            FamilyGathering=0.85,   # ✓
        )

    # ── GENERIC KURTA / KURTI ────────────────────────────────────────────────
    if 'kurta' in t or 'kurti' in t:
        return _scores(
            Casual=0.60, Office=0.40, Meeting=0.30,
            Party=0.48, Shopping=0.62, Religious=0.72,
            TamilWedding=0.68,
            FamilyGathering=0.88,   # ✓ BEST item for family gathering
        )

    # ── WEDDING / BRIDAL LEHENGA ─────────────────────────────────────────────
    if 'wedding lehenga' in t or 'bridal lehenga' in t:
        return _scores(
            Party=0.62, Religious=0.50,
            TamilWedding=0.98,
            WesternWedding=0.30,
            FamilyGathering=0.68,
        )

    # ── GENERIC LEHENGA ──────────────────────────────────────────────────────
    if 'lehenga' in t:
        return _scores(
            Party=0.85, Date=0.60, Religious=0.58,
            TamilWedding=0.90,
            WesternWedding=0.42,
            FamilyGathering=0.78,   # ✓
        )

    # ── SHERWANI ─────────────────────────────────────────────────────────────
    if 'sherwani' in t:
        return _scores(
            Party=0.60, Religious=0.88,
            TamilWedding=0.95,
            WesternWedding=0.55,
            FamilyGathering=0.78,   # ✓
        )

    # ── SALWAR / PATIALA / CHURIDAR ──────────────────────────────────────────
    if any(w in t for w in ['salwar', 'patiala', 'churidar']):
        return _scores(
            Casual=0.82, Office=0.50, Meeting=0.38,
            Party=0.50, Shopping=0.80, Religious=0.72,
            TamilWedding=0.52,
            FamilyGathering=0.88,   # ✓
        )

    # ── DEFAULT ──────────────────────────────────────────────────────────────
    return _scores(
        Casual=0.60, Office=0.38, Meeting=0.30,
        Party=0.38, Shopping=0.60,
        FamilyGathering=0.55,
    )