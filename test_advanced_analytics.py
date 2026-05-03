"""
Test Advanced Analytics and Style Profile Features
Tests the new analytics dashboard and LSTM-powered style analyzer
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

sys.path.append(str(Path(__file__).parent / 'backend'))

# Import database first
import database

# Import services directly to avoid circular imports
import sys
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path / 'services'))

from analytics_service import AdvancedAnalyticsService
from style_analyzer import StyleProfileAnalyzer

import json
from datetime import datetime, timedelta

# Initialize services
analytics_service = AdvancedAnalyticsService()
style_analyzer = StyleProfileAnalyzer()


def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_database_schema():
    """Test that new database columns exist"""
    print_section("1. Testing Database Schema Updates")
    
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(wardrobe_items)")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    
    required_columns = ['purchase_price', 'purchase_date', 'season']
    
    for col in required_columns:
        if col in columns:
            print(f"  ✅ Column '{col}' exists")
        else:
            print(f"  ❌ Column '{col}' missing")
    
    print(f"\n  Total columns: {len(columns)}")


def test_add_sample_purchase_data():
    """Add sample purchase data to test items"""
    print_section("2. Adding Sample Purchase Data")
    
    items = database.get_all_wardrobe_items()
    
    if not items:
        print("  ⚠️  No items in wardrobe. Please add items first.")
        return
    
    # Add sample purchase info to first 5 items
    sample_data = [
        {'price': 29.99, 'date': '2025-01-15', 'season': 'winter'},
        {'price': 49.99, 'date': '2025-02-20', 'season': 'spring'},
        {'price': 35.00, 'date': '2024-11-10', 'season': 'fall'},
        {'price': 89.99, 'date': '2025-03-01', 'season': 'spring'},
        {'price': 19.99, 'date': '2024-12-25', 'season': 'winter'},
    ]
    
    for i, item in enumerate(items[:5]):
        if i < len(sample_data):
            data = sample_data[i]
            success = database.update_item_purchase_info(
                item['id'],
                purchase_price=data['price'],
                purchase_date=data['date'],
                season=data['season']
            )
            if success:
                print(f"  ✅ Updated item #{item['id']} - ${data['price']} ({data['season']})")


def test_wear_pattern_insights():
    """Test wear pattern analysis"""
    print_section("3. Testing Wear Pattern Insights")
    
    patterns = analytics_service.get_wear_pattern_insights()
    
    print(f"\n  📊 Most Worn Items:")
    for item in patterns['mostWorn'][:5]:
        print(f"     • {item['filename']} - Worn {item['wearCount']} times")
    
    print(f"\n  📊 Least Worn Items:")
    for item in patterns['leastWorn'][:5]:
        print(f"     • {item['filename']} - Worn {item['wearCount']} times")
    
    print(f"\n  💰 Best Value Items:")
    for item in patterns['costPerWear'][:5]:
        if item['costPerWear']:
            print(f"     • {item['filename']} - ${item['costPerWear']:.2f} per wear")
    
    print(f"\n  📈 Summary:")
    print(f"     Total Wardrobe Value: ${patterns['totalValue']:.2f}")
    print(f"     Total Spent: ${patterns['totalSpent']:.2f}")
    print(f"     Average Cost Per Wear: ${patterns['averageCostPerWear']:.2f}")


def test_wear_frequency_timeline():
    """Test wear frequency timeline"""
    print_section("4. Testing Wear Frequency Timeline")
    
    for period in ['monthly', 'weekly', 'daily']:
        timeline = analytics_service.get_wear_frequency_timeline(period=period, limit=5)
        print(f"\n  📅 {period.upper()} Timeline:")
        print(f"     Total Wears: {timeline['totalWears']}")
        for entry in timeline['timeline']:
            print(f"     • {entry['period']}: {entry['wears']} wears")


def test_seasonal_analysis():
    """Test seasonal analysis"""
    print_section("5. Testing Seasonal Analysis")
    
    seasonal = analytics_service.get_seasonal_analysis()
    
    for season in ['spring', 'summer', 'fall', 'winter']:
        data = seasonal[season]
        print(f"\n  🌸 {season.upper()}:")
        print(f"     Total Wears: {data['totalWears']}")
        print(f"     Items: {len(data['items'])}")
        if data['topColors']:
            print(f"     Top Colors: {', '.join([c['color'] for c in data['topColors'][:3]])}")


def test_event_preferences():
    """Test event preference tracking"""
    print_section("6. Testing Event Preference Tracking")
    
    events = analytics_service.get_event_preference_tracking()
    
    print(f"\n  🎉 Total Events Attended: {events['totalEvents']}")
    if events['mostAttendedEvent']:
        print(f"  🏆 Most Attended: {events['mostAttendedEvent'][0]} ({events['mostAttendedEvent'][1]} times)")
    
    print(f"\n  📊 Event Statistics:")
    for event_stat in events['eventStats'][:5]:
        print(f"     • {event_stat['event']}: {event_stat['attendanceCount']} times, {event_stat['itemsForEvent']} items")


def test_forgotten_items():
    """Test forgotten items detection"""
    print_section("7. Testing Forgotten Items Alert")
    
    forgotten = analytics_service.get_forgotten_items(days_threshold=90)
    
    print(f"\n  ⚠️  {forgotten['message']}")
    print(f"  📦 Very Forgotten (6+ months): {len(forgotten['veryForgotten'])}")
    print(f"  📦 Forgotten (3-6 months): {len(forgotten['forgotten'])}")
    
    print(f"\n  💡 Suggestions:")
    for suggestion in forgotten['suggestions'][:5]:
        print(f"     • {suggestion}")


def test_style_profile():
    """Test style profile analysis with LSTM"""
    print_section("8. Testing Style Profile Analysis (LSTM-Powered)")
    
    profile = style_analyzer.analyze_style_profile()
    
    print(f"\n  👔 Dominant Style: {profile['dominantStyle']}")
    
    print(f"\n  📊 Style Breakdown:")
    for style, percentage in profile['styleBreakdown'].items():
        print(f"     • {style}: {percentage}%")
    
    print(f"\n  🎨 Color Palette:")
    print(f"     Top Colors: {', '.join(profile['colorPalette']['topColors'][:5])}")
    
    print(f"\n  🎯 Style Confidence:")
    conf = profile['styleConfidence']
    print(f"     Score: {conf['score']}/100")
    print(f"     Level: {conf['level']}")
    print(f"     {conf['description']}")
    
    print(f"\n  🔮 LSTM Prediction:")
    pred = profile['futurePrediction']
    if pred.get('available'):
        print(f"     Next Likely Event: {pred['nextLikelyEvent']}")
        print(f"     Confidence: {pred['confidence']:.2%}")
        print(f"     Model: {pred['modelUsed']}")
        print(f"     {pred['interpretation']}")
    else:
        print(f"     {pred.get('message', 'Not available')}")


def test_color_palette_analysis():
    """Test detailed color analysis"""
    print_section("9. Testing Color Palette Analysis")
    
    palette = style_analyzer.get_color_palette_analysis()
    
    print(f"\n  🎨 Color Diversity: {palette['colorDiversity']} unique colors")
    print(f"  🏆 Most Worn Color: {palette['mostWornColor']}")
    print(f"  ✨ Color Personality: {palette['colorPersonality']}")
    
    print(f"\n  📊 Top Primary Colors:")
    for color_data in palette['topPrimaryColors'][:5]:
        print(f"     • {color_data['color']}: {color_data['wearCount']} wears")


def test_outfit_combinations():
    """Test outfit combination intelligence"""
    print_section("10. Testing Outfit Combination Intelligence")
    
    combinations = style_analyzer.get_outfit_combination_intelligence()
    
    print(f"\n  👕 Total Outfits Tracked: {combinations['totalOutfits']}")
    print(f"  🔄 Unique Combinations: {combinations['uniqueCombinations']}")
    print(f"  📏 Average Items Per Outfit: {combinations['averageItemsPerOutfit']}")
    
    print(f"\n  🔥 Top Combinations:")
    for combo in combinations['topCombinations'][:5]:
        types_str = ' + '.join(combo['types'])
        print(f"     • {types_str}: {combo['frequency']} times")


def test_style_evolution():
    """Test style evolution timeline"""
    print_section("11. Testing Style Evolution Timeline")
    
    evolution = style_analyzer.get_style_evolution_timeline(months=6)
    
    print(f"\n  📈 Months Analyzed: {evolution['monthsAnalyzed']}")
    
    for month_data in evolution['timeline']:
        print(f"\n  📅 {month_data['month']}:")
        print(f"     Total Wears: {month_data['totalWears']}")
        if month_data['topEvent']:
            print(f"     Top Event: {month_data['topEvent']}")
        if month_data['topColor']:
            print(f"     Top Color: {month_data['topColor']}")
        if month_data['topType']:
            print(f"     Top Type: {month_data['topType']}")


def test_comprehensive_dashboard():
    """Test the complete dashboard"""
    print_section("12. Testing Comprehensive Dashboard")
    
    print("\n  🔄 Generating comprehensive dashboard...")
    dashboard = analytics_service.get_comprehensive_dashboard()
    
    print(f"\n  ✅ Dashboard Generated Successfully!")
    print(f"  📊 Components:")
    print(f"     • Wear Patterns: {len(dashboard['wearPatterns']['mostWorn'])} most worn items")
    print(f"     • Timeline: {len(dashboard['frequencyTimeline']['timeline'])} periods")
    
    # Calculate total seasonal wears
    total_seasonal_wears = sum(
        dashboard['seasonalAnalysis'][season]['totalWears'] 
        for season in ['spring', 'summer', 'fall', 'winter']
    )
    print(f"     • Seasonal: {total_seasonal_wears} total seasonal wears")
    print(f"     • Events: {dashboard['eventPreferences']['totalEvents']} unique events")
    print(f"     • Forgotten: {dashboard['forgottenItems']['totalForgotten']} items")
    print(f"     • Cost Analysis: ${dashboard['costAnalysis']['totalInvested']:.2f} invested")
    print(f"\n  🕐 Generated At: {dashboard['generatedAt']}")


def main():
    """Run all tests"""
    print("\n" + "🚀 " * 35)
    print("  TESTING ADVANCED ANALYTICS & STYLE PROFILE FEATURES")
    print("🚀 " * 35)
    
    try:
        # Test database schema
        test_database_schema()
        
        # Add sample data
        test_add_sample_purchase_data()
        
        # Test analytics features
        test_wear_pattern_insights()
        test_wear_frequency_timeline()
        test_seasonal_analysis()
        test_event_preferences()
        test_forgotten_items()
        
        # Test style profile features
        test_style_profile()
        test_color_palette_analysis()
        test_outfit_combinations()
        test_style_evolution()
        
        # Test comprehensive dashboard
        test_comprehensive_dashboard()
        
        print("\n" + "="*70)
        print("  ✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📝 API Endpoints Available:")
        print("  • GET  /api/analytics/advanced - Full dashboard")
        print("  • GET  /api/analytics/wear-patterns - Wear insights")
        print("  • GET  /api/analytics/cost-per-wear - Cost analysis")
        print("  • GET  /api/analytics/timeline?period=monthly - Timeline")
        print("  • GET  /api/analytics/seasonal - Seasonal analysis")
        print("  • GET  /api/analytics/events - Event tracking")
        print("  • GET  /api/analytics/forgotten-items?days=90 - Forgotten items")
        print("\n  • GET  /api/style/profile - Style profile (LSTM)")
        print("  • GET  /api/style/color-palette - Color analysis")
        print("  • GET  /api/style/combinations - Outfit patterns")
        print("  • GET  /api/style/evolution?months=6 - Style timeline")
        print("  • PUT  /api/wardrobe/<id>/purchase-info - Update price/date")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
