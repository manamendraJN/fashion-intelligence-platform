# Size Matching System - Setup and Usage Guide

## 🚀 Quick Start Guide

Follow these steps to set up and use the garment size matching system.

---

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Backend dependencies installed (see main README)
- Frontend dependencies installed (see main README)

---

## 🔧 Setup Instructions

### Step 1: Initialize the Database

```bash
# Navigate to backend directory
cd backend

# Run the database population script
python database/populate_sample_data.py
```

**Expected Output:**
```
🚀 Starting sample data population...
📦 Adding brands...
  ✓ Nike
  ✓ Adidas
  ✓ Zara
  ✓ H&M
  ✓ Levi's
  ✓ Uniqlo
👕 Adding garment categories...
  ✓ T-Shirt (Men)
  ✓ T-Shirt (Women)
  ...
✅ Sample data population completed!
```

This creates `backend/database/fashion_db.sqlite` with:
- 6 brands
- 9 garment categories
- 6 complete size charts
- Sample measurements and mappings

### Step 2: Verify Database Creation

Check that the database file exists:

```bash
# Windows
dir backend\database\fashion_db.sqlite

# Linux/Mac
ls -la backend/database/fashion_db.sqlite
```

### Step 3: Start the Backend Server

```bash
cd backend
python app.py
```

**Expected Output:**
```
============================================================
🚀 Starting Body Measurement AI API v1.0
📍 Host: localhost:5000
🔧 Debug: True
============================================================
✅ Size recommendation routes initialized
 * Running on http://localhost:5000
```

### Step 4: Test the Size API

Open a new terminal and test the API:

```bash
# Test 1: Check service health
curl http://localhost:5000/api/size/health

# Test 2: Get brands
curl http://localhost:5000/api/size/brands

# Test 3: Get size recommendation
curl -X POST http://localhost:5000/api/size/recommend \
  -H "Content-Type: application/json" \
  -d "{\"measurements\": {\"chest\": 95, \"shoulder_breadth\": 45, \"waist\": 82}, \"brand_id\": 1, \"category_id\": 1}"
```

### Step 5: Start the Frontend (Optional)

```bash
cd frontend
npm run dev
```

Then navigate to `http://localhost:5173` (or the port shown) in your browser.

---

## 📊 Using the System

### Method 1: Via Frontend UI

1. **Navigate to Size Matching Page**
   - Add route to `App.jsx` if not already added:
   ```jsx
   import SizeMatching from './pages/SizeMatching';
   // Add route: <Route path="/size-matching" element={<SizeMatching />} />
   ```

2. **Get Body Measurements**
   - Option A: Upload front/side images to extract measurements
   - Option B: Use sample measurements for testing

3. **Select Garment**
   - Choose a brand (Nike, Zara, H&M, etc.)
   - Choose a garment category (T-Shirt, Jeans, Dress, etc.)

4. **View Recommendations**
   - See recommended size with confidence score
   - Review detailed measurement fit analysis
   - Check alternative sizes
   - Compare across multiple brands

### Method 2: Via API Directly

#### Get Brands List

```bash
curl http://localhost:5000/api/size/brands
```

**Response:**
```json
{
  "success": true,
  "data": {
    "brands": [
      {
        "brand_id": 1,
        "brand_name": "Nike",
        "brand_country": "USA",
        "size_system": "US"
      }
    ]
  }
}
```

#### Get Categories

```bash
curl http://localhost:5000/api/size/categories
```

#### Get Size Recommendation

```bash
curl -X POST http://localhost:5000/api/size/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "measurements": {
      "chest": 95,
      "shoulder_breadth": 45,
      "waist": 82
    },
    "brand_id": 1,
    "category_id": 1,
    "fit_type": "Regular"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recommendation": {
      "brand_name": "Nike",
      "category_name": "T-Shirt",
      "recommended_size": "M",
      "confidence": 92.5,
      "match_score": 94.2,
      "alternatives": [...],
      "match_details": [...],
      "fit_advice": [
        "✅ Excellent fit! This size matches your measurements very well."
      ]
    }
  }
}
```

#### Compare Across Multiple Brands

```bash
curl -X POST http://localhost:5000/api/size/recommend/multiple-brands \
  -H "Content-Type: application/json" \
  -d '{
    "measurements": {
      "chest": 95,
      "shoulder_breadth": 45,
      "waist": 82
    },
    "category_id": 1,
    "fit_type": "Regular",
    "min_confidence": 60.0
  }'
```

### Method 3: Via Python Script

Create a test script `test_size_matching.py`:

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:5000/api/size"

# Your body measurements
my_measurements = {
    "chest": 95,
    "waist": 82,
    "hip": 98,
    "shoulder_breadth": 45,
    "arm_length": 60
}

# Get recommendation for Nike T-Shirt
response = requests.post(
    f"{BASE_URL}/recommend",
    json={
        "measurements": my_measurements,
        "brand_id": 1,  # Nike
        "category_id": 1,  # Men's T-Shirt
        "fit_type": "Regular"
    }
)

result = response.json()

if result['success']:
    rec = result['data']['recommendation']
    print(f"\n{'='*60}")
    print(f"Brand: {rec['brand_name']}")
    print(f"Garment: {rec['category_name']}")
    print(f"Recommended Size: {rec['recommended_size']}")
    print(f"Confidence: {rec['confidence']}%")
    print(f"{'='*60}\n")
    
    print("Fit Advice:")
    for advice in rec['fit_advice']:
        print(f"  {advice}")
    
    print("\nMeasurement Details:")
    for detail in rec['match_details']:
        print(f"  {detail['measurement']}: {detail['user_value']} cm "
              f"(size: {detail['size_range']}) - {detail['fit']}")
