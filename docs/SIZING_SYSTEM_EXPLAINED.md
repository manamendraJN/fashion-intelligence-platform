# Sizing System Explanation

## Why Am I Seeing "24" Instead of S/M/L?

Different garment types use **different sizing systems**. The recommendation engine correctly returns the appropriate size format based on the garment category you selected.

## Sizing Systems by Garment Type

### 📏 Letter Sizes (XS, S, M, L, XL, XXL)
Used for:
- **T-Shirts** (Men's & Women's)
- **Polo Shirts**
- **Dress Shirts**
- **Blouses**
- **Dresses**
- **Jackets**

Example from database:
- Nike Men's T-Shirt: XS, S, M, L, XL, XXL
- Adidas Women's T-Shirt: XS, S, M, L, XL
- H&M Women's Dress: XS, S, M, L, XL

### 🔢 Numeric Sizes (24, 26, 28, 30, 32, 34, etc.)
Used for:
- **Jeans** (Men's & Women's)
- **Pants**
- **Trousers**

These numbers represent **waist circumference in inches**.

Example from database:
- **Women's Jeans**: 24, 25, 26, 27, 28, 29, 30, 32, 34
- **Men's Jeans**: 28, 30, 32, 34, 36, 38

## Your Current Situation

Based on the diagnostic, you received size **"24"** which means:

✅ You selected **Jeans (Women)** as your garment category
✅ Size 24 = 24-inch waist (approx. 61cm)
✅ This is found in: Zara, H&M, Levi's, and Uniqlo women's jeans

### Low Match Score (32.7%)

The low confidence score suggests:
- Your measurements may fall between sizes
- You might be closer to size 26 or size 28
- The algorithm is less confident about this recommendation

## How to Get Letter Sizes (S/M/L/XL)

To receive letter sizes instead of numeric sizes:

1. **Select a Different Category:**
   - Choose "T-Shirt (Men)" or "T-Shirt (Women)"
   - Choose "Dress (Women)"
   - Choose "Jacket" or "Polo Shirt"

2. **Avoid Selecting:**
   - "Jeans (Men)" or "Jeans (Women)" → Returns numeric waist sizes
   - "Pants" or "Trousers" → Returns numeric waist sizes

## Database Status Confirmation

✅ **Correct table structure** - All 8 tables present:
   - brands
   - garment_categories  
   - size_charts
   - sizes
   - size_measurements
   - category_measurements
   - user_measurements
   - recommendation_log

✅ **Data populated successfully:**
   - 6 brands (Nike, Adidas, Zara, H&M, Levi's, Uniqlo)
   - 10 garment categories
   - 20 size charts
   - 111 individual sizes
   - 333 measurement data points

✅ **Size "24" correctly exists in:**
   - Zara Jeans (Women)
   - H&M Jeans (Women)
   - Levi's Jeans (Women)
   - Uniqlo Jeans (Women)

## Recommendation

If you want S/M/L/XL sizes:
1. Go back to the size recommendation page
2. Select **"T-Shirt (Men)"** or **"T-Shirt (Women)"**
3. Keep your measurements the same
4. Click "Get Size Recommendation"

Expected result: You should receive a size like "M" or "L" instead of "24"

## Size Conversion Reference

### Women's Jeans (Numeric → Letter Equivalent)
- Size 24-25 ≈ XXS
- Size 26-27 ≈ XS
- Size 28-29 ≈ S
- Size 30-31 ≈ M
- Size 32-33 ≈ L
- Size 34+ ≈ XL+

### Men's Jeans
- Size 28-29 ≈ XS
- Size 30-31 ≈ S
- Size 32-33 ≈ M
- Size 34-36 ≈ L
- Size 38+ ≈ XL+

**Note:** These conversions are approximate. Always use the size system specific to the garment type.
