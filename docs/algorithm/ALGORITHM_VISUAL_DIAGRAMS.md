# Size Matching Algorithm - Visual Diagrams for Research Panel

## 1. 📏 SCORING ZONES DIAGRAM

### Single Measurement Scoring System

```
Score
100 |                    ╔═══════╗
    |                    ║PERFECT║
 95 |              ╔═════╩═══════╩═════╗
    |              ║   GOOD MATCH      ║
 90 |══════════════╩═══════════════════╩══════════════
    |         ║                             ║
 80 |    ╔════╝                             ╚════╗
    |    ║  ACCEPTABLE (Within Tolerance)       ║
 70 |════╩════════════════════════════════════════╩════
    |  ║                                           ║
 50 |  ║         POOR FIT                          ║
    |  ║      (Beyond Tolerance)                   ║
  0 |══╩═══════════════════════════════════════════╩══
    |  |    |         |         |         |    |    |
       A    B        MIN     OPTIMAL     MAX   D    E
      (Too           (Range)             (Range)   (Too
      Small)                                       Large)

Legend:
  A = min - tolerance - excess
  B = min - tolerance  
  MIN = Minimum size range
  OPTIMAL = Best fit point
  MAX = Maximum size range
  D = max + tolerance
  E = max + tolerance + excess
```

### Numeric Example: Chest Measurement for Size M

```
Chest Size M: Range 94-100 cm, Optimal 97 cm, Tolerance 3 cm

Score
100 |                    97
    |                    ▲
 95 |              94 ───┴─── 100
    |              └───────────┘
 90 |══════════════════════════════════════
    |         │                       │
 80 |    ╔════╝                       ╚════╗
    |    91                               103
 70 |════╩═════════════════════════════════╩════
    |  │                                     │
 50 |  88                                  106
    |  │                                     │
  0 |══╩═════════════════════════════════════╩══
    88  91   94      97      100  103      106

User Chest Measurements:
  88 cm → Score: ~20  (Too small, beyond tolerance)
  91 cm → Score: ~77  (Slightly small, within tolerance)
  94 cm → Score: ~90  (Perfect fit, at minimum range)
  97 cm → Score: 100  (Perfect fit, at optimal)
 100 cm → Score: ~90  (Perfect fit, at maximum range)
 103 cm → Score: ~77  (Slightly large, within tolerance)
 106 cm → Score: ~20  (Too large, beyond tolerance)
```

---

## 2. 📊 SCORING FORMULA VISUALIZATION

### Case 1: Within Range (Perfect Fit Zone)

```
User value between MIN and MAX

         OPTIMAL
            │
    ┌───────┼───────┐
   MIN             MAX
    │               │
    └───────────────┘
      Range Width

Score = 100 - (distance_from_optimal / range_width) × 10
Bounded: max(90, min(100, score))

Example:
  Range: 94-100 cm (width=6cm), Optimal: 97 cm
  User: 99 cm
  
  Distance from optimal: |99-97| = 2 cm
  Score = 100 - (2/6) × 10 = 100 - 3.33 = 96.67
```

### Case 2: Within Tolerance (Acceptable Zone)

```
User value outside range but within tolerance

    TOLERANCE │         │ TOLERANCE
       ◄──────┼─────────┼──────►
              MIN     MAX

Score = 90 - (deviation / tolerance) × 20
Bounded: max(70, score)

Example:
  Range: 94-100 cm, Tolerance: 3 cm
  User: 102 cm
  
  Deviation: 102-100 = 2 cm
  Score = 90 - (2/3) × 20 = 90 - 13.33 = 76.67
```

### Case 3: Beyond Tolerance (Poor Fit Zone)

```
User value far outside acceptable range

    POOR  │  TOLERANCE │    RANGE    │ TOLERANCE │  POOR
    ◄─────┼─────◄──────┼─────────────┼──────►────┼─────►
                       MIN         MAX

Score = 70 - (excess_deviation × 10)
Penalty: 10 points per cm beyond tolerance
Bounded: max(0, score)

Example:
  Range: 94-100 cm, Tolerance: 3 cm
  User: 108 cm
  
  Deviation: 108-100 = 8 cm
  Excess: 8-3 = 5 cm beyond tolerance
  Penalty: 5 × 10 = 50 points
  Score = 70 - 50 = 20
```

