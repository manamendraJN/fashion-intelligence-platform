# Event-Based Clothing Pairing System

## Overview
This document explains the **Rule-Based Event Context Pairing System** implemented in the Fashion Intelligence Platform. The system provides context-aware clothing recommendations based on the event type (Office, Office Meeting, Casual, etc.).

---

## 🎯 Features

### 1. **Event-Specific Pairing Rules**
The system now considers the **event context** when recommending clothing pairs:

- **Office**: Professional but slightly relaxed (jeans allowed with formal tops)
- **Office Meeting**: Strictly formal attire (blazers, pencil skirts, dress shirts)
- **Casual**: Comfortable, relaxed clothing (T-shirts, shorts, casual skirts)
- **Party**: Dressy items with optional layering
- **Gym/Sports**: Athletic wear only

### 2. **"Office Meeting" as Separate Event**
Added **"Office Meeting"** as a distinct event type from general **"Office"**:
- More formal dress code requirements
- Blazers recommended for important meetings
- Stricter pairing rules

### 3. **Smart Avoidance System**
The system now **excludes inappropriate items** based on event context:
- ❌ No T-shirts with office jeans
- ❌ No casual wear for office meetings
- ❌ No pencil skirts for casual outings

---

## 📋 Pairing Rules by Event

### **OFFICE** (Professional but flexible)

| Selected Item | Recommended Pairings | ❌ Avoid |
|---------------|---------------------|----------|
| **Jeans** | Blouse, Formal Shirt, Blazers | T-shirts, Tank Tops, Hoodies |
| **Trousers** | Blouse, Formal Shirt, Blazers | T-shirts, Tank Tops |
| **Pencil Skirt** | Blouse, Formal Shirt, Button-down | T-shirts, Crop Tops |
| **Blouse** | Trousers, Pencil Skirt, Jeans | Shorts, Mini Skirt, Leggings |

### **OFFICE MEETING** (Strictly formal)

| Selected Item | Recommended Pairings | ❌ Avoid |
|---------------|---------------------|----------|
| **Pencil Skirt** | Blouse, Formal Shirt, Blazers | T-shirts, Casual Shirts |
| **Blazers** | Blouse, Tank Top, Pencil Skirt, Trousers | T-shirts, Shorts, Jeans |
| **Trousers** | Blouse, Formal Shirt, Blazers | T-shirts, Casual Tops |
| **Blouse** | Formal Trousers, Pencil Skirt, Blazers | Jeans, Shorts, Leggings |

### **CASUAL** (Relaxed & comfortable)

| Selected Item | Recommended Pairings | ❌ Avoid |
|---------------|---------------------|----------|
| **Jeans** | T-shirts, Tank Tops, Casual Shirt, Sweaters | Formal Shirts |
| **T-shirts** | Jeans, Shorts, Casual Skirts, Leggings | Pencil Skirts, Formal Trousers |
| **Skirts** (excluding pencil) | T-shirts, Tank Tops, Casual Shirts | — |
| **Shorts** | T-shirts, Tank Tops, Casual Shirts | Blazers, Formal Shirts |

### **PARTY** (Dressy with layering)

| Selected Item | Recommended Pairings |
|---------------|---------------------|
| **Formal Dress** | Blazers, Cardigan (optional) |
| **Cocktail Dress** | Blazers, Cardigan (optional) |
| **Skirts** | Blouse, Crop Top, Tank Top |

---

## 🔧 Technical Implementation

### Backend Changes

#### 1. **New Function: `get_event_based_pairing()`**
**File:** `backend/utils/color_utils.py`

```python
def get_event_based_pairing(item_type, item_color, event_type=None):
    """
    Get clothing pairing recommendations based on event type
    
    Args:
        item_type: Type of clothing (e.g., "Jeans", "Blouse")
        item_color: Color of the item
        event_type: Event context (e.g., "Office", "Office Meeting", "Casual")
    
    Returns:
        Dictionary with:
        - matching_types: List of recommended clothing types
        - matching_colors: List of compatible colors
        - avoid_types: List of inappropriate types for this event
        - pairing_note: Explanation of the rule
        - event_type: The event context used
    """
```

#### 2. **Updated API Endpoint: `/api/outfit-pairing/<item_id>`**
**File:** `backend/routes/wardrobe_routes.py`

Now accepts optional `event_type` query parameter:

```http
GET /api/outfit-pairing/123?event_type=Office Meeting
```

**Response includes:**
```json
{
  "success": true,
  "item": {
    "id": 123,
    "type": "Pencil Skirt",
    "color": "Black"
  },
  "matches": [...],
  "matchingTypes": ["Blouse", "Formal Shirt", "Blazers"],
  "avoidTypes": ["Tshirts", "Tank Top"],
  "pairingNote": "Strictly professional tops for important meetings",
  "eventType": "Office Meeting"
}
```

#### 3. **Event Constants Updated**
**File:** `backend/core/event_constants.py`

Added "Office Meeting" to standard events:
```python
STANDARD_EVENTS = [
    "Casual",
    "Office",
    "Office Meeting",  # ✨ New
    "Party",
    ...
]
```

---