else:
    print(f"Error: {result.get('error')}")
```

Run it:
```bash
python test_size_matching.py
```

---

## 🔍 Understanding the Results

### Confidence Scores

- **90-100%**: Excellent match - highly confident recommendation
- **75-89%**: Good match - reliable recommendation
- **60-74%**: Acceptable match - consider trying alternatives
- **<60%**: Limited match - try other brands or check measurements

### Match Scores

Individual measurement scores indicate how well each measurement fits:
- **90-100**: Perfect fit within size range
- **70-89**: Close fit, within tolerance
- **<70**: Outside typical range for this size

### Fit Indicators

- **perfect**: Your measurement is within the ideal range
- **slightly_small**: You're at the lower end of the range
- **slightly_large**: You're at the upper end of the range
- **too_small**: Consider sizing up
- **too_large**: Consider sizing down

---

## 🛠️ Customization

### Adding Your Own Brand Data

1. **Collect Size Chart Data**
   - Follow the [Data Collection Guide](./SIZE_CHART_DATA_COLLECTION_GUIDE.md)

2. **Add to Database**

```python
from database.db_manager import db_manager

# Add brand
brand_id = db_manager.insert_brand(
    name="Your Brand",
    country="USA",
    size_system="US",
    website="https://yourbrand.com"
)

# Add size chart
chart_id = db_manager.insert_size_chart(
    brand_id=brand_id,
    category_id=1,  # Use existing category or create new
    chart_name="Your Brand Men's Shirts",
    fit_type="Regular"
)

# Add sizes and measurements
# See populate_sample_data.py for examples
```

3. **Restart Backend Server**

### Modifying Matching Algorithm

Edit `backend/services/size_matching_service.py`:

```python
class SizeMatchingService:
    
    def _score_single_measurement(self, user_value, min_val, max_val, ...):
        # Customize scoring logic here
        # Default: 100 points for perfect match, scaling down
        pass
    
    def _calculate_confidence(self, best_score, all_scores):
        # Customize confidence calculation
        # Consider score gaps, measurement coverage, etc.
        pass
```

---

## 🐛 Troubleshooting

### Issue: "Database file not found"

**Solution:**
```bash
cd backend
python database/populate_sample_data.py
```

### Issue: "No size charts available"

**Cause:** Database is empty or brand/category doesn't have a size chart

**Solution:**
1. Check database exists: `backend/database/fashion_db.sqlite`
2. Repopulate: `python database/populate_sample_data.py`
3. Verify brand_id and category_id are valid

### Issue: "Model not loaded" error

**Solution:** This is expected if you haven't trained the body measurement extraction model yet. The size matching system can work independently by providing measurements manually.

### Issue: "CORS error" in frontend

**Solution:** Ensure backend is running on `http://localhost:5000` and CORS is enabled in `app.py` (should be by default).

### Issue: "Connection refused"

**Solution:**
1. Check backend is running: `python backend/app.py`
2. Verify port 5000 is not in use
3. Check firewall settings

---

## 📊 Testing with Different Profiles

Test the system with various body types:

### Athletic Build
```json
{
  "chest": 102,
  "shoulder_breadth": 48,
  "waist": 85,
  "bicep": 35
}
```

### Average Build
```json
{
  "chest": 95,
  "shoulder_breadth": 45,
  "waist": 82,
  "hip": 98
}
```

### Slim Build
```json
{
  "chest": 88,
  "shoulder_breadth": 42,
  "waist": 74,
  "hip": 90
}
```

---

## 📈 Next Steps

1. **Expand Database**
   - Add more brands using the data collection guide
   - Add more garment categories (jackets, suits, etc.)
   - Include different fit types (slim, relaxed, athletic)

2. **Improve Algorithm**
   - Collect user feedback on recommendations
   - Implement machine learning model
   - Add fabric type considerations

3. **Integration**
   - Combine with body measurement extraction
   - Add user profile management
   - Implement recommendation history

4. **Research Analysis**
   - Analyze sizing consistency across brands
   - Study measurement importance per garment type
   - Evaluate confidence score accuracy

---

## 📚 Additional Resources

- **[Complete System Documentation](./SIZE_MATCHING_SYSTEM.md)**
- **[Data Collection Guide](./SIZE_CHART_DATA_COLLECTION_GUIDE.md)**
- **[Database Schema](../backend/database/schema.sql)**
- **[Sample Data Script](../backend/database/populate_sample_data.py)**
- **[API Routes](../backend/routes/size_routes.py)**
- **[Matching Algorithm](../backend/services/size_matching_service.py)**

---

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the system logs in the terminal
3. Verify all prerequisites are installed
4. Ensure database is properly initialized

---

**Version**: 1.0  
**Last Updated**: 2024-03-08  
**Status**: Research Prototype

---

## Quick Reference Commands

```bash
# Initialize database
python backend/database/populate_sample_data.py

# Start backend
python backend/app.py

# Start frontend
cd frontend && npm run dev

# Test API
curl http://localhost:5000/api/size/health

# Get recommendation
curl -X POST http://localhost:5000/api/size/recommend \
  -H "Content-Type: application/json" \
  -d '{"measurements": {"chest": 95, "waist": 82}, "brand_id": 1, "category_id": 1}'
```