---

## 3. ⚖️ WEIGHTED AGGREGATION DIAGRAM

### Multi-Measurement Scoring Process

```
USER MEASUREMENTS              SIZE M CHART
┌─────────────────┐           ┌──────────────────┐
│ Chest:    98 cm │    vs     │ 94-100 cm        │ → Score: 98
│ Waist:    84 cm │    vs     │ 80-88 cm         │ → Score: 100
│ Shoulder: 46 cm │    vs     │ 44-47 cm         │ → Score: 96
│ Sleeve:   23 cm │    vs     │ 22-24 cm         │ → Score: 95
└─────────────────┘           └──────────────────┘
         ↓                              ↓
         └──────────────┬───────────────┘
                        ↓
              ┌─────────────────┐
              │ APPLY WEIGHTS   │
              └─────────────────┘
                        ↓
    ┌───────────────────────────────────────┐
    │  Chest:    98 × 1.5 = 147.0          │
    │  Waist:   100 × 0.8 = 80.0           │
    │  Shoulder: 96 × 1.2 = 115.2          │
    │  Sleeve:   95 × 0.5 = 47.5           │
    │                      ───────          │
    │  Total:              389.7           │
    │  Total Weight:       4.0             │
    │                                      │
    │  Final Score: 389.7 / 4.0 = 97.4    │
    └───────────────────────────────────────┘
```

### Weight Distribution Example (T-Shirt)

```
           IMPORTANCE WEIGHT
Chest      ████████████████  1.5  ← Most critical
Shoulder   ████████████      1.2
Waist      ████████          0.8
Sleeve     █████             0.5  ← Least critical

Why? Chest fit determines if shirt is wearable.
     Sleeve length is more forgiving.
```

---

## 4. 🎯 CONFIDENCE CALCULATION DIAGRAM

### Two-Factor Confidence Model

```
                    CONFIDENCE SCORE
                          │
            ┌─────────────┴─────────────┐
            │                           │
      FACTOR 1                    FACTOR 2
   Match Quality              Separation Gap
 (How good is best?)      (How clear is winner?)
         │                          │
         ↓                          ↓
   Best Score = 95           Gap = 95 - 78 = 17
         │                          │
         └──────────┬───────────────┘
                    ↓
            Confidence = 95 + (17 × 0.5)
            Confidence = 103.5 → Capped at 100
            
            FINAL: 100% Confident
```

### Confidence Scenarios Graph

```
Confidence
   100% │     A ●
        │       
    95% │           
        │         B ●
    90% │
        │              
    85% │                  
        │                  C ●
    80% │
        │
    75% │                        
        │                        D ●
    70% │────┬────┬────┬────┬────┬────┬────┬────
        0    5   10   15   20   25   30   35
                Score Gap (Best - Second)

Scenario A: Best=95, Second=78 → Gap=17 → Confidence=100%
Scenario B: Best=92, Second=85 → Gap=7  → Confidence=92%
Scenario C: Best=85, Second=83 → Gap=2  → Confidence=77%
Scenario D: Best=68, Second=65 → Gap=3  → Confidence=61%

Key Insight: Large gaps increase confidence;
            Small gaps decrease confidence
```

---

