# Garment Size Matching System

## Overview

The Garment Size Matching System is a research module integrated into the Fashion Intelligence Platform that matches user body measurements with brand-specific garment size charts to recommend the most suitable clothing size for online shopping.

---

## 🎯 Features

- **Multi-Brand Support**: Store and compare size charts from multiple clothing brands
- **Smart Matching Algorithm**: Weighted scoring system that considers measurement ranges and tolerances
- **Confidence Scoring**: Provides confidence levels for recommendations
- **Alternative Suggestions**: Suggests alternative sizes when appropriate
- **Brand Comparison**: Compare your size across different brands
- **Detailed Match Analytics**: Shows which measurements fit well and which don't
- **Fit Advice**: Human-readable recommendations and warnings

---

## 📁 System Architecture

### Database Layer (`backend/database/`)

- **`schema.sql`**: SQLite database schema with 8 core tables
- **`db_manager.py`**: Database operations manager
- **`populate_sample_data.py`**: Sample data for 6 brands across multiple categories

#### Database Schema Overview

```
┌─────────────┐      ┌──────────────────┐      ┌──────────┐
│   brands    │──┬───│  size_charts     │──┬───│  sizes   │
└─────────────┘  │   └──────────────────┘  │   └──────────┘
                 │                          │         │
                 │   ┌──────────────────┐  │         │
                 └───│ garment_categories│  │         │
                     └──────────────────┘  │         │
                                           │         │
                                           │   ┌─────────────────┐
                                           └───│size_measurements│
                                               └─────────────────┘
```

**Key Tables:**
- `brands`: Brand information (Nike, Zara, H&M, etc.)
- `garment_categories`: Garment types (T-Shirt, Jeans, Dress, etc.)
- `size_charts`: Links brands to categories with fit types
- `sizes`: Size labels (XS, S, M, L, XL, 32, 34, etc.)
- `size_measurements`: Body measurement ranges for each size
- `category_measurements`: Defines which measurements matter for each garment type
- `user_measurements`: Optional user profile storage
- `recommendation_log`: Analytics and recommendation history

### Service Layer (`backend/services/`)

- **`size_matching_service.py`**: Core matching algorithm and recommendation engine

#### Matching Algorithm

The size matching algorithm uses a weighted scoring approach:

1. **Measurement Scoring** (per measurement):
   - Perfect match (within range): 90-100 points
   - Close match (within tolerance): 70-89 points
   - Outside tolerance: <70 points (decreasing with distance)

2. **Weight Application**:
   - Each measurement has an importance weight (0.0-1.0)
   - Critical measurements (chest for shirts, waist for pants) weighted higher
   - Category-specific weights applied from `category_measurements` table

3. **Final Score Calculation**:
   ```
   final_score = Σ(measurement_score × weight) / Σ(weights)
   ```

4. **Confidence Calculation**:
   - Based on final score and gap to second-best option
   - High confidence: Clear winner with good score
   - Low confidence: Multiple sizes score similarly

### API Layer (`backend/routes/`)

- **`size_routes.py`**: RESTful API endpoints for size recommendations

---

## 🚀 Getting Started

### 1. Initialize Database

```bash
cd backend
python database/populate_sample_data.py
```

This creates `fashion_db.sqlite` and populates it with sample data for:
- 6 brands: Nike, Adidas, Zara, H&M, Levi's, Uniqlo
- 9 garment categories across Men's and Women's
- 6 complete size charts with measurements

### 2. Start Backend Server

```bash
cd backend
python app.py
```

The size recommendation API will be available at `http://localhost:5000/api/size/`

### 3. Test the API

```bash
# Check service health
curl http://localhost:5000/api/size/health

# Get available brands
curl http://localhost:5000/api/size/brands

# Get size recommendation
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

---

## 📡 API Endpoints

### GET `/api/size/brands`
Get all available brands

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
    ],
    "count": 6
  }
}
```

### GET `/api/size/categories?gender=Men`
Get garment categories, optionally filtered by gender

**Response:**
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "category_id": 1,
        "category_name": "T-Shirt",
        "gender": "Men"
      }
    ]
  }
}
```

### POST `/api/size/recommend`
Get size recommendation for specific brand and garment

**Request:**
```json
{
  "measurements": {
    "chest": 95,
    "shoulder_breadth": 45,
    "waist": 82
  },
  "brand_id": 1,
  "category_id": 1,
  "fit_type": "Regular"
}
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
      "alternatives": [
        {
          "size": "L",
          "score": 87.3,
          "fit_note": "Size up - May be looser"
        }
      ],
      "match_details": [
        {
          "measurement": "chest",
          "user_value": 95,
          "size_range": "91-97 cm",
          "optimal": 94,
          "score": 98.5,
          "fit": "perfect"
        }
      ],
      "fit_advice": [
        "✅ Excellent fit! This size matches your measurements very well."
      ]
    }
  }
}
```

### POST `/api/size/recommend/multiple-brands`
Get recommendations across all brands for a garment category

**Request:**
```json
{
  "measurements": {
    "chest": 95,
    "shoulder_breadth": 45,
    "waist": 82
  },
  "category_id": 1,
  "gender": "Men",
  "fit_type": "Regular",
  "min_confidence": 60.0
}
```

### POST `/api/size/compare-brands`
Compare your size across specific brands

**Request:**
```json
{
  "measurements": {
    "waist": 82,
    "hip": 98,
    "leg_length": 81
  },
  "category_id": 5,
  "brand_ids": [5, 1, 2],
  "fit_type": "Regular"
}
```

**Response:**
```json
{
  "comparison": {
    "comparisons": [
      {"brand_name": "Levi's", "recommended_size": "32", "confidence": 95.2},
      {"brand_name": "Nike", "recommended_size": "M", "confidence": 88.1}
    ],
    "summary": "Variable sizing across brands: Levi's: 32, Nike: M"
  }
}
```

### GET `/api/size/size-chart/{brand_id}/{category_id}`
Get detailed size chart with all measurements

**Response:**
```json
{
  "chart": {
    "chart_id": 1,
    "brand_name": "Nike",
    "category_name": "T-Shirt"
  },
  "sizes": [
    {
      "size_label": "M",
      "measurements": [
        {"type": "chest", "min": 91, "max": 97, "optimal": 94}
      ]
    }
  ]
}
```

---

## 🔧 Configuration

### Adding New Brands

```python
from database.db_manager import db_manager

