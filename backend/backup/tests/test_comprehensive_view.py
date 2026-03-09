import requests
import json

# Test the comprehensive view endpoint
url = 'http://localhost:5000/api/admin/comprehensive-view'

try:
    response = requests.get(url)
    result = response.json()
    
    if result['success']:
        print("✅ Comprehensive View API Working!")
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        # Brand summary
        brand_summary = result['data']['brand_summary']
        print(f"\nTotal Brands: {len(brand_summary)}")
        
        for brand in brand_summary:
            print(f"\n{brand['brand_name']} ({brand['country']}, {brand['size_system']})")
            print(f"  Total Categories: {brand['total_categories']}")
            print(f"  Total Sizes: {brand['total_sizes']}")
            
            gender_info = []
            if brand['men_categories'] > 0:
                gender_info.append(f"♂ {brand['men_categories']} Men")
            if brand['women_categories'] > 0:
                gender_info.append(f"♀ {brand['women_categories']} Women")
            if brand['unisex_categories'] > 0:
                gender_info.append(f"⚥ {brand['unisex_categories']} Unisex")
            
            if gender_info:
                print(f"  Gender Distribution: {', '.join(gender_info)}")
        
        # Gender distribution
        print("\n" + "="*80)
        print("GENDER DISTRIBUTION")
        print("="*80)
        
        gender_dist = result['data']['gender_distribution']
        for item in gender_dist:
            print(f"{item['brand_name']} - {item['gender']}: {item['category_count']} categories, {item['size_count']} sizes")
        
        # Sample comprehensive data (first 5 rows)
        print("\n" + "="*80)
        print("SAMPLE DATA (First 5 rows)")
        print("="*80)
        
        comprehensive_data = result['data']['comprehensive_data'][:5]
        for row in comprehensive_data:
            print(f"\n{row['brand_name']} > {row['category_name']} ({row['gender']}) > Size {row['size_label']}")
            if row['chest_min']:
                print(f"  Chest: {row['chest_min']}-{row['chest_max']} cm")
            if row['waist_min']:
                print(f"  Waist: {row['waist_min']}-{row['waist_max']} cm")
    else:
        print(f"❌ Error: {result['error']}")
        
except Exception as e:
    print(f"❌ Failed to connect: {e}")
