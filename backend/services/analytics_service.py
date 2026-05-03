"""
Advanced Analytics Service
Provides wear pattern insights, cost analysis, seasonal trends, and forgotten items tracking
"""

import json
import logging
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path
import sys

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent.parent))

import database

logger = logging.getLogger(__name__)


class AdvancedAnalyticsService:
    """Service for advanced wardrobe analytics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_wear_pattern_insights(self):
        """
        Analyze wear patterns: most/least worn, cost per wear, frequency analysis
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get all items with wear history
        cursor.execute('''
            SELECT id, filename, image_path, clothing_type, wear_count, 
                   last_worn, wear_history, purchase_price, purchase_date, 
                   created_at, primary_color
            FROM wardrobe_items
        ''')
        items = cursor.fetchall()
        conn.close()
        
        if not items:
            return {
                'mostWorn': [],
                'leastWorn': [],
                'costPerWear': [],
                'totalValue': 0,
                'totalCostPerWear': 0
            }
        
        # Process items
        items_data = []
        total_value = 0
        total_spent = 0
        
        for item in items:
            wear_count = item['wear_count'] or 0
            purchase_price = item['purchase_price']
            
            cost_per_wear = None
            if purchase_price and wear_count > 0:
                cost_per_wear = purchase_price / wear_count
                total_spent += purchase_price
                
            if purchase_price:
                total_value += purchase_price
            
            items_data.append({
                'id': item['id'],
                'filename': item['filename'],
                'url': item['image_path'],
                'type': item['clothing_type'],
                'wearCount': wear_count,
                'lastWorn': item['last_worn'],
                'purchasePrice': purchase_price,
                'purchaseDate': item['purchase_date'],
                'costPerWear': round(cost_per_wear, 2) if cost_per_wear else None,
                'primaryColor': item['primary_color'],
                'wearHistory': json.loads(item['wear_history']) if item['wear_history'] else []
            })
        
        # Sort for most/least worn
        sorted_by_wear = sorted(items_data, key=lambda x: x['wearCount'], reverse=True)
        most_worn = sorted_by_wear[:10]
        least_worn = [item for item in sorted_by_wear if item['wearCount'] == 0][:10]
        if not least_worn:
            least_worn = sorted_by_wear[-10:]
        
        # Sort by cost per wear (best value items)
        items_with_cost = [item for item in items_data if item['costPerWear'] is not None]
        best_value_items = sorted(items_with_cost, key=lambda x: x['costPerWear'])[:10]
        
        return {
            'mostWorn': most_worn,
            'leastWorn': least_worn,
            'costPerWear': best_value_items,
            'totalValue': round(total_value, 2),
            'totalSpent': round(total_spent, 2),
            'averageCostPerWear': round(total_spent / sum(item['wearCount'] for item in items_data if item['wearCount'] > 0), 2) if total_spent > 0 else 0
        }
    
    def get_wear_frequency_timeline(self, period='monthly', limit=12):
        """
        Get wear frequency timeline (daily/weekly/monthly)
        
        Args:
            period: 'daily', 'weekly', or 'monthly'
            limit: Number of periods to return
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT wear_history FROM wardrobe_items WHERE wear_history != "[]"')
        rows = cursor.fetchall()
        conn.close()
        
        # Collect all wear events
        all_wears = []
        for row in rows:
            history = json.loads(row['wear_history']) if row['wear_history'] else []
            for wear in history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    if 'date' in wear:
                        all_wears.append({
                            'date': wear['date'],
                            'occasion': wear.get('occasion', 'Unknown')
                        })
                elif isinstance(wear, str):
                    all_wears.append({
                        'date': wear,
                        'occasion': 'Unknown'
                    })
        
        if not all_wears:
            return {'timeline': [], 'period': period}
        
        # Group by period
        timeline = defaultdict(int)
        
        for wear in all_wears:
            try:
                wear_date = datetime.fromisoformat(wear['date'])
                
                if period == 'daily':
                    key = wear_date.strftime('%Y-%m-%d')
                elif period == 'weekly':
                    # Get week start (Monday)
                    week_start = wear_date - timedelta(days=wear_date.weekday())
                    key = week_start.strftime('%Y-%m-%d')
                elif period == 'monthly':
                    key = wear_date.strftime('%Y-%m')
                else:
                    key = wear_date.strftime('%Y-%m-%d')
                
                timeline[key] += 1
            except Exception as e:
                self.logger.error(f"Error parsing date {wear['date']}: {e}")
                continue
        
        # Sort by date and limit
        sorted_timeline = sorted(timeline.items(), key=lambda x: x[0], reverse=True)[:limit]
        sorted_timeline.reverse()  # Chronological order
        
        # Calculate trend
        if len(sorted_timeline) >= 2:
            first_half = sorted_timeline[:len(sorted_timeline)//2]
            second_half = sorted_timeline[len(sorted_timeline)//2:]
            first_avg = sum(v for k, v in first_half) / len(first_half)
            second_avg = sum(v for k, v in second_half) / len(second_half)
            trend = 'increasing' if second_avg > first_avg else 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'timeline': [{'date': k, 'wears': v} for k, v in sorted_timeline],
            'period': period,
            'trend': trend,
            'totalWears': sum(timeline.values())
        }
    
    def get_seasonal_analysis(self):
        """
        Analyze what items are worn in each season
        Determine season from wear dates if season column is not set
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, image_path, clothing_type, wear_count, 
                   wear_history, season, primary_color
            FROM wardrobe_items
        ''')
        items = cursor.fetchall()
        conn.close()
        
        # Season mapping (Northern Hemisphere)
        def get_season_from_date(date_str):
            try:
                dt = datetime.fromisoformat(date_str)
                month = dt.month
                if month in [3, 4, 5]:
                    return 'spring'
                elif month in [6, 7, 8]:
                    return 'summer'
                elif month in [9, 10, 11]:
                    return 'fall'
                else:
                    return 'winter'
            except:
                return None
        
        seasonal_data = {
            'spring': {'items': [], 'totalWears': 0, 'topColors': []},
            'summer': {'items': [], 'totalWears': 0, 'topColors': []},
            'fall': {'items': [], 'totalWears': 0, 'topColors': []},
            'winter': {'items': [], 'totalWears': 0, 'topColors': []}
        }
        
        for item in items:
            wear_history = json.loads(item['wear_history']) if item['wear_history'] else []
            
            # Determine which seasons this item is worn in
            season_wears = defaultdict(int)
            seasons_colors = defaultdict(list)
            
            for wear in wear_history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    date_str = wear.get('date', '')
                elif isinstance(wear, str):
                    date_str = wear
                else:
                    continue
                
                season = get_season_from_date(date_str)
                if season:
                    season_wears[season] += 1
                    if item['primary_color']:
                        seasons_colors[season].append(item['primary_color'])
            
            # Add item to seasons where it's worn
            for season, count in season_wears.items():
                seasonal_data[season]['items'].append({
                    'id': item['id'],
                    'filename': item['filename'],
                    'url': item['image_path'],
                    'type': item['clothing_type'],
                    'seasonWears': count,
                    'primaryColor': item['primary_color']
                })
                seasonal_data[season]['totalWears'] += count
            
            # If item has explicit season tag, ensure it's in that season's list
            if item['season'] and item['season'] in seasonal_data:
                # Check if already added
                existing = any(i['id'] == item['id'] for i in seasonal_data[item['season']]['items'])
                if not existing:
                    seasonal_data[item['season']]['items'].append({
                        'id': item['id'],
                        'filename': item['filename'],
                        'url': item['image_path'],
                        'type': item['clothing_type'],
                        'seasonWears': 0,
                        'primaryColor': item['primary_color'],
                        'tagged': True
                    })
        
        # Calculate top colors for each season
        for season in seasonal_data:
            colors = []
            for item in seasonal_data[season]['items']:
                if item.get('primaryColor'):
                    colors.extend([item['primaryColor']] * item.get('seasonWears', 1))
            
            color_counts = Counter(colors)
            seasonal_data[season]['topColors'] = [
                {'color': color, 'count': count} 
                for color, count in color_counts.most_common(5)
            ]
            
            # Sort items by wear count
            seasonal_data[season]['items'] = sorted(
                seasonal_data[season]['items'], 
                key=lambda x: x.get('seasonWears', 0), 
                reverse=True
            )[:15]  # Top 15 items per season
        
        return seasonal_data
    
    def get_event_preference_tracking(self):
        """
        Track which events the user attends most and item usage by event
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT wear_history FROM wardrobe_items WHERE wear_history != "[]"')
        rows = cursor.fetchall()
        conn.close()
        
        # Collect all occasions
        occasion_counts = Counter()
        occasion_items = defaultdict(set)
        
        for row in rows:
            history = json.loads(row['wear_history']) if row['wear_history'] else []
            for wear in history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    occasion = wear.get('occasion', 'Unknown')
                elif isinstance(wear, str):
                    occasion = 'Unknown'
                else:
                    continue
                    
                occasion_counts[occasion] += 1
        
        # Get items per occasion
        cursor = database.get_connection().cursor()
        cursor.execute('SELECT id, best_event, wear_count, filename, image_path FROM wardrobe_items')
        items = cursor.fetchall()
        cursor.close()
        
        event_stats = []
        for occasion, count in occasion_counts.most_common(10):
            matching_items = [
                {
                    'id': item['id'],
                    'filename': item['filename'],
                    'url': item['image_path'],
                    'wearCount': item['wear_count']
                }
                for item in items if item['best_event'] == occasion
            ]
            
            event_stats.append({
                'event': occasion,
                'attendanceCount': count,
                'itemsForEvent': len(matching_items),
                'topItems': sorted(matching_items, key=lambda x: x['wearCount'], reverse=True)[:5]
            })
        
        return {
            'totalEvents': len(occasion_counts),
            'eventStats': event_stats,
            'mostAttendedEvent': occasion_counts.most_common(1)[0] if occasion_counts else None
        }
    
    def get_forgotten_items(self, days_threshold=90):
        """
        Get forgotten items alert - items not worn in specified days
        
        Args:
            days_threshold: Number of days to consider item as "forgotten"
        """
        items = database.get_unworn_items_since(days_threshold)
        
        # Add individual suggestions to each item
        items_with_suggestions = []
        for item in items:
            days = item.get('daysSinceWorn') or 0
            
            # Generate item-specific suggestion
            if days >= 180:
                suggestion = f"Unworn for {days//30} months - consider donating"
            elif days >= 120:
                suggestion = f"Try pairing with your favorite items"
            elif days == 0 or days is None:
                suggestion = "Never worn - plan an outfit around this"
            else:
                suggestion = f"{days} days unworn - time to wear it!"
            
            items_with_suggestions.append({
                **item,
                'suggestion': suggestion
            })
        
        return {
            'count': len(items),
            'items': items_with_suggestions,
            'message': f"{len(items)} Items Not Worn in {days_threshold}+ Days"
        }
    
    def _generate_forgotten_suggestions(self, items):
        """Generate suggestions for forgotten items"""
        suggestions = []
        
        if len(items) > 0:
            suggestions.append("Consider creating outfits with these unused items")
        
        if len(items) >= 5:
            suggestions.append("Review these items - consider donating unworn pieces")
        
        if len(items) >= 10:
            suggestions.append(f"You have {len(items)} rarely used items taking up space")
            suggestions.append("Consider selling high-value unworn items")
        
        # Group by type
        type_counts = Counter(item['type'] for item in items)
        for clothing_type, count in type_counts.most_common(3):
            if count >= 3:
                suggestions.append(f"You have {count} rarely worn {clothing_type}s")
        
        return suggestions
    
    def get_cost_per_wear_analysis(self):
        """
        Detailed cost per wear analysis
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, image_path, clothing_type, wear_count, 
                   purchase_price, purchase_date, primary_color
            FROM wardrobe_items
            WHERE purchase_price IS NOT NULL
        ''')
        items = cursor.fetchall()
        conn.close()
        
        analysis = []
        for item in items:
            wear_count = item['wear_count'] or 0
            price = item['purchase_price']
            
            cost_per_wear = price / wear_count if wear_count > 0 else price
            
            # Calculate ROI (lower cost per wear = better ROI)
            if wear_count > 0:
                roi_score = min(100, (price / (cost_per_wear * 10)) * 100)  # Normalized to 0-100
            else:
                roi_score = 0
            
            analysis.append({
                'id': item['id'],
                'filename': item['filename'],
                'url': item['image_path'],
                'type': item['clothing_type'],
                'purchasePrice': price,
                'wearCount': wear_count,
                'costPerWear': round(cost_per_wear, 2),
                'roiScore': round(roi_score, 1),
                'valueRating': self._get_value_rating(cost_per_wear, wear_count)
            })
        
        # Sort by best value (lowest cost per wear for worn items)
        worn_items = [item for item in analysis if item['wearCount'] > 0]
        all_sorted = sorted(analysis, key=lambda x: x['costPerWear'])
        best_value = sorted(worn_items, key=lambda x: x['costPerWear'])[:10]
        
        # Worst value (high cost per wear)
        worst_value = sorted(worn_items, key=lambda x: x['costPerWear'], reverse=True)[:10]
        
        # Unworn expensive items (money wasted)
        unworn_expensive = sorted(
            [item for item in analysis if item['wearCount'] == 0],
            key=lambda x: x['purchasePrice'],
            reverse=True
        )[:10]
        
        return {
            'items': all_sorted,  # All items sorted by cost per wear (for frontend table)
            'bestValue': best_value,
            'worstValue': worst_value,
            'unwornExpensive': unworn_expensive,
            'totalInvested': sum(item['purchasePrice'] for item in analysis),
            'averageCostPerWear': round(sum(item['costPerWear'] for item in worn_items) / len(worn_items), 2) if worn_items else 0
        }
    
    def _get_value_rating(self, cost_per_wear, wear_count):
        """Rate the value of an item"""
        if wear_count == 0:
            return 'Unworn'
        elif cost_per_wear < 1:
            return 'Excellent Value'
        elif cost_per_wear < 5:
            return 'Great Value'
        elif cost_per_wear < 10:
            return 'Good Value'
        elif cost_per_wear < 20:
            return 'Fair Value'
        else:
            return 'Poor Value'
    
    def get_seasonal_wear_distribution(self):
        """
        Analyze wear distribution across seasons
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT wear_history FROM wardrobe_items WHERE wear_history != "[]"')
        rows = cursor.fetchall()
        conn.close()
        
        season_wears = {
            'spring': 0,
            'summer': 0,
            'fall': 0,
            'winter': 0
        }
        
        def get_season_from_date(date_str):
            try:
                dt = datetime.fromisoformat(date_str)
                month = dt.month
                if month in [3, 4, 5]:
                    return 'spring'
                elif month in [6, 7, 8]:
                    return 'summer'
                elif month in [9, 10, 11]:
                    return 'fall'
                else:
                    return 'winter'
            except:
                return None
        
        for row in rows:
            history = json.loads(row['wear_history']) if row['wear_history'] else []
            for wear in history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    date_str = wear.get('date', '')
                elif isinstance(wear, str):
                    date_str = wear
                else:
                    continue
                    
                season = get_season_from_date(date_str)
                if season:
                    season_wears[season] += 1
        
        total = sum(season_wears.values())
        
        return {
            'seasonalWears': season_wears,
            'percentages': {
                season: round((count / total * 100), 1) if total > 0 else 0
                for season, count in season_wears.items()
            },
            'totalWears': total,
            'mostActiveSeasons': sorted(season_wears.items(), key=lambda x: x[1], reverse=True)
        }
    
    def get_comprehensive_dashboard(self):
        """
        Get all analytics data for the dashboard
        """
        try:
            wear_patterns = self.get_wear_pattern_insights()
            frequency = self.get_wear_frequency_timeline(period='monthly', limit=12)
            seasonal = self.get_seasonal_analysis()
            events = self.get_event_preference_tracking()
            forgotten = self.get_forgotten_items(days_threshold=90)
            cost_analysis = self.get_cost_per_wear_analysis()
            
            return {
                'wearPatterns': wear_patterns,
                'frequencyTimeline': frequency,
                'seasonalAnalysis': seasonal,
                'eventPreferences': events,
                'forgottenItems': forgotten,
                'costAnalysis': cost_analysis,
                'generatedAt': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error generating dashboard: {e}")
            raise


# Singleton instance
analytics_service = AdvancedAnalyticsService()
