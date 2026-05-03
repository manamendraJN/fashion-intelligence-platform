# Tolerance and Weights Configuration Guide

## Current Implementation

Your system uses **two-level weights**:

### 1. Base Tolerance and Weight (Per Measurement)
**Location**: `backend/database/db_manager.py` - Lines 271-274

```python
'optimal': (min_val + max_val) / 2 if min_val and max_val else None,
'tolerance': 2.0,  # ← DEFAULT TOLERANCE (2 cm)
'weight': 1.0      # ← BASE WEIGHT (neutral)
```

**What this means**:
- Every measurement gets a **2.0 cm tolerance** (how far outside the size range is acceptable)
- Every measurement starts with a **1.0 weight** (neutral importance)

---

### 2. Category Importance Weights (Multiplied with base weight)
**Location**: `backend/database/db_manager.py` - Lines 291-348

```python
def get_category_measurement_requirements(self, category_id: int):
```

**Weights by Category**:

| Category | Measurement | Importance Weight | Required |
|----------|-------------|-------------------|----------|
| **T-Shirt/Polo** | chest | 1.0 | ✓ |
| | shoulder_breadth | 0.8 | ✗ |
| | waist | 0.6 | ✗ |
| **Shirt** | chest | 1.0 | ✓ |
| | shoulder_breadth | 0.8 | ✗ |
| | sleeve_length | 0.7 | ✗ |
| | waist | 0.6 | ✗ |
| **Hoodie** | chest | 1.0 | ✓ |
| | shoulder_breadth | 0.8 | ✗ |
| | waist | 0.7 | ✗ |
| **Sweater** | chest | 1.0 | ✓ |
| | shoulder_breadth | 0.8 | ✗ |
| | sleeve_length | 0.7 | ✗ |
| | waist | 0.7 | ✗ |
| **Shorts** | waist | 1.0 | ✓ |
| | hip | 0.9 | ✓ |
| | leg_length | 0.5 | ✗ |
| **Jeans/Pants** | waist | 1.0 | ✓ |
| | hip | 0.9 | ✓ |
| | leg_length | 0.7 | ✗ |
| **Dress/Skirt** | chest | 1.0 | ✓ |
| | waist | 1.0 | ✓ |
| | hip | 0.9 | ✓ |
| **Jacket/Coat** | chest | 1.0 | ✓ |
| | shoulder_breadth | 0.9 | ✓ |
| | arm_length | 0.8 | ✗ |

---

## How To Customize

### Option A: Change Default Tolerance (Quick)

Edit line 273 in `db_manager.py`:
```python
'tolerance': 3.0,  # Change from 2.0 to 3.0 cm for more flexibility
```

### Option B: Change Category Importance Weights

Edit lines 315-370 in `db_manager.py`:
```python
# Example: Make shoulder more important for T-shirts
if 't-shirt' in category_name:
    return [
        {'measurement_type': 'chest', 'importance_weight': 1.0, 'is_required': True},
        {'measurement_type': 'shoulder_breadth', 'importance_weight': 0.9, 'is_required': True},  # ← Changed from 0.8
        {'measurement_type': 'waist', 'importance_weight': 0.6, 'is_required': False}
    ]

# Example: Make leg_length less important for shorts (already set to 0.5)
elif 'shorts' in category_name:
    return [
        {'measurement_type': 'waist', 'importance_weight': 1.0, 'is_required': True},
        {'measurement_type': 'hip', 'importance_weight': 0.9, 'is_required': True},
        {'measurement_type': 'leg_length', 'importance_weight': 0.3, 'is_required': False}  # ← Changed from 0.5
    ]
```

### Option C: Add Per-Measurement Tolerance (Advanced)

You could modify the code to set different tolerances per measurement type:

```python
# In get_sizes_for_chart() around line 271-274
tolerance_map = {
    'chest': 2.5,
    'waist': 3.0,
    'hip': 2.0,
    'shoulder_breadth': 1.5,
    'leg_length': 3.0
}

measurements.append({
    'type': mtype,
    'min': min_val,
    'max': max_val,
    'optimal': (min_val + max_val) / 2 if min_val and max_val else None,
    'tolerance': tolerance_map.get(mtype, 2.0),  # ← Use custom tolerance
    'weight': 1.0
})
```

---

## Final Weight Calculation

The algorithm multiplies these together:
```
Final Weight = base_weight (1.0) × importance_weight (0.6-1.0)
```

**Example for T-Shirt**:
- Chest: 1.0 × 1.0 = **1.0** (most important)
- Shoulder: 1.0 × 0.8 = **0.8** (important)
- Waist: 1.0 × 0.6 = **0.6** (less important)

This ensures chest measurements affect the final score more than waist measurements!
