# How to Add Size Charts to the System

## Understanding the Error

When you see the message **"Size chart not found for this brand and garment category"**, it means:

1. The brand you selected doesn't exist in the database, OR
2. The garment category doesn't exist, OR
3. There is no size chart mapping between that specific brand and category combination

## Where Size Charts Are Stored

The system uses a SQLite database located at:
```
backend/database/fashion_db.sqlite
```

### Database Structure

The size chart data is organized across multiple related tables:

```
brands                    → Stores brand information (Nike, Zara, etc.)
   ↓
size_charts              → Links brands to categories with fit types
   ↓
sizes                    → Defines size labels (S, M, L, XL, etc.)
   ↓
size_measurements        → Actual measurement ranges for each size
```

## Method 1: Using the Sample Data Script (Recommended for Beginners)

The easiest way to add size charts is to modify the existing sample data script:

### Step 1: Open the populate script
```bash
backend/database/populate_sample_data.py
```

### Step 2: Add your brand to the brands_data list
```python
brands_data = [
    ("Nike", "USA", "US", "https://www.nike.com", "Athletic and sportswear"),
    ("Your Brand Name", "Country", "Size System", "https://yourbrand.com", "Description"),
]
```

### Step 3: Add your garment category (if needed)
```python
categories_data = [
    ("T-Shirt", "Men", "Short sleeve and long sleeve t-shirts"),
    ("Your Category", "Men", "Your description"),
]
```

### Step 4: Add the size chart with measurements

Add a new section like this example:

```python
# =========================================================================
# Your Brand Men's T-Shirts
# =========================================================================
logger.info("📊 Adding Your Brand Men's T-Shirt size chart...")

chart_id = db_manager.insert_size_chart(
    brands["Your Brand Name"],           # Must match the brand name above
    categories["T-Shirt_Men"],           # Format: CategoryName_Gender
    "Your Brand Men's T-Shirts",        # Chart description
    "Regular"                            # Fit type: Regular/Slim/Relaxed
)

# Define sizes with measurements (in centimeters)
your_brand_sizes = [
    # Format: (size_label, order, {measurement_type: (min_value, max_value)})
    ("S", 1, {
        "chest": (86, 91),              # Chest circumference in cm
        "shoulder_breadth": (42, 44),   # Shoulder width in cm
        "waist": (76, 81)               # Waist circumference in cm
    }),
    ("M", 2, {
        "chest": (91, 97),
        "shoulder_breadth": (44, 46),
        "waist": (81, 86)
    }),
    ("L", 3, {
        "chest": (97, 104),
        "shoulder_breadth": (46, 48),
        "waist": (86, 94)
    }),
    ("XL", 4, {
        "chest": (104, 114),
        "shoulder_breadth": (48, 51),
        "waist": (94, 104)
    }),
]

# Insert the sizes and measurements into database
for size_label, order, measurements in your_brand_sizes:
    size_id = db_manager.insert_size(chart_id, size_label, order)
    for meas_type, (min_val, max_val) in measurements.items():
        optimal = (min_val + max_val) / 2  # Calculate middle value
        db_manager.insert_size_measurement(
            size_id, meas_type, min_val, max_val, optimal, 
            tolerance=2.5  # Acceptable deviation in cm
        )
```

### Step 5: Run the script to populate the database
```bash
cd backend
python database/populate_sample_data.py --reset
```

**Warning:** The `--reset` flag will delete all existing data!

## Method 2: Using Python Script to Add Data to Existing Database

If you want to add size charts WITHOUT deleting existing data, create a new script:

### Create: `backend/add_my_size_chart.py`

```python
"""
Script to add custom size charts to existing database
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import db_manager

# Step 1: Add or get the brand
brand_id = db_manager.get_or_create_brand(
    name="Gap",
    country="USA",
    size_system="US",
    website="https://www.gap.com",
    notes="Casual clothing"
)
print(f"Brand ID: {brand_id}")

# Step 2: Add or get the category
category_id = db_manager.get_or_create_category(
    name="T-Shirt",
    gender="Men",
    description="Casual t-shirts"
)
print(f"Category ID: {category_id}")

# Step 3: Define measurement requirements for this category (if not already done)
# This tells the system which measurements are important for matching
requirements = [
    ("chest", 1.0, True, "Primary measurement for upper body fit"),
    ("shoulder_breadth", 0.8, True, "Important for shoulder fit"),
    ("waist", 0.5, False, "For overall fit"),
]

for meas_type, weight, required, desc in requirements:
    try:
        db_manager.insert_category_measurement_mapping(
            category_id, meas_type, weight, required, desc
        )
    except:
        pass  # Already exists

# Step 4: Create the size chart
chart_id = db_manager.insert_size_chart(
    brand_id=brand_id,
    category_id=category_id,
    chart_name="Gap Men's Essential T-Shirts",
    fit_type="Regular"
)
print(f"Size Chart ID: {chart_id}")

# Step 5: Add sizes with measurements
sizes_data = [
    ("S", 1, {"chest": (88, 93), "shoulder_breadth": (43, 45), "waist": (76, 81)}),
    ("M", 2, {"chest": (93, 99), "shoulder_breadth": (45, 47), "waist": (81, 87)}),
    ("L", 3, {"chest": (99, 107), "shoulder_breadth": (47, 50), "waist": (87, 96)}),
    ("XL", 4, {"chest": (107, 117), "shoulder_breadth": (50, 53), "waist": (96, 107)}),
]

for size_label, order, measurements in sizes_data:
    # Insert size
    size_id = db_manager.insert_size(chart_id, size_label, order)
    
    # Insert measurements for this size
    for meas_type, (min_val, max_val) in measurements.items():
        optimal = (min_val + max_val) / 2
        db_manager.insert_size_measurement(
            size_id=size_id,
            measurement_type=meas_type,
            min_value=min_val,
            max_value=max_val,
            optimal_value=optimal,
            tolerance=2.5,
            weight=1.0
        )
    print(f"  Added size: {size_label}")

print("\n✅ Size chart added successfully!")
```