### Frontend Changes

#### 1. **Chat Page Event Categories**
**File:** `frontend/src/pages/Chat.jsx`

Added "Office Meeting" event chip:
```jsx
{
  label: 'Work & Daily',
  events: [
    { name: 'Office',         icon: '💼', ... },
    { name: 'Office Meeting', icon: '🎯', ... }, // ✨ New
    { name: 'Interview',      icon: '📋', ... },
    ...
  ]
}
```

#### 2. **Event Extraction Logic**
Updated `extractOccasionOrActivity()` to distinguish between "Office" and "Office Meeting":
```javascript
// Check for "office meeting" BEFORE general "office"
if (t.includes('office meeting')) return { value: 'Office Meeting', ... };
if (t.includes('office')) return { value: 'Office', ... };
```

---

## 🧪 Testing

Run the test script to see event-based pairing in action:

```bash
python test_event_pairing.py
```

**Example Output:**
```
🎯 Event: Office
👕 Item: Blue Jeans
────────────────────────────────────────────
📌 Note: Office-appropriate tops only (no T-shirts)

✅ RECOMMENDED PAIRINGS:
   • Blouse
   • Formal Shirt
   • Blazers

❌ AVOID (Not Appropriate for Office):
   • Tshirts
   • Tank Top
   • Hoodies
```

---

## 📊 Examples

### Example 1: Office Jeans
**User selects:** Blue Jeans + Office event

**System recommends:**
- ✅ Blouse (professional)
- ✅ Formal Shirt (appropriate)
- ✅ Blazers (elevated look)
- ❌ **NOT T-shirts** (too casual for office)

### Example 2: Pencil Skirt for Meeting
**User selects:** Black Pencil Skirt + Office Meeting event

**System recommends:**
- ✅ Blouse (professional)
- ✅ Formal Shirt (meeting-appropriate)
- ✅ Blazers (powerful look)
- ❌ **NOT Casual Tops** (not formal enough)

### Example 3: Casual Jeans
**User selects:** Blue Jeans + Casual event

**System recommends:**
- ✅ T-shirts (relaxed)
- ✅ Tank Tops (summer casual)
- ✅ Sweaters (cozy casual)
- No strict avoidances (very flexible)

### Example 4: Dress Pairing
**User selects:** Formal Dress + Any event

**System recommends:**
- ✅ Blazers (professional layering)
- ✅ Cardigan (elegant layering)
- Works as standalone or with "pair tag" items

### Example 5: Blazers for Meeting
**User selects:** Blazers + Office Meeting

**System recommends:**
- ✅ Blouse (under blazer)
- ✅ Tank Top (layered look)
- ✅ Pencil Skirt (bottom pairing)
- ✅ Formal Trousers (professional)

---

## 🎨 Color Matching Still Active

The system **still uses color theory** in combination with event rules:

- **Blue Jeans** will match with:
  - White Blouse (neutral + blue)
  - Black Formal Shirt (neutral + blue)
  - Cream Blazer (warm neutral + cool blue)

- **Black Pencil Skirt** will match with:
  - White Blouse (high contrast)
  - Light Pink Blouse (soft contrast)
  - Gold accessories (luxe pairing)

---

## 🚀 How to Use

### In Chat Interface:
1. User clicks **"Office Meeting"** event chip
2. System shows appropriate clothing items
3. User clicks an item (e.g., Pencil Skirt)
4. System recommends **event-appropriate** pairings (Blouse, Blazers, NOT T-shirts)

### In API:
```javascript
fetch(`/api/outfit-pairing/123?event_type=Office Meeting`)
  .then(res => res.json())
  .then(data => {
    console.log(data.matchingTypes);  // ["Blouse", "Formal Shirt", "Blazers"]
    console.log(data.avoidTypes);      // ["Tshirts", "Tank Top"]
  });
```

---

## ✅ Benefits

1. **Context-Aware:** Recommendations change based on where you're going
2. **Prevents Mistakes:** System won't suggest T-shirts with office jeans
3. **Flexible yet Strict:** Casual allows everything, Office Meeting is very formal
4. **User Education:** Pairing notes explain WHY certain combinations work
5. **Scalable:** Easy to add new events (Wedding, Gym, Beach, etc.)

---

## 📝 Next Steps

### Potential Enhancements:
1. **Weather Integration:** "Blazer for cold office meeting"
2. **Time of Day:** "Morning meeting vs. After-work casual"
3. **User Preferences:** Learn individual formality preferences
4. **Pattern Mixing:** "Striped shirt + solid skirt"
5. **Accessory Recommendations:** "Add statement necklace for party"

---

## 🎯 Summary

| Before | After |
|--------|-------|
| ❌ Jeans + Office → suggests T-shirts | ✅ Jeans + Office → suggests Blouse, Formal Shirt |
| ❌ No distinction between Office & Meeting | ✅ "Office Meeting" as separate, formal event |
| ❌ Only color-based matching | ✅ Event context + color matching |
| ❌ No avoidance system | ✅ System excludes inappropriate items |

**Result:** Intelligent, context-aware clothing recommendations that help users dress appropriately for any occasion! 🎉
