# Size Matching Algorithm - Glossary & Key Terms

Quick reference guide for technical terminology used in the algorithm and presentation.

---

## Core Algorithm Terms

### **Size Chart**
A table containing measurement ranges for each size offered by a brand for a specific garment category.

**Example:**
```
Nike Men's T-Shirt (Regular Fit)
Size S:  Chest 88-94cm, Waist 76-82cm
Size M:  Chest 94-100cm, Waist 82-88cm
Size L:  Chest 100-106cm, Waist 88-94cm
```

---

### **Measurement Range**
The minimum and maximum body measurement values that a particular size is designed to fit.

**Components:**
- **Minimum (min):** Lower boundary of acceptable fit
- **Maximum (max):** Upper boundary of acceptable fit
- **Range Width:** max - min (the "room" within a size)

**Example:**
```
Size M Chest: 94-100 cm
min = 94, max = 100, width = 6 cm
```

---

### **Optimal Value**
The ideal body measurement within a size range that represents the best possible fit.

**Properties:**
- Usually the midpoint of the range
- Sometimes brand-specified
- Can be null/optional
- Used to calculate distance for fine-tuning scores

**Example:**
```
Range: 94-100 cm
Optimal: 97 cm (midpoint)

Person with 97cm chest = perfect fit
Person with 95cm or 99cm = still good, but not quite as ideal
```

**In Code:**
```python
optimal = (min_val + max_val) / 2
```

---

### **Tolerance**
Additional leeway beyond the size range where the garment might still fit acceptably.

**Purpose:**
- Accounts for fabric stretch
- Allows for measurement imprecision
- Provides "gray zone" scoring

**Example:**
```
Size M Chest: 94-100 cm, Tolerance: 3 cm
Acceptable fit range: 91-103 cm
- 91-94 cm: Slightly tight but wearable
- 94-100 cm: Perfect fit
- 100-103 cm: Slightly loose but wearable
- <91 or >103: Won't fit well
```

**Default Values:**
- Typical: 2-4 cm
- Depends on garment type and fabric

---

### **Weight (Importance Weight)**
A numerical multiplier indicating how much a particular measurement matters for the final recommendation.

**Purpose:**
- Prioritizes critical measurements
- Different weights for different garment types

**Examples:**

**T-Shirt weights:**
```
Chest:    1.5  (Most important - determines if wearable)
Shoulder: 1.2  (Important for comfort)
Waist:    0.8  (Less critical)
Sleeve:   0.5  (Most forgiving)
```

**Pants weights:**
```
Waist:    1.8  (Most critical)
Hips:     1.5  (Very important)
Inseam:   1.0  (Important)
Thigh:    0.7  (Less critical)
```

**Principle:** If measurement X is off, will the garment still be wearable?
- Yes → Lower weight
- No → Higher weight

---

### **Match Score**
A numerical value (0-100) indicating how well a user's measurement fits a particular size's range.

**Score Ranges:**
- **90-100:** Perfect fit (within range)
- **70-89:** Acceptable fit (within tolerance)
- **0-69:** Poor fit (beyond tolerance)

**Calculation depends on position:**
1. Within range → High score (90-100)
2. Outside range, within tolerance → Medium score (70-89)
3. Beyond tolerance → Low score (0-69)

---

### **Final Score (Aggregate Score)**
The weighted average of all individual measurement scores for a complete size evaluation.

**Formula:**
$$\text{Final Score} = \frac{\sum_{i=1}^{n} (\text{score}_i \times \text{weight}_i)}{\sum_{i=1}^{n} \text{weight}_i}$$

**Example:**
```
Measurements for Size M:
- Chest:    score=98, weight=1.5 → contribution=147
- Waist:    score=100, weight=0.8 → contribution=80
- Shoulder: score=96, weight=1.2 → contribution=115.2

Final = (147 + 80 + 115.2) / (1.5 + 0.8 + 1.2) = 97.7
```

---

### **Confidence Score**
A percentage (0-100%) indicating how certain the algorithm is about its recommendation.

**Factors:**
1. **Match Quality:** How good is the best match?
2. **Separation Gap:** How much better is it than alternatives?

**Interpretation:**
- **90-100%:** Very confident - clear best choice
- **70-89%:** Confident - good match with some separation
- **60-69%:** Moderate - may want to try alternatives
- **<60%:** Low confidence - consider other brands

**Example:**
```
Size M: 95 (best)
Size L: 78 (second)
Gap: 17 points (large)
→ Confidence: ~100% (very sure M is right)

vs.

Size M: 85 (best)
Size L: 83 (second)
Gap: 2 points (small)
→ Confidence: ~77% (might want to try both)
```

