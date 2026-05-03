# Quick Reference: Database Tables & Relationships

## The 5 Core Tables

```
┏━━━━━━━━━━━━━━━┓
┃   BRANDS      ┃  👔 Stores: Nike, Zara, H&M, Gap
┃ (Who makes it)┃     
┗━━━━━━━┯━━━━━━━┛     
        │              
        └─────────┐    
                  │    
        ┏━━━━━━━━┷━━━━━━━━━━━┓
        ┃  SIZE_CHARTS        ┃  🔗 The Bridge/Link
        ┃  (Brand + Category) ┃     Connects brand to garment type
        ┗━━━━━━━━┯━━━━━━━━━━━┛     
                  │              
        ┌─────────┘              
        │                        
┏━━━━━━━┷━━━━━━━━━━━┓          
┃ GARMENT_CATEGORIES ┃  👕 Stores: T-Shirt, Jeans, Dress
┃  (What is it)      ┃     Gender: Men, Women, Unisex
┗━━━━━━━━━━━━━━━━━━━━┛          


        SIZE_CHARTS
             │
             │ (One chart has many sizes)
             ▼
        ┏━━━━━━━━━━━┓
        ┃   SIZES    ┃  📏 Stores: S, M, L, XL, 32, 34
        ┃ (Size label)┃     Order: 1, 2, 3, 4
        ┗━━━━━┯━━━━━━┛
              │
              │ (One size has many measurements)
              ▼
        ┏━━━━━━━━━━━━━━━━━━┓
        ┃ SIZE_MEASUREMENTS  ┃  📐 Stores actual data:
        ┃ (Actual numbers)   ┃     chest: 91-97 cm
        ┗━━━━━━━━━━━━━━━━━━━┛     waist: 81-86 cm
                                   shoulder: 44-46 cm
```

---

## Real Data Example

### Nike Men's T-Shirt Size M

```
BRANDS table:
┌──────────┬────────────┐
│ brand_id │ brand_name │
├──────────┼────────────┤
│    1     │    Nike    │  ← This is brand #1
└──────────┴────────────┘

GARMENT_CATEGORIES table:
┌─────────────┬───────────────┬────────┐
│ category_id │ category_name │ gender │
├─────────────┼───────────────┼────────┤
│      1      │    T-Shirt    │  Men   │  ← This is category #1
└─────────────┴───────────────┴────────┘

SIZE_CHARTS table (THE LINK):
┌──────────┬──────────┬─────────────┬──────────┐
│ chart_id │ brand_id │ category_id │ fit_type │
├──────────┼──────────┼─────────────┼──────────┤
│    1     │    1     │      1      │ Regular  │  ← Links Nike (#1) + T-Shirt Men (#1)
└──────────┴──────────┴─────────────┴──────────┘

SIZES table:
┌─────────┬──────────┬────────────┐
│ size_id │ chart_id │ size_label │
├─────────┼──────────┼────────────┤
│   102   │    1     │     M      │  ← Size M for Nike chart
└─────────┴──────────┴────────────┘

SIZE_MEASUREMENTS table:
┌─────────┬───────────────────┬───────────┬───────────┐
│ size_id │ measurement_type  │ min_value │ max_value │
├─────────┼───────────────────┼───────────┼───────────┤
│   102   │      chest        │    91     │    97     │  ← Chest: 91-97 cm
│   102   │ shoulder_breadth  │    44     │    46     │  ← Shoulder: 44-46 cm
│   102   │      waist        │    81     │    86     │  ← Waist: 81-86 cm
└─────────┴───────────────────┴───────────┴───────────┘
```

---

## The Flow: From Brand to Measurements

```
"Nike" 
   ↓ (stored in BRANDS table)
brand_id = 1
   ↓
   ↓ (linked in SIZE_CHARTS)
   +-----→ "T-Shirt Men"
              ↓ (stored in GARMENT_CATEGORIES)
           category_id = 1
              ↓
              ↓ (linked in SIZE_CHARTS)
           chart_id = 1
              ↓
              ↓ (sizes defined in SIZES table)
           Sizes: S, M, L, XL
              ↓
              ↓ (measurements in SIZE_MEASUREMENTS)
           Size M:
             - chest: 91-97 cm
             - shoulder: 44-46 cm
             - waist: 81-86 cm
```

---

## Table Purposes (One Sentence Each)

1. **BRANDS** - Stores brand names (Nike, Zara, H&M)
2. **GARMENT_CATEGORIES** - Stores garment types (T-Shirt, Jeans, Dress) by gender
3. **SIZE_CHARTS** - Links brand + category together (creates the size chart)
4. **SIZES** - Stores size labels (S, M, L, XL) for each chart
5. **SIZE_MEASUREMENTS** - Stores actual measurement ranges (91-97 cm) for each size

---

## Why 5 Tables Instead of 1 Big Table?