# 1. Add brand
brand_id = db_manager.insert_brand(
    name="New Brand",
    country="USA",
    size_system="US",
    website="https://newbrand.com"
)

# 2. Create size chart
chart_id = db_manager.insert_size_chart(
    brand_id=brand_id,
    category_id=1,  # T-Shirt category
    chart_name="New Brand Men's T-Shirts",
    fit_type="Regular"
)

# 3. Add sizes
size_id = db_manager.insert_size(
    chart_id=chart_id,
    size_label="M",
    size_order=3
)

# 4. Add measurements
db_manager.insert_size_measurement(
    size_id=size_id,
    measurement_type="chest",
    min_val=91,
    max_val=97,
    optimal_val=94,
    tolerance=2.5,
    weight=1.0
)
```

### Customizing Matching Algorithm

Edit `backend/services/size_matching_service.py`:

```python
# Adjust scoring weights
def _score_single_measurement(self, user_value, min_val, max_val, ...):
    # Modify scoring logic here
    ...

# Adjust confidence calculation
def _calculate_confidence(self, best_score, all_scores):
    # Modify confidence logic here
    ...
```

---

## 📊 Sample Data Included

### Brands
1. **Nike** (USA, US sizing) - Men's T-Shirts
2. **Adidas** (Germany, EU sizing) - (Ready for expansion)
3. **Zara** (Spain, EU sizing) - Women's Dresses
4. **H&M** (Sweden, EU sizing) - Women's T-Shirts
5. **Levi's** (USA, US sizing) - Men's Jeans
6. **Uniqlo** (Japan, Asia sizing) - Men's Dress Shirts

### Size Charts
- Nike Men's Athletic T-Shirts (XS-2XL)
- Zara Women's Dresses (XS-XL)
- Levi's Men's 501 Jeans (28-38)
- H&M Women's Basic T-Shirts (XS-XL)
- Uniqlo Men's Formal Shirts (S-2XL)

---

## 📚 Data Collection

For expanding the size chart database, see:
- **[Size Chart Data Collection Guide](./SIZE_CHART_DATA_COLLECTION_GUIDE.md)** - Comprehensive guide
- **`backend/scripts/scrape_size_charts.py`** - Web scraping template

---

## 🧪 Testing

### Unit Tests (To be implemented)

```python
# Test matching algorithm
def test_size_matching():
    measurements = {'chest': 95, 'waist': 82}
    result = size_matching_service.find_best_size(
        measurements, brand_id=1, category_id=1
    )
    assert result['recommended_size'] == 'M'
    assert result['confidence'] > 80
```

### Manual Testing

Test with your own measurements:

```python
from services.size_matching_service import size_matching_service

my_measurements = {
    'chest': 95,
    'waist': 82,
    'hip': 98,
    'shoulder_breadth': 45
}

# Test Nike T-Shirt
result = size_matching_service.find_best_size(
    my_measurements,
    brand_id=1,  # Nike
    category_id=1,  # Men's T-Shirt
    fit_type='Regular'
)

print(f"Recommended size: {result['recommended_size']}")
print(f"Confidence: {result['confidence']}%")
print(f"Advice: {result['fit_advice']}")
```

---

## 🔬 Research Considerations

### Limitations

1. **Data Availability**: Limited to brands with accessible size charts
2. **Measurement Accuracy**: Dependent on body measurement extraction accuracy
3. **Garment Variations**: Same size may fit differently across garment styles
4. **Fabric Properties**: Algorithm doesn't account for stretch/rigid fabrics
5. **Personal Preferences**: Doesn't consider individual fit preferences

### Future Enhancements

- [ ] Machine learning model trained on user feedback
- [ ] Fabric type considerations (stretch, rigid, etc.)
- [ ] Personalization based on previous purchases
- [ ] Integration with e-commerce platforms
- [ ] AR try-on simulation
- [ ] Seasonal variations (winter vs summer fits)
- [ ] Plus-size and specialty sizing
- [ ] International size system conversions

---

## 📖 Academic References

- ASTM D5585: Standard Table of Body Measurements for Adult Male
- ASTM D5586: Standard Table of Body Measurements for Adult Female  
- ISO 8559: Garment construction and anthropometric surveys
- Fashion Industry Size Standards Research

---

## 🤝 Contributing

To add new brands or improve the matching algorithm:

1. **Add Size Chart Data**: Follow the data collection guide
2. **Test Matching**: Verify recommendations with sample measurements
3. **Document Changes**: Update this README
4. **Submit for Review**: Include source verification

---

## 📄 License

This is a research prototype for academic purposes.

---

## 📞 Support

For questions or issues:
- Check the [Data Collection Guide](./SIZE_CHART_DATA_COLLECTION_GUIDE.md)
- Review database schema: `backend/database/schema.sql`
- Examine sample data: `backend/database/populate_sample_data.py`

---

**Version**: 1.0  
**Last Updated**: 2024-03-08  
**Status**: Research Prototype