---

## Scoring Components

### **Deviation**
The distance between user measurement and the nearest range boundary.

**Formula:**
```python
if user_value < min_val:
    deviation = min_val - user_value  # Below range
else:
    deviation = user_value - max_val  # Above range
```

**Example:**
```
Size M: 94-100 cm
User: 102 cm
deviation = 102 - 100 = 2 cm (above range)
```

---

### **Excess Deviation**
The amount by which deviation exceeds tolerance.

**Formula:**
```python
excess_deviation = deviation - tolerance
```

**Example:**
```
Size M: 94-100 cm, tolerance: 3 cm
User: 108 cm
deviation = 108 - 100 = 8 cm
excess_deviation = 8 - 3 = 5 cm (5cm beyond acceptable)
```

---

### **Penalty**
Score reduction applied when user measurement is beyond tolerance.

**Formula:**
```python
penalty = excess_deviation × 10  # 10 points per cm
penalty = min(70, penalty)        # Cap at 70
score = max(0, 70 - penalty)      # Final score
```

**Rationale:** Each cm beyond tolerance makes fit increasingly poor.

**Example:**
```
excess = 5 cm
penalty = 5 × 10 = 50 points
score = 70 - 50 = 20 (poor fit)
```

---

### **Range Width**
The span of measurements that a size accommodates.

**Formula:**
```python
range_width = max_val - min_val
```

**Example:**
```
Size M: 94-100 cm
range_width = 100 - 94 = 6 cm
```

**Uses:**
- Calculating distance from optimal as percentage
- Normalizing scores across different measurement types

---

## Fit Assessment Terms

### **Fit Categories**

**perfect**
- User measurement within min-max range
- Score: 90-100
- Meaning: Size will fit comfortably

**slightly_small**
- User measurement below min, within tolerance
- Score: 70-89
- Meaning: Might be slightly tight but wearable

**slightly_large**
- User measurement above max, within tolerance
- Score: 70-89
- Meaning: Might be slightly loose but wearable

**too_small**
- User measurement below min-tolerance
- Score: <70
- Meaning: Will be uncomfortably tight or unwearable

**too_large**
- User measurement above max+tolerance
- Score: <70
- Meaning: Will be uncomfortably loose or unwearable

---

### **Size Order**
Sequential ranking of sizes from smallest to largest.

**Example:**
```
XS → 1
S  → 2
M  → 3
L  → 4
XL → 5
```

**Uses:**
- Comparing alternatives ("Size up" vs "Size down")
- Generating fit notes

---

## Database Terms

### **Brand**
Clothing manufacturer or retailer (e.g., Nike, Adidas, Zara).

**Properties:**
- Brand ID
- Brand name
- Optional: country, sizing system

---

### **Category**
Type of garment (e.g., T-Shirt, Jeans, Dress, Jacket).

**Properties:**
- Category ID
- Category name
- Required measurements (chest, waist, hips, etc.)

---

### **Fit Type**
Style variation within a garment category.

**Common values:**
- Regular/Classic
- Slim/Fitted
- Relaxed/Loose
- Athletic
- Oversized

**Impact:** Same brand, same category, different fit type = different size charts

---

### **Sizing System**
Regional standards for size labels.

**Examples:**
- US: S, M, L, XL
- EU: 36, 38, 40, 42
- UK: 8, 10, 12, 14
- Japan: 1, 2, 3, 4

---

### **Measurement Type**
Body dimension being measured.

**Common types:**
- chest / bust
- waist
- hips
- shoulder_width
- sleeve_length
- inseam
- outseam
- neck

---

## Algorithm Terms

### **Multi-Criteria Decision Making (MCDM)**
Mathematical framework for making choices based on multiple factors.

**In our context:**
- Criteria = measurements (chest, waist, etc.)
- Alternatives = sizes (S, M, L)
- Weights = importance of each measurement
- Decision = which size to recommend

---

### **Weighted Sum Model (WSM)**
MCDM method that multiplies criteria values by weights and sums them.

**Formula:**
$$A_i = \sum_{j=1}^{n} w_j \times x_{ij}$$

Where:
- $A_i$ = score for alternative i
- $w_j$ = weight for criterion j
- $x_{ij}$ = value for alternative i, criterion j

**Our implementation:** Weighted average of measurement scores

---

### **Normalization**
Scaling values to common range for fair comparison.