### Run your custom script:
```bash
cd backend
python add_my_size_chart.py
```

## Method 3: Direct Database Access (Advanced)

If you're comfortable with SQL, you can add data directly:

```bash
cd backend/database
sqlite3 fashion_db.sqlite
```

Then run SQL commands:

```sql
-- 1. Add a brand
INSERT INTO brands (brand_name, brand_country, size_system, website_url, notes)
VALUES ('Gap', 'USA', 'US', 'https://www.gap.com', 'Casual wear');

-- 2. Get the brand_id (remember this number)
SELECT brand_id FROM brands WHERE brand_name = 'Gap';

-- 3. Get category_id for the garment type you want
SELECT category_id FROM garment_categories WHERE category_name = 'T-Shirt' AND gender = 'Men';

-- 4. Create a size chart (use the IDs from steps 2 and 3)
INSERT INTO size_charts (brand_id, category_id, chart_name, fit_type, is_active)
VALUES (7, 1, 'Gap Men''s T-Shirts', 'Regular', 1);

-- 5. Get the chart_id
SELECT chart_id FROM size_charts WHERE brand_id = 7 AND category_id = 1;

-- 6. Add sizes (use chart_id from step 5)
INSERT INTO sizes (chart_id, size_label, size_order) VALUES (7, 'S', 1);
INSERT INTO sizes (chart_id, size_label, size_order) VALUES (7, 'M', 2);
INSERT INTO sizes (chart_id, size_label, size_order) VALUES (7, 'L', 3);

-- 7. Add measurements for each size (use size_id)
SELECT size_id FROM sizes WHERE chart_id = 7 AND size_label = 'S';
INSERT INTO size_measurements (size_id, measurement_type, min_value, max_value, optimal_value)
VALUES (1, 'chest', 88, 93, 90.5);
```

## Important Measurement Guidelines

### Common Measurement Types

For different garment categories, use these measurement types:

**Men's T-Shirts / Shirts:**
- `chest` - Chest circumference
- `shoulder_breadth` - Shoulder width
- `waist` - Waist circumference
- `arm_length` - Arm/sleeve length

**Women's Tops / Dresses:**
- `chest` - Bust circumference
- `waist` - Waist circumference
- `hip` - Hip circumference
- `shoulder_breadth` - Shoulder width

**Pants / Jeans:**
- `waist` - Waist circumference
- `hip` - Hip circumference
- `leg_length` - Inseam length
- `thigh` - Thigh circumference

### Measurement Units

- All measurements must be in **centimeters (cm)**
- If you have measurements in inches, convert: `cm = inches × 2.54`

### Size Order

The `size_order` field determines how sizes are sorted:
- 1 = Smallest (XS, 28, 0)
- 2, 3, 4... = Increasing size
- Higher numbers = Larger sizes

## Verifying Your Size Charts

After adding size charts, verify they're working:

### Method 1: Use the setup script
```bash
cd backend
python setup_size_matching.py
```

This will show all brands, categories, and run a test recommendation.

### Method 2: Check the database directly
```bash
cd backend
python check_database.py
```

### Method 3: Test via API
```bash
# Start the backend first
cd backend
python app.py

# Then in another terminal:
curl http://localhost:5000/api/size/brands
curl http://localhost:5000/api/size/categories
curl http://localhost:5000/api/size/size-chart/1/1  # brand_id / category_id
```

## Quick Start: Complete Example

Here's a complete working example to add a new brand with size chart:

```bash
cd backend
```

Create `add_quick_example.py`:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from database.db_manager import db_manager

# Add brand
brand_id = db_manager.get_or_create_brand("Example Brand", "USA", "US")

# Get existing category
category_id = 1  # Assuming T-Shirt Men's exists

# Create size chart
chart_id = db_manager.insert_size_chart(brand_id, category_id, "Example Chart", "Regular")

# Add one size
size_id = db_manager.insert_size(chart_id, "M", 1)
db_manager.insert_size_measurement(size_id, "chest", 90, 95, 92.5, 2.5, 1.0)
db_manager.insert_size_measurement(size_id, "waist", 80, 85, 82.5, 2.5, 0.8)

print("✅ Size chart added! Brand ID:", brand_id)
```

Run it:
```bash
python add_quick_example.py
```

## Need Help?

- See `docs/SIZE_MATCHING_SYSTEM.md` for system documentation
- See `docs/SIZE_CHART_DATA_COLLECTION_GUIDE.md` for collecting size chart data
- Check `backend/database/populate_sample_data.py` for complete examples
- All database methods are in `backend/database/db_manager.py`

## Common Issues

### Issue: "UNIQUE constraint failed"
**Solution:** The brand/category combination already exists. Check the database first or use `get_or_create_` methods instead of `insert_` methods.

### Issue: "No such table: brands"
**Solution:** Database not initialized. Run `python setup_size_matching.py`

### Issue: "Recommendation returns error"
**Solution:** Make sure:
1. Brand exists in database
2. Category exists in database
3. Size chart exists linking that brand + category
4. Sizes exist in that size chart
5. Measurements exist for those sizes
