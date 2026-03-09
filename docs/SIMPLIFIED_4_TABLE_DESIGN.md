# Simplified 4-Table Database Design

## The 4 Tables (Simple & Clear)

```
┌─────────────┐
│  BRANDS     │  Table 1: Who makes the clothes? (Nike, Zara, H&M)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ SIZE_CHARTS     │  Table 2: Link Brand + Garment Type (Nike Men's T-Shirts)
└──────┬──────────┘
       ▲
       │
┌──────┴──────────────┐
│ GARMENT_CATEGORIES  │  Table 3: What type of clothing? (T-Shirt, Jeans, Dress)
└─────────────────────┘

       │
       ▼
┌─────────────────────────────────────────────┐
│  SIZES                                      │  Table 4: All size data in one place
│  - Size labels (S, M, L, XL)                │  (Size labels + measurements together)
│  - Measurements (chest, waist, shoulder)    │
└─────────────────────────────────────────────┘
```

---

## Table 1: BRANDS
**Purpose:** Store brand information

| Column       | Example              |
|--------------|----------------------|
| brand_id     | 1                    |
| brand_name   | Nike                 |
| country      | USA                  |
| size_system  | US                   |

**Sample Data:**
```
ID  | Brand Name | Country | System
----|------------|---------|-------
1   | Nike       | USA     | US
2   | Zara       | Spain   | EU
3   | H&M        | Sweden  | EU
```

---

## Table 2: GARMENT_CATEGORIES
**Purpose:** Define types of clothing

| Column        | Example    |
|---------------|------------|
| category_id   | 1          |
| category_name | T-Shirt    |
| gender        | Men        |

**Sample Data:**
```
ID  | Category  | Gender
----|-----------|-------
1   | T-Shirt   | Men
2   | T-Shirt   | Women
3   | Jeans     | Men
4   | Dress     | Women
```

---

## Table 3: SIZE_CHARTS
**Purpose:** Connect a brand with a garment type

| Column      | Example                        |
|-------------|--------------------------------|
| chart_id    | 1                              |
| brand_id    | 1 (Nike)                       |
| category_id | 1 (T-Shirt Men)                |
| fit_type    | Regular                        |

**Sample Data:**
```
Chart ID | Brand ID | Category ID | Fit Type
---------|----------|-------------|----------
1        | 1 (Nike) | 1 (T-Shirt) | Regular
2        | 2 (Zara) | 4 (Dress)   | Regular
3        | 1 (Nike) | 1 (T-Shirt) | Slim
```

