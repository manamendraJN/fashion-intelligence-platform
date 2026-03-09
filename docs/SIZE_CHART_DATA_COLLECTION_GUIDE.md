# Garment Size Chart Data Collection Guide

## Overview

This guide provides comprehensive instructions for collecting reliable garment size chart data from clothing brands for the Fashion Intelligence Platform research project.

---

## 📋 Table of Contents

1. [Data Collection Strategy](#data-collection-strategy)
2. [Where to Find Size Charts](#where-to-find-size-charts)
3. [Data Extraction Methods](#data-extraction-methods)
4. [Data Recording Template](#data-recording-template)
5. [Quality Assurance](#quality-assurance)
6. [Brand Selection Criteria](#brand-selection-criteria)
7. [Common Challenges](#common-challenges)

---

## 🎯 Data Collection Strategy

### Research Prototype Scope

For this research prototype, we recommend starting with:
- **6-10 brands** representing different markets (athletic, casual, formal, fast fashion)
- **3-5 garment categories** (e.g., T-shirts, Jeans, Dresses, Jackets)
- **Both genders** for comprehensive coverage
- **Standard fit types** (Regular fit initially, then expand to Slim/Relaxed/Athletic)

### Priority Measurements

Focus on collecting these body measurements for each garment type:

| Garment Type | Critical Measurements | Secondary Measurements |
|--------------|----------------------|------------------------|
| **T-Shirts/Tops** | Chest, Shoulder Breadth | Waist, Arm Length |
| **Dress Shirts** | Chest, Shoulder Breadth, Arm Length | Waist |
| **Jeans/Pants** | Waist, Hip, Leg Length | Thigh, Calf |
| **Dresses** | Chest (Bust), Waist, Hip | Shoulder Breadth |
| **Jackets** | Chest, Shoulder Breadth, Arm Length | Waist |

---

## 🔍 Where to Find Size Charts

### 1. Official Brand Websites

**Most Reliable Source** - Brand websites typically have official size charts under:
- Product pages (look for "Size Guide" button)
- Footer links: "Size Guide", "Fit Guide", "Sizing Information"
- Help/FAQ sections

**Popular Brand Examples:**
```
Nike:        https://www.nike.com/size-fit
Adidas:      https://www.adidas.com/us/help/size_charts
Zara:        https://www.zara.com/us/en/help/size-guide
H&M:         https://www2.hm.com/en_us/customer-service/sizeguide.html
Levi's:      https://www.levi.com/US/en_US/size-chart
Uniqlo:      https://www.uniqlo.com/us/en/size
Gap:         https://www.gap.com/browse/sizeChart.do
Old Navy:    https://oldnavy.gap.com/browse/sizeChart.do
J.Crew:      https://www.jcrew.com/sizecharts/main.jsp
Banana Rep:  https://bananarepublic.gap.com/browse/sizeChart.do
```

### 2. Retailer Aggregator Sites

Multi-brand retailers often compile size charts:
- Amazon (brand storefronts)
- Zappos (detailed shoe/clothing charts)
- Nordstrom (standardized size information)
- ASOS (size guides per brand)

### 3. Brand Catalogs and PDFs

Some brands provide downloadable size charts:
- Look for "Fit Guide PDF" or "Size Chart PDF"
- Usually found in "Customer Support" sections

### 4. Physical Store Inquiry

For brands without online size charts:
- Call customer service and request sizing information
- Visit physical stores and photograph size charts
- Request sizing information via email

---

## 📊 Data Extraction Methods

### Method 1: Manual Extraction (Most Accurate)

**Steps:**
1. Navigate to brand's official size guide
2. Identify the specific garment category
3. Note the sizing system (US, UK, EU, or International)
4. Record measurements for each size in centimeters
5. Convert from inches if necessary (1 inch = 2.54 cm)
6. Document fit type (Regular, Slim, Relaxed, etc.)

**Example Screenshot Workflow:**
```
1. Take screenshot of size chart
2. Save with naming convention: BrandName_GarmentType_Gender_Date.png
3. Extract data into spreadsheet
4. Verify measurements against multiple sources if possible
```

### Method 2: Web Scraping (For Multiple Brands)

**Tools:**
- Python with BeautifulSoup or Selenium
- Browser developer tools to inspect HTML structure
- Excel/CSV for data organization

**Sample Code Structure:**
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_size_chart(url, brand_name):
    # Fetch page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find size table (varies by website)
    table = soup.find('table', class_='size-chart')
    
    # Extract data
    # ... parsing logic ...
    
    return size_data_df
```

**⚠️ Important:**
- Respect robots.txt and terms of service
- Add delays between requests
- For research purposes only

### Method 3: API Access (Rare)

Some brands provide APIs for product information that may include sizing:
- Check brand developer portals
- Usually requires registration and API key

---

## 📝 Data Recording Template

### Excel/CSV Template Structure

Create a spreadsheet with these columns:

```
Brand Name | Country | Size System | Category | Gender | Fit Type | Size Label | Size Order | Measurement Type | Min (cm) | Max (cm) | Optimal (cm) | Notes | Date Collected | Source URL
```

**Example Data:**

| Brand | Country | System | Category | Gender | Fit | Size | Order | Measurement | Min | Max | Optimal | Notes | Date | Source |
|-------|---------|--------|----------|--------|-----|------|-------|-------------|-----|-----|---------|-------|------|--------|
| Nike | USA | US | T-Shirt | Men | Regular | M | 3 | Chest | 91 | 97 | 94 | Athletic fit | 2024-03-08 | nike.com/size |
| Nike | USA | US | T-Shirt | Men | Regular | M | 3 | Shoulder | 44 | 46 | 45 | - | 2024-03-08 | nike.com/size |

### JSON Format (For Direct Database Import)

```json
{
  "brand": "Nike",
  "brand_country": "USA",
  "size_system": "US",
  "category": "T-Shirt",
  "gender": "Men",
  "fit_type": "Regular",
  "sizes": [
    {
      "label": "M",
      "order": 3,
      "measurements": {
        "chest": {"min": 91, "max": 97, "optimal": 94},
        "shoulder_breadth": {"min": 44, "max": 46, "optimal": 45},
        "waist": {"min": 81, "max": 86, "optimal": 83.5}
      }
    }
  ],
  "source_url": "https://www.nike.com/size-fit",
  "date_collected": "2024-03-08"
}
```

---

## ✅ Quality Assurance

### Validation Checklist

Before adding data to the database:

- [ ] **Measurement Units Verified**: All measurements in centimeters
- [ ] **Consistency Check**: Min < Max for all ranges
- [ ] **Logical Progression**: Sizes increase consistently (XS < S < M < L < XL)
- [ ] **Source Documented**: URL and date recorded
- [ ] **Multiple Verification**: Cross-checked with at least one other source if possible
- [ ] **Fit Type Specified**: Regular/Slim/Relaxed clearly indicated
- [ ] **Gender Confirmed**: Men's/Women's/Unisex clearly specified

### Common Errors to Avoid

1. **Unit Confusion**: Mixing inches and centimeters
2. **Garment vs Body Measurements**: Some charts show garment dimensions, not body measurements
3. **Regional Variations**: EU size 40 ≠ US size 40
4. **Fit Type Mixing**: Don't combine regular and slim fit in same chart
5. **Outdated Data**: Size charts may change; note collection date

### Verification Strategies

1. **Compare Multiple Sources**: Check brand's website, Amazon listing, and retailer sites
2. **Logical Range Check**: Typical adult chest ranges 80-130cm, waist 60-120cm
3. **Cross-Brand Comparison**: Similar sizes across brands should be comparable
4. **Customer Reviews**: Check if customers mention sizing issues

---

## 🎯 Brand Selection Criteria

### Recommended Brand Categories

**1. Athletic/Sportswear (2-3 brands)**
- Nike, Adidas, Under Armour, Puma
- Well-documented size charts
- International presence

**2. Fast Fashion (2-3 brands)**
- Zara, H&M, Forever 21, Uniqlo
- Broad size ranges
- Frequent updates

**3. Denim/Casual (1-2 brands)**
- Levi's, Wrangler, Lee, Gap
- Numeric sizing (jeans)
- Long history of standardization

**4. Formal/Business (1-2 brands)**
- Brooks Brothers, J.Crew, Banana Republic
- Professional sizing
- Detailed measurements

**5. Premium/Designer (Optional)**
- For variability research
- Often have more detailed size charts

### Selection Priority Matrix

| Priority | Criteria | Weight |
|----------|----------|--------|
| High | Has detailed online size chart | 40% |
| High | International brand | 20% |
| Medium | Multiple garment categories | 20% |
| Medium | Clear body measurement specifications | 10% |
| Low | Brand popularity/recognition | 10% |

---

## 🚧 Common Challenges

### Challenge 1: Inconsistent Chart Formats

**Problem**: Every brand presents size charts differently

**Solution**: 
- Create a standardized extraction template
- Focus on extracting core measurements
- Document any brand-specific notes

### Challenge 2: Garment vs. Body Measurements

**Problem**: Some charts show garment dimensions, not body measurements

**Solution**:
- Look for "body measurements" label explicitly
- If only garment measurements available, note this in database
- Consider applying conversion factors (research recommended ease allowances)

### Challenge 3: Missing Measurements

**Problem**: Not all measurements available for every garment

**Solution**:
- Record what's available
- Mark missing measurements as NULL in database
- Algorithm will work with available measurements

### Challenge 4: International Size Conversions

**Problem**: US 8 ≠ UK 8 ≠ EU 8

**Solution**:
- Always store the original size system
- Focus on body measurements (cm) not size labels
- Database schema supports multiple size systems per brand

### Challenge 5: Dynamic/Interactive Size Charts

**Problem**: Some websites use interactive JavaScript tools

**Solution**:
- Use browser developer tools to inspect network requests
- Take screenshots at different selections
- Consider using Selenium for automated extraction

---

## 🛠️ Data Collection Tools

### Recommended Software

1. **Spreadsheet**: Excel, Google Sheets, LibreOffice Calc
2. **Web Scraping**: Python (BeautifulSoup, Scrapy, Selenium)
3. **Screenshot**: Windows Snipping Tool, macOS Screenshot, Lightshot
4. **Unit Conversion**: Google Calculator, ConvertUnits.com
5. **Data Validation**: Python pandas, Excel Data Validation

### Measurement Converter

Quick reference for common conversions:

| Inches | Centimeters | | Inches | Centimeters |
|--------|-------------|---|--------|-------------|
| 30" | 76.2 cm | | 38" | 96.5 cm |
| 32" | 81.3 cm | | 40" | 101.6 cm |
| 34" | 86.4 cm | | 42" | 106.7 cm |
| 36" | 91.4 cm | | 44" | 111.8 cm |

---

## 📦 Next Steps

### After Data Collection

1. **Data Validation**: Run quality checks on collected data
2. **Database Import**: Use provided Python scripts to populate database
3. **Algorithm Testing**: Test size matching with sample measurements
4. **Iteration**: Add more brands/categories based on initial results

### Expanding the Dataset

As your research progresses:
- Add seasonal variations (winter vs summer fits)
- Include specialty categories (athletic, maternity, plus-size)
- Document brand-specific sizing patterns
- Track sizing changes over time

---

## 📚 Additional Resources

### Academic References

For understanding garment sizing standards:
- ASTM D5585 (Standard Table of Body Measurements for Adult Male)
- ASTM D5586 (Standard Table of Body Measurements for Adult Female)
- ISO 8559 (Garment construction and anthropometric surveys)

### Online Communities

- Reddit: r/femalefashionadvice, r/malefashionadvice (sizing discussions)
- Fashion forums with sizing databases
- Brand-specific communities

---

## 📞 Support

For questions about data collection or database schema:
- Review database schema: `backend/database/schema.sql`
- Sample data script: `backend/database/populate_sample_data.py`
- Database documentation in project README

---

**Document Version**: 1.0  
**Last Updated**: 2024-03-08  
**Author**: Fashion Intelligence Platform Research Team