### ❌ Bad: One Giant Table
```
| Brand | Category | Gender | Size | Measurement | Min | Max |
|-------|----------|--------|------|-------------|-----|-----|
| Nike  | T-Shirt  | Men    | M    | chest       | 91  | 97  |
| Nike  | T-Shirt  | Men    | M    | shoulder    | 44  | 46  |
| Nike  | T-Shirt  | Men    | M    | waist       | 81  | 86  |
| Nike  | T-Shirt  | Men    | L    | chest       | 97  | 104 |
```
**Problems:**
- "Nike" repeated 1000+ times (wasted space)
- Want to change Nike's name? Update 1000+ rows!
- Hard to manage and slow to query

### ✅ Good: 5 Connected Tables
```
BRANDS:
| ID | Name |
|----|------|
| 1  | Nike |  ← Store "Nike" ONCE

SIZE_MEASUREMENTS:
| ID | brand_id | size_id | type  | min | max |
|----|----------|---------|-------|-----|-----|
| 1  |    1     |   102   | chest | 91  | 97  |  ← Reference Nike by ID
```
**Benefits:**
- "Nike" stored once
- Change Nike's name? Update 1 row
- Fast queries, no duplicate data

---

## How to Add Your Own Brand

### Simple 5-Step Process:

```python
# Step 1: Add Brand
brand_id = db_manager.get_or_create_brand("Your Brand", "Country", "US")

# Step 2: Add/Get Category
category_id = db_manager.get_or_create_category("T-Shirt", "Men", "Description")

# Step 3: Create Size Chart (the link!)
chart_id = db_manager.insert_size_chart(brand_id, category_id, "Chart Name", "Regular")

# Step 4: Add Sizes
size_m_id = db_manager.insert_size(chart_id, "M", 2)
size_l_id = db_manager.insert_size(chart_id, "L", 3)

# Step 5: Add Measurements
db_manager.insert_size_measurement(size_m_id, "chest", 91, 97, 94)
db_manager.insert_size_measurement(size_m_id, "waist", 81, 86, 83.5)
```

**That's it!** Your brand is now in the system.

---

## Key Concepts

### Primary Key (PK)
- Unique ID for each row
- Example: brand_id, size_id, chart_id
- Like a person's social security number - unique identifier

### Foreign Key (FK)
- Reference to another table's Primary Key
- Example: size_charts.brand_id → brands.brand_id
- Like saying "this chart belongs to brand #1 (Nike)"

### Relationship Types
- **One-to-Many**: One brand → Many size charts
- **Many-to-Many**: Many brands ↔ Many categories (via size_charts bridge)

---

## Visual: Complete Structure

```
┌─────────────┐
│   BRANDS    │ 1
│  (Nike)     │───┐
└─────────────┘   │
                  │ Many size charts
                  │
                  ▼
              ┌───────────────┐
              │  SIZE_CHARTS  │
              │  (Nike+Shirt) │ 1
              └───────────────┘───┐
                  ▲               │
                  │               │ Many sizes
┌─────────────────┴─┐             │
│ GARMENT_CATEGORIES│             ▼
│    (T-Shirt)      │         ┌───────┐
└───────────────────┘         │ SIZES │ 1
                              │  (M)  │───┐
                              └───────┘   │
                                          │ Many measurements
                                          ▼
                                   ┌──────────────────┐
                                   │SIZE_MEASUREMENTS │
                                   │  (chest: 91-97)  │
                                   └──────────────────┘
```

Numbers show relationship: 1 = One, Many = Multiple

---

## Files to Check

1. **Schema (Table Definitions)**
   - `backend/database/schema.sql`
   - Shows CREATE TABLE statements

2. **Data Access Functions**
   - `backend/database/db_manager.py`
   - Python functions to insert/query data

3. **Sample Data**
   - `backend/database/populate_sample_data.py`
   - Examples of adding Nike, Zara, H&M

4. **How to Add Charts**
   - `backend/add_size_chart.py`
   - Ready-to-use template

---

## Quick Mental Model

Think of it like organizing a library:

```
BRANDS = Publishers (who made the book)
CATEGORIES = Book Types (fiction, non-fiction, textbook)
SIZE_CHARTS = Specific Books (Nike's T-Shirt book)
SIZES = Chapters (S, M, L, XL)
SIZE_MEASUREMENTS = Pages (actual content/data)
```

You don't write the publisher's name on every page of every book.
You write it once (in BRANDS), then reference it (using brand_id).

Same logic here! 📚

---

## Summary

✅ **Your approach is correct!**
✅ **The system already uses this design!**
✅ **It's professional, scalable, and maintainable!**

This is how real e-commerce platforms (Amazon, Zalando, ASOS) manage their size charts.

---

**Next Steps:**
1. Read `DATABASE_DESIGN_EXPLAINED.md` for detailed walkthrough
2. Read `HOW_TO_ADD_SIZE_CHARTS.md` for practical examples
3. Try `python add_size_chart.py` to add your first brand

You understand the concept correctly! 🎯