**This is the bridge!** It links Nike (brand #1) with Men's T-Shirts (category #1)

---

## Table 4: SIZES
**Purpose:** Store size labels AND all measurements in one place

| Column           | Example          |
|------------------|------------------|
| size_id          | 102              |
| chart_id         | 1                |
| size_label       | M                |
| size_order       | 2                |
| chest_min        | 91.0 cm          |
| chest_max        | 97.0 cm          |
| shoulder_min     | 44.0 cm          |
| shoulder_max     | 46.0 cm          |
| waist_min        | 81.0 cm          |
| waist_max        | 86.0 cm          |
| hip_min          | NULL             |
| hip_max          | NULL             |
| arm_length_min   | NULL             |
| arm_length_max   | NULL             |

**Sample Data (Nike Men's T-Shirt sizes):**
```
Size ID | Chart | Label | Order | Chest    | Shoulder | Waist    
--------|-------|-------|-------|----------|----------|----------
101     | 1     | S     | 1     | 86-91 cm | 42-44 cm | 76-81 cm
102     | 1     | M     | 2     | 91-97 cm | 44-46 cm | 81-86 cm
103     | 1     | L     | 3     | 97-104cm | 46-48 cm | 86-94 cm
104     | 1     | XL    | 4     | 104-114cm| 48-51 cm | 94-104cm
```

**Note:** Different garment types use different measurement columns:
- T-Shirts use: chest, shoulder, waist
- Jeans use: waist, hip, leg_length
- Dresses use: chest (bust), waist, hip
- Unused columns are left NULL (empty)

---

## How They Connect: Complete Example

### Nike Men's T-Shirt Size M

```
Step 1: BRANDS table
┌────┬──────┐
│ ID │ Name │
├────┼──────┤
│ 1  │ Nike │ ← Brand ID = 1
└────┴──────┘

Step 2: GARMENT_CATEGORIES table
┌────┬──────────┬────────┐
│ ID │ Category │ Gender │
├────┼──────────┼────────┤
│ 1  │ T-Shirt  │ Men    │ ← Category ID = 1
└────┴──────────┴────────┘

Step 3: SIZE_CHARTS table (THE LINK)
┌──────────┬──────────┬─────────────┬──────────┐
│ Chart ID │ Brand ID │ Category ID │ Fit Type │
├──────────┼──────────┼─────────────┼──────────┤
│    1     │    1     │      1      │ Regular  │ ← Links Nike + T-Shirt Men
└──────────┴──────────┴─────────────┴──────────┘

Step 4: SIZES table (ALL DATA IN ONE PLACE)
┌─────────┬──────────┬───────┬───────┬───────────┬──────────┬───────────┐
│ Size ID │ Chart ID │ Label │ Order │   Chest   │ Shoulder │   Waist   │
├─────────┼──────────┼───────┼───────┼───────────┼──────────┼───────────┤
│   102   │    1     │   M   │   2   │ 91-97 cm  │ 44-46 cm │ 81-86 cm  │
└─────────┴──────────┴───────┴───────┴───────────┴──────────┴───────────┘
```

Done! All the data you need in 4 tables.

---

## Simple Schema (SQL)

```sql
-- Table 1: Brands
CREATE TABLE brands (
    brand_id INTEGER PRIMARY KEY,
    brand_name TEXT NOT NULL,
    country TEXT,
    size_system TEXT
);

-- Table 2: Garment Categories
CREATE TABLE garment_categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    gender TEXT NOT NULL
);

-- Table 3: Size Charts (Bridge/Link)
CREATE TABLE size_charts (
    chart_id INTEGER PRIMARY KEY,
    brand_id INTEGER,
    category_id INTEGER,
    fit_type TEXT,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES garment_categories(category_id)
);

-- Table 4: Sizes (with all measurements)
CREATE TABLE sizes (
    size_id INTEGER PRIMARY KEY,
    chart_id INTEGER,
    size_label TEXT NOT NULL,
    size_order INTEGER,
    
    -- Body measurements (all in one table)
    chest_min REAL,
    chest_max REAL,
    shoulder_min REAL,
    shoulder_max REAL,
    waist_min REAL,
    waist_max REAL,
    hip_min REAL,
    hip_max REAL,
    arm_length_min REAL,
    arm_length_max REAL,
    leg_length_min REAL,
    leg_length_max REAL,
    
    FOREIGN KEY (chart_id) REFERENCES size_charts(chart_id)
);
```

---

## How to Add Data (Simple Python)

```python
from database.db_manager import db_manager

# 1. Add Brand
db_manager.execute(
    "INSERT INTO brands (brand_name, country, size_system) VALUES (?, ?, ?)",
    ["Gap", "USA", "US"]
)
brand_id = 7  # Get the ID

# 2. Get Category (already exists)
category_id = 1  # T-Shirt Men

# 3. Create Size Chart (the link)
db_manager.execute(
    "INSERT INTO size_charts (brand_id, category_id, fit_type) VALUES (?, ?, ?)",
    [brand_id, category_id, "Regular"]
)
chart_id = 15  # Get the ID

# 4. Add Size with ALL measurements
db_manager.execute("""
    INSERT INTO sizes (
        chart_id, size_label, size_order,
        chest_min, chest_max,
        shoulder_min, shoulder_max,
        waist_min, waist_max
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    chart_id,    # 15
    "M",         # Size label
    2,           # Size order
    91, 97,      # Chest: 91-97 cm
    44, 46,      # Shoulder: 44-46 cm
    81, 86       # Waist: 81-86 cm
])
```

**Done!** Size M added with all measurements in one INSERT statement.

---

## Comparison: 5 Tables vs 4 Tables

### Old Way (5 tables):
```
BRANDS
SIZE_CHARTS
GARMENT_CATEGORIES
SIZES ← size labels only
SIZE_MEASUREMENTS ← measurements in separate table
```

### New Way (4 tables):
```
BRANDS
SIZE_CHARTS
GARMENT_CATEGORIES
SIZES ← size labels AND measurements together
```

**What changed?**
- Merged SIZES and SIZE_MEASUREMENTS into one table
- Instead of storing measurements in separate rows, use columns
- Simpler! Less tables to manage!

---

## Which Measurements for Which Garments?

### T-Shirts / Shirts (Men & Women)
Use these columns:
- `chest_min`, `chest_max`
- `shoulder_min`, `shoulder_max`
- `waist_min`, `waist_max`
- `arm_length_min`, `arm_length_max`

Leave empty: hip, leg_length

### Jeans / Pants (Men & Women)
Use these columns:
- `waist_min`, `waist_max`
- `hip_min`, `hip_max`
- `leg_length_min`, `leg_length_max`

Leave empty: chest, shoulder, arm_length

### Dresses (Women)
Use these columns:
- `chest_min`, `chest_max` (bust)
- `waist_min`, `waist_max`
- `hip_min`, `hip_max`

Leave empty: shoulder, arm_length, leg_length

---

## Complete Example: Add Gap Men's T-Shirt

```python
# Step 1: Add brand (if not exists)
INSERT INTO brands (brand_name, country, size_system) 
VALUES ('Gap', 'USA', 'US');
-- Returns brand_id = 7

# Step 2: Category already exists (T-Shirt Men = 1)

# Step 3: Create size chart
INSERT INTO size_charts (brand_id, category_id, fit_type)
VALUES (7, 1, 'Regular');
-- Returns chart_id = 15

# Step 4: Add all sizes at once
INSERT INTO sizes (chart_id, size_label, size_order, chest_min, chest_max, shoulder_min, shoulder_max, waist_min, waist_max)
VALUES 
    (15, 'S', 1, 86, 91, 42, 44, 76, 81),
    (15, 'M', 2, 91, 97, 44, 46, 81, 86),
    (15, 'L', 3, 97, 104, 46, 48, 86, 94),
    (15, 'XL', 4, 104, 114, 48, 51, 94, 104);

-- Done! 4 sizes added in one command
```

---

## Benefits of 4 Tables vs 5 Tables

✅ **Simpler**: Only 4 tables to understand
✅ **Faster queries**: No need to join 5 tables, only 4
✅ **Easier to add data**: One INSERT instead of multiple
✅ **Less overwhelming**: Fewer moving parts

❌ **Trade-off**: Sizes table has many columns (but most are NULL/empty for each garment type)

---

## Visual Summary

```
┌─────────────┐
│   BRANDS    │  Store brands once
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   SIZE_CHARTS       │  Link brand + category
│   (Bridge Table)    │
└──────┬──────────────┘
       ▲
       │
┌──────┴─────────────────┐
│  GARMENT_CATEGORIES    │  Store garment types
└────────────────────────┘
       │
       ▼
┌───────────────────────────────────────┐
│           SIZES                       │
│  ┌────────────┬──────────────────┐   │
│  │ size_label │  Measurements    │   │
│  ├────────────┼──────────────────┤   │
│  │ S          │ 86-91, 42-44, 76-81 │
│  │ M          │ 91-97, 44-46, 81-86 │
│  │ L          │ 97-104, 46-48, 86-94│
│  └────────────┴──────────────────┘   │
└───────────────────────────────────────┘
  Everything in one place!
```

---

## Summary

**4 Simple Tables:**
1. **BRANDS** - Who makes it? (Nike, Zara)
2. **GARMENT_CATEGORIES** - What is it? (T-Shirt, Jeans)
3. **SIZE_CHARTS** - Bridge/Link (Nike + T-Shirt)
4. **SIZES** - All size data (labels + measurements together)

**Key Change from 5 tables:**
- Merged size labels and measurements into one table
- Use columns for measurements instead of separate rows
- Simpler to understand and manage!

---

**Files:**
- See `simplified_schema.sql` for the 4-table database structure
- See `add_size_chart_simple.py` for easy data insertion examples

This is much cleaner! 🎯