**In our algorithm:**
- All scores normalized to 0-100
- Weights applied after normalization
- Final score also 0-100

---

### **Fuzzy Boundaries**
Concept where transitions between categories are gradual, not sharp.

**In our algorithm:**
- Tolerance creates "fuzzy zone"
- Scores gradually decrease outside range
- Not binary (fit/no-fit) but continuous

---

### **Sensitivity Analysis**
Testing how changes in inputs affect outputs.

**Example Questions:**
- How does increasing tolerance affect scores?
- How sensitive is recommendation to weight changes?
- What if one measurement is missing?

---

## Measurement Terms

### **Body Measurements**
Physical dimensions of a person's body.

**How obtained:**
- Self-measurement with tape measure
- Professional measurement
- 3D body scanning (future)
- Historical purchase data (future)

**Units:** Always centimeters (cm) in our system

---

### **Garment Measurements**
Physical dimensions of the clothing item itself.

**Note:** Often different from body measurements
- Garment chest might be larger than body chest (ease)
- Our system uses body-to-size-range matching

---

### **Ease**
Extra room built into garment beyond exact body measurements.

**Typically:**
- Fitted shirts: 2-4 cm ease
- Regular shirts: 5-8 cm ease
- Oversized: 10+ cm ease

**In our system:** Reflected in size range width

---

## Statistical Terms

### **Accuracy**
Percentage of correct recommendations.

**Formula:**
```
Accuracy = Correct recommendations / Total recommendations
```

**Example:** 87 out of 100 recommendations matched user's actual size = 87% accuracy

---

### **Precision**
When system recommends a size, how often is it correct?

**Formula:**
```
Precision = True Positives / (True Positives + False Positives)
```

---

### **Recall**
Of all correct sizes, how many did system find?

**Formula:**
```
Recall = True Positives / (True Positives + False Negatives)
```

---

### **Confidence Interval**
Range of uncertainty around a measurement or prediction.

**Example:**
"We recommend Size M with 95% confidence" means:
- 95% probability M is correct
- 5% probability another size might be better

---

## Technical Terms

### **API Endpoint**
URL that accepts requests and returns recommendations.

**Example:**
```
POST /api/size-match
Body: {
  "measurements": {"chest": 98, "waist": 84},
  "brand_id": 5,
  "category_id": 2
}
```

---

### **JSON Response**
Structured data format returned by API.

**Example:**
```json
{
  "recommended_size": "M",
  "confidence": 98,
  "match_score": 97,
  "alternatives": ["L", "S"]
}
```

---

### **Singleton Pattern**
Design pattern ensuring only one instance of service exists.

**In code:**
```python
size_matching_service = SizeMatchingService()
# Single shared instance used throughout application
```

---

## Common Abbreviations

- **cm** - Centimeters
- **min** - Minimum
- **max** - Maximum
- **opt** - Optimal
- **tol** - Tolerance
- **meas** - Measurement
- **conf** - Confidence
- **WSM** - Weighted Sum Model
- **MCDM** - Multi-Criteria Decision Making
- **API** - Application Programming Interface

---

## Quick Reference: Typical Values

### Score Thresholds
- 90+ = Excellent
- 75-89 = Good
- 60-74 = Acceptable
- <60 = Poor

### Confidence Levels
- 90%+ = Very confident
- 75-89% = Confident
- 60-74% = Moderate
- <60% = Low confidence

### Typical Weights
- Critical measurements: 1.5-2.0
- Important measurements: 1.0-1.4
- Less critical: 0.5-0.9

### Typical Tolerance
- Rigid garments: 2-3 cm
- Stretch garments: 4-6 cm
- Very stretchy: 8-10 cm

---

## Usage in Sentences

**For Research Panel:**

"The algorithm calculates a **match score** for each size by comparing user measurements to the size's **measurement range**. Measurements closer to the **optimal value** receive higher scores. The **tolerance** parameter allows for acceptable fits slightly outside the range. **Weights** ensure that critical measurements like chest for shirts have more influence than less critical ones like sleeve length. The final **confidence score** reflects both the match quality and the gap between the best and second-best options."

**For Technical Audience:**

"We implement a **weighted sum model** where each measurement receives a score based on its **deviation** from the size **range**. Scores are **normalized** to 0-100, weighted by importance, and aggregated. **Confidence** is calculated using a two-factor model considering match quality and separation gap."

**For General Audience:**

"We score how well your body measurements fit each size in a brand's size chart. Better fits get higher scores. We then pick the size with the best score and tell you how confident we are in that choice."