## 5. 🔄 COMPLETE WORKFLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PHASE                              │
│  User: {chest:98, waist:84, hips:96}                        │
│  Query: Nike T-Shirt, Regular Fit                           │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE QUERY                             │
│  → Retrieve Nike T-Shirt size chart                         │
│  → Get sizes: XS, S, M, L, XL, XXL                          │
│  → Get measurement requirements & weights                   │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              SCORING PHASE (FOR EACH SIZE)                  │
│                                                             │
│  Size XS:  Score = 45  ──┐                                 │
│  Size S:   Score = 72  ──┤                                 │
│  Size M:   Score = 97  ──┤─→ Sort by score                 │
│  Size L:   Score = 78  ──┤                                 │
│  Size XL:  Score = 58  ──┤                                 │
│  Size XXL: Score = 42  ──┘                                 │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   RANKING PHASE                             │
│  1st: Size M  (97) ← BEST MATCH                            │
│  2nd: Size L  (78)                                          │
│  3rd: Size S  (72)                                          │
│  4th: Size XL (58)                                          │
│  5th: Size XS (45)                                          │
│  6th: Size XXL(42)                                          │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              CONFIDENCE CALCULATION                         │
│  Best Score: 97                                             │
│  Gap to 2nd: 97 - 78 = 19 (Large gap!)                     │
│  Confidence: 97 + (19 × 0.5) = 106.5 → Capped at 100       │
│  FINAL CONFIDENCE: 100%                                     │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                FIT ADVICE GENERATION                        │
│  ✅ Excellent fit! Size M matches very well                 │
│  • Chest: Perfect fit (98cm in range 94-100cm)             │
│  • Waist: Perfect fit (84cm matches optimal)               │
│  • No sizing issues detected                               │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  OUTPUT PHASE                               │
│  {                                                          │
│    recommended_size: "M",                                   │
│    confidence: 100,                                         │
│    match_score: 97,                                         │
│    alternatives: ["L", "S"],                                │
│    fit_advice: [...]                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 📈 SCORE DISTRIBUTION COMPARISON

### Good Recommendation (Clear Winner)

```
Score
100 │     M ████████████████████████  97
    │
 80 │              L ███████████████  78
    │
 60 │                   S ███████████  72
    │                      XL ████████  58
 40 │                         XS █████  45
    │                         XXL ████  42
  0 └──────┬────┬────┬────┬────┬──────
          XS   S    M    L    XL  XXL

Analysis: Clear winner (M), high confidence
Recommendation: Size M with 100% confidence
```

### Ambiguous Recommendation (Close Scores)

```
Score
100 │
    │
 80 │     M ████████████████████  85
    │     L ███████████████████   83
    │
 60 │          S █████████████     75
    │             XL ███████████   72
 40 │
    │
  0 └──────┬────┬────┬────┬────┬──────
          XS   S    M    L    XL  XXL

Analysis: M and L very close, uncertain winner
Recommendation: Try both M and L (76% confidence)
```

### Poor Recommendation (All Low Scores)

```
Score
100 │
    │
 80 │
    │
 60 │     M ██████████  62
    │     L █████████   58
    │     S ████████    54
 40 │     XL ███████    50
    │
  0 └──────┬────┬────┬────┬────┬──────
          XS   S    M    L    XL  XXL

Analysis: All sizes fit poorly
Recommendation: Consider other brands (56% confidence)
```

---

## 7. 🎨 MEASUREMENT FIT CATEGORIES

### Visual Fit Assessment Matrix

```
                    TOO      SLIGHTLY   PERFECT   SLIGHTLY    TOO
                   SMALL      SMALL               LARGE      LARGE
                     │          │         │         │          │
Score Range:        0-69      70-89    90-100    70-89      0-69
                     │          │         │         │          │
User Position:  ◄────┴────►◄───┴───►◄───┴───►◄───┴────►◄────┴────►
                     │     │    │    │    │    │    │     │    │
  Beyond         (min-tol) min  opt  max (max+tol)    Beyond
 Tolerance                                            Tolerance

Example for Chest 94-100cm, Tolerance 3cm:

 88cm ──► TOO_SMALL        (Beyond tolerance, won't fit)
 91cm ──► SLIGHTLY_SMALL   (Within tolerance, tight fit)
 94cm ──► PERFECT          (At range minimum)
 97cm ──► PERFECT          (At optimal)
100cm ──► PERFECT          (At range maximum)
103cm ──► SLIGHTLY_LARGE   (Within tolerance, loose fit)
106cm ──► TOO_LARGE        (Beyond tolerance, won't fit)
```

---

## 8. 💡 DECISION TREE VISUALIZATION

```
                      USER MEASUREMENT
                            │
                            ↓
                ┌───────────────────────┐
                │    Within Range?      │
                │ (min ≤ user ≤ max)    │
                └───────────┬───────────┘
                           / \
                      YES /   \ NO
                         /     \
                        ↓       ↓
            ┌──────────────┐  ┌──────────────────┐
            │ At Optimal?  │  │ Within Tolerance?│
            └──────┬───────┘  └────────┬─────────┘
                  / \                  / \
             YES /   \ NO         YES /   \ NO
                /     \               /     \
               ↓       ↓             ↓       ↓
          ┌──────┐  ┌─────┐    ┌──────┐  ┌──────┐
          │Score │  │Score│    │Score │  │Score │
          │ 100  │  │90-99│    │70-89 │  │ 0-69 │
          └──────┘  └─────┘    └──────┘  └──────┘
             │         │           │         │
             └─────────┴───────────┴─────────┘
                         │
                         ↓
                  Apply Weight
                         │
                         ↓
              Contribution to Total Score
```

---

## 9. 📊 COMPARATIVE ANALYSIS TABLE

### How Different Users Score for Same Size

```
Size M: Chest Range 94-100cm (Optimal: 97cm), Tolerance: 3cm

┌──────────────┬─────────────┬──────────┬─────────────┬─────────────┐
│ User Chest   │ Position    │ Distance │ Fit Status  │ Score       │
├──────────────┼─────────────┼──────────┼─────────────┼─────────────┤
│ 88 cm        │ Way Below   │ -6 cm    │ Too Small   │ 20 (Poor)   │
│ 91 cm        │ Below       │ -3 cm    │ Slightly ↓  │ 77 (OK)     │
│ 94 cm        │ At Min      │ -3 cm    │ Perfect     │ 90 (Great)  │
│ 95 cm        │ Near Opt    │ -2 cm    │ Perfect     │ 97 (Great)  │
│ 97 cm ★      │ At Optimal  │  0 cm    │ Perfect     │ 100 (Best)  │
│ 99 cm        │ Near Opt    │ +2 cm    │ Perfect     │ 97 (Great)  │
│ 100 cm       │ At Max      │ +3 cm    │ Perfect     │ 90 (Great)  │
│ 103 cm       │ Above       │ +3 cm    │ Slightly ↑  │ 77 (OK)     │
│ 108 cm       │ Way Above   │ +8 cm    │ Too Large   │ 20 (Poor)   │
└──────────────┴─────────────┴──────────┴─────────────┴─────────────┘

★ = Optimal fit point
↓ = Small/tight     ↑ = Large/loose
```

---

## 10. 🔬 ALGORITHM SENSITIVITY ANALYSIS

### How Tolerance Affects Scoring

```
User Chest: 102 cm (2cm beyond Size M max of 100cm)

Tolerance = 1 cm:
  102 > 101 → Beyond tolerance → Score: 50 (Poor fit)
  
Tolerance = 3 cm:
  102 ≤ 103 → Within tolerance → Score: 77 (Acceptable)
  
Tolerance = 5 cm:
  102 ≤ 105 → Within tolerance → Score: 82 (Good)

Graph:
Score
100 │
    │                        ┌─────────────
 80 │              ┌─────────┤
    │    Tol=5────►│         │
 60 │         ┌────┤Tol=3   Tol=1
    │         │    │         │
 40 │    Tol=1│    │         │
    └────┬────┬────┬────┬────┬────┬────
        98   99  100  101  102  103  104
                 (User: 102cm)

Key: Higher tolerance = More forgiving scoring
```

---

## PRESENTATION TIPS

### Visual Aid Recommendations:

1. **Print Slide 1 (Scoring Zones)** - Core concept visual
2. **Hand out Slide 3 (Weighted Aggregation)** - Shows calculation
3. **Animate Slide 5 (Workflow)** - Shows step-by-step process
4. **Use Slide 9 (Comparison Table)** - Concrete examples

### Color Coding Suggestions:
- 🟢 Green: Perfect fit (90-100)
- 🟡 Yellow: Acceptable (70-89)
- 🔴 Red: Poor fit (0-69)

### Interactive Demo Ideas:
1. Live calculation with audience member's measurements
2. Show how changing one measurement affects score
3. Compare multiple brands for same person
