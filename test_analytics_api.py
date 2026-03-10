"""
API Test for Advanced Analytics
Quick HTTP tests for all new analytics endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_endpoint(method, endpoint, description, params=None, data=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"🔍 Testing: {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            
            # Print key info from response
            if 'analytics' in data:
                print(f"   📊 Dashboard components: {len(data['analytics'])} sections")
            elif 'styleProfile' in data:
                profile = data['styleProfile']
                print(f"   👔 Dominant Style: {profile.get('dominantStyle')}")
                print(f"   🎯 Confidence: {profile['styleConfidence']['score']}/100")
            elif 'patterns' in data:
                patterns = data['patterns']
                print(f"   📈 Most worn items: {len(patterns['mostWorn'])}")
                print(f"   💰 Total value: ${patterns['totalValue']:.2f}")
            elif 'costAnalysis' in data:
                cost = data['costAnalysis']
                print(f"   💵 Total invested: ${cost['totalInvested']:.2f}")
                print(f"   📊 Best value items: {len(cost['bestValue'])}")
            elif 'timeline' in data:
                timeline = data['timeline']['timeline']
                print(f"   📅 Timeline entries: {len(timeline)}")
            elif 'seasonal' in data:
                seasonal = data['seasonal']
                print(f"   🌸 Total wears: {seasonal['totalWears']}")
            elif 'events' in data:
                events = data['events']
                print(f"   🎉 Total events: {events['totalEvents']}")
            elif 'forgottenItems' in data:
                forgotten = data['forgottenItems']
                print(f"   ⚠️  {forgotten['message']}")
            elif 'colorPalette' in data:
                palette = data['colorPalette']
                print(f"   🎨 Color diversity: {palette['colorDiversity']} colors")
            elif 'combinations' in data:
                combos = data['combinations']
                print(f"   👕 Total outfits: {combos['totalOutfits']}")
            elif 'evolution' in data:
                evo = data['evolution']
                print(f"   📈 Months analyzed: {evo['monthsAnalyzed']}")
            
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error - Is the server running?")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Test all analytics API endpoints"""
    print("\n" + "🔬 " * 35)
    print("  API TESTING: Advanced Analytics & Style Profile")
    print("🔬 " * 35)
    
    # Check server status
    print("\n🔍 Checking server status...")
    try:
        response = requests.get(f"{BASE_URL}/api/wardrobe/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Server is running at {BASE_URL}")
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
    except:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print("   Please start the server with: cd backend; python app.py")
        return
    
    # Test Advanced Analytics Endpoints
    print_header("🔷 ADVANCED ANALYTICS ENDPOINTS")
    
    test_endpoint("GET", "/api/analytics/advanced", 
                  "Comprehensive Analytics Dashboard")
    
    test_endpoint("GET", "/api/analytics/wear-patterns", 
                  "Wear Pattern Insights")
    
    test_endpoint("GET", "/api/analytics/cost-per-wear", 
                  "Cost Per Wear Analysis")
    
    test_endpoint("GET", "/api/analytics/timeline", 
                  "Wear Frequency Timeline (Monthly)", 
                  params={'period': 'monthly', 'limit': 12})
    
    test_endpoint("GET", "/api/analytics/timeline", 
                  "Wear Frequency Timeline (Weekly)", 
                  params={'period': 'weekly', 'limit': 8})
    
    test_endpoint("GET", "/api/analytics/seasonal", 
                  "Seasonal Analysis")
    
    test_endpoint("GET", "/api/analytics/events", 
                  "Event Preference Tracking")
    
    test_endpoint("GET", "/api/analytics/forgotten-items", 
                  "Forgotten Items Alert (90 days)", 
                  params={'days': 90})
    
    # Test Style Profile Endpoints
    print_header("🔷 STYLE PROFILE ENDPOINTS (LSTM-Powered)")
    
    test_endpoint("GET", "/api/style/profile", 
                  "Personal Style Profile with LSTM")
    
    test_endpoint("GET", "/api/style/color-palette", 
                  "Color Palette Analysis")
    
    test_endpoint("GET", "/api/style/combinations", 
                  "Outfit Combination Intelligence")
    
    test_endpoint("GET", "/api/style/evolution", 
                  "Style Evolution Timeline", 
                  params={'months': 6})
    
    # Test Update Endpoint
    print_header("🔷 DATA UPDATE ENDPOINTS")
    
    test_endpoint("PUT", "/api/wardrobe/154/purchase-info", 
                  "Update Purchase Info",
                  data={
                      'purchasePrice': 59.99,
                      'purchaseDate': '2025-01-15',
                      'season': 'winter'
                  })
    
    print("\n" + "="*70)
    print("  🎉 API TESTING COMPLETE!")
    print("="*70)
    
    print("\n📚 Quick Reference:")
    print("  • /api/analytics/advanced - All analytics in one call")
    print("  • /api/style/profile - LSTM-powered style insights")
    print("  • /api/analytics/forgotten-items?days=90 - Unworn items alert")


if __name__ == '__main__':
    main()
