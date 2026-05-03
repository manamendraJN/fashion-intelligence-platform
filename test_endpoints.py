"""
Test all frontend-required analytics endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

print("🧪 Testing Analytics Endpoints\n")
print("="*70)

# Test 1: Basic Analytics
print("\n1. Testing /api/analytics")
try:
    r = requests.get(f'{BASE_URL}/api/analytics', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'stats': {'stats' in data}")
    print(f"   ✅ Has 'charts': {'charts' in data}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Advanced Analytics
print("\n2. Testing /api/analytics/advanced")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/advanced', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'mostWorn': {'mostWorn' in data}")
    print(f"   ✅ Has 'leastWorn': {'leastWorn' in data}")
    print(f"   ✅ Has 'eventFrequency': {'eventFrequency' in data}")
    print(f"   ✅ Has 'seasonDistribution': {'seasonDistribution' in data}")
    print(f"   ✅ Has 'colorDistribution': {'colorDistribution' in data}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Style Profile
print("\n3. Testing /api/analytics/style-profile")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/style-profile', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'dominantStyle': {'dominantStyle' in data}")
    print(f"   ✅ Has 'totalAnalyzedWears': {'totalAnalyzedWears' in data}")
    print(f"   ✅ Has 'stylePersonality': {'stylePersonality' in data}")
    print(f"   ✅ Has 'colorPalette.favoriteColor': {'colorPalette' in data and 'favoriteColor' in data.get('colorPalette', {})}")
    print(f"   ✅ Has 'insights': {'insights' in data}")
    print(f"   ✅ Has 'categoryBreakdown': {'categoryBreakdown' in data}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Forgotten Items
print("\n4. Testing /api/analytics/forgotten-items?threshold=90")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/forgotten-items?threshold=90', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'count': {'count' in data}")
    print(f"   ✅ Has 'items': {'items' in data}")
    print(f"   ✅ Has 'message': {'message' in data}")
    print(f"   📊 Count: {data.get('count', 0)}")
    if 'items' in data and len(data['items']) > 0:
        print(f"   ✅ First item has 'suggestion': {'suggestion' in data['items'][0]}")
        print(f"   📋 First item keys: {list(data['items'][0].keys())}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Cost Efficiency
print("\n5. Testing /api/analytics/cost-efficiency")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/cost-efficiency', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'items': {'items' in data}")
    if 'items' in data and len(data['items']) > 0:
        print(f"   📊 Items count: {len(data['items'])}")
        print(f"   📋 First item keys: {list(data['items'][0].keys())}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Wear Timeline
print("\n6. Testing /api/analytics/wear-timeline?days=90&granularity=weekly")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/wear-timeline?days=90&granularity=weekly', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'timeline': {'timeline' in data}")
    print(f"   ✅ Has 'trend': {'trend' in data}")
    if 'timeline' in data and len(data['timeline']) > 0:
        print(f"   📊 Timeline points: {len(data['timeline'])}")
        print(f"   📋 First point keys: {list(data['timeline'][0].keys())}")
        print(f"   📈 Trend: {data.get('trend', 'N/A')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 7: Predictions
print("\n7. Testing /api/analytics/predictions")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/predictions', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   ✅ Has 'predictions': {'predictions' in data}")
    if 'predictions' in data and len(data['predictions']) > 0:
        print(f"   📊 Predictions count: {len(data['predictions'])}")
        print(f"   📋 First prediction item keys: {list(data['predictions'][0]['item'].keys())}")
        print(f"   ⚡ Score: {data['predictions'][0]['score']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 8: Seasonal
print("\n8. Testing /api/analytics/seasonal")
try:
    r = requests.get(f'{BASE_URL}/api/analytics/seasonal', timeout=5)
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   Response keys: {list(data.keys())}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ All endpoint tests completed!")
