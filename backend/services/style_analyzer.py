"""
Smart Style Profile Analyzer
Uses LSTM/GRU models and wear history to analyze personal style evolution
"""

import json
import logging
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path
import sys
import numpy as np

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

import database
from services.wardrobe_model_service import WardrobeModelService

logger = logging.getLogger(__name__)


class StyleProfileAnalyzer:
    """Analyze and predict personal style preferences using ML models"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            # Get the model directory path
            model_dir = Path(__file__).parent.parent / 'models' / 'wardrobe models'
            self.model_service = WardrobeModelService(model_dir)
            self.logger.info("✅ Style Analyzer initialized with ML models")
        except Exception as e:
            self.logger.warning(f"ML models not available: {e}")
            self.model_service = None
    
    def analyze_style_profile(self):
        """
        Comprehensive style profile analysis
        - Analyzes wear history to determine dominant styles
        - Color palette preferences
        - Event frequency patterns
        - Style confidence/adventurousness score
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, image_path, clothing_type, wear_count, 
                   wear_history, best_event, primary_color, all_colors
            FROM wardrobe_items
        ''')
        items = cursor.fetchall()
        conn.close()
        
        if not items:
            return self._empty_profile()
        
        # Analyze wear patterns
        total_wears = sum(item['wear_count'] for item in items)
        
        # Event/occasion analysis
        event_counts = Counter()
        color_counts = Counter()
        type_counts = Counter()
        
        for item in items:
            # Count by event type
            if item['best_event']:
                event_counts[item['best_event']] += item['wear_count']
            
            # Count by clothing type
            if item['clothing_type']:
                type_counts[item['clothing_type']] += item['wear_count']
            
            # Count colors worn
            if item['primary_color']:
                color_counts[item['primary_color']] += item['wear_count']
        
        # Calculate style preferences
        style_breakdown = self._calculate_style_breakdown(event_counts, total_wears)
        
        # Color palette (top colors with percentages)
        top_colors_with_percentage = [
            {'color': color, 'count': count, 'percentage': round(count/total_wears*100, 1) if total_wears > 0 else 0}
            for color, count in color_counts.most_common(10)
        ]
        favorite_color = color_counts.most_common(1)[0][0] if color_counts else None
        
        # Outfit combination patterns (from wear history)
        combination_patterns = self._analyze_combination_patterns(items)
        
        # Style confidence score
        confidence_score = self._calculate_style_confidence(items, event_counts, color_counts)
        
        # Category breakdown (clothing types as percentages)
        category_breakdown = {}
        if total_wears > 0:
            for typ, count in type_counts.items():
                category_breakdown[typ] = round((count / total_wears) * 100, 1)
        
        # Generate insights
        insights = self._generate_style_insights(event_counts, color_counts, type_counts, confidence_score)
        
        # Predict future style preferences using LSTM
        future_prediction = self._predict_style_evolution(items)
        
        return {
            'dominantStyle': style_breakdown['dominant'],
            'totalAnalyzedWears': total_wears,
            'styleBreakdown': style_breakdown['breakdown'],
            'stylePersonality': {
                'classicScore': round(style_breakdown['breakdown'].get('formal', 0) + style_breakdown['breakdown'].get('casual', 0) * 0.5, 1),
                'adventurousScore': round(style_breakdown['breakdown'].get('party', 0) + style_breakdown['breakdown'].get('sporty', 0) * 0.5, 1)
            },
            'styleConfidenceScore': round(confidence_score['score'], 0),
            'colorPalette': {
                'favoriteColor': favorite_color,
                'topColors': top_colors_with_percentage,
                'colorDistribution': [
                    {'color': color, 'count': count, 'percentage': round(count/total_wears*100, 1) if total_wears > 0 else 0}
                    for color, count in color_counts.most_common(10)
                ]
            },
            'wearPreference': style_breakdown['breakdown'],
            'categoryBreakdown': category_breakdown,
            'mostWornTypes': [
                {'type': typ, 'count': count}
                for typ, count in type_counts.most_common(10)
            ],
            'combinationPatterns': combination_patterns,
            'styleConfidence': confidence_score,
            'insights': insights,
            'futurePrediction': future_prediction,
            'analyzedAt': datetime.now().isoformat()
        }
    
    def _calculate_style_breakdown(self, event_counts, total_wears):
        """
        Map events to style categories
        """
        # Map events to style categories
        style_mapping = {
            'casual': ['Casual Outing', 'Family Gathering', 'Shopping'],
            'formal': ['Office Meeting', 'Wedding', 'Date Night'],
            'sporty': ['Gym', 'Sports Event'],
            'party': ['Party', 'Date Night', 'Wedding']
        }
        
        style_counts = defaultdict(int)
        
        for event, count in event_counts.items():
            for style, events in style_mapping.items():
                if event in events:
                    style_counts[style] += count
        
        # Calculate percentages
        breakdown = {}
        if total_wears > 0:
            for style, count in style_counts.items():
                breakdown[style] = round((count / total_wears) * 100, 1)
        
        # Determine dominant style
        dominant = max(style_counts.items(), key=lambda x: x[1])[0] if style_counts else 'casual'
        
        # Add secondary style
        if len(style_counts) > 1:
            secondary = sorted(style_counts.items(), key=lambda x: x[1], reverse=True)[1][0]
            dominant_label = f"{dominant}-{secondary}"
        else:
            dominant_label = dominant
        
        return {
            'dominant': dominant_label,
            'breakdown': breakdown
        }
    
    def _analyze_combination_patterns(self, items):
        """
        Analyze which items are worn together frequently
        """
        # Group wears by date to find what was worn together
        date_outfits = defaultdict(list)
        
        for item in items:
            history = json.loads(item['wear_history']) if item['wear_history'] else []
            for wear in history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    date = wear.get('date', '')
                elif isinstance(wear, str):
                    date = wear
                else:
                    continue
                    
                if date:
                    date_outfits[date].append({
                        'id': item['id'],
                        'type': item['clothing_type'],
                        'color': item['primary_color']
                    })
        
        # Find frequent combinations
        combination_counts = Counter()
        for date, outfit in date_outfits.items():
            if len(outfit) >= 2:
                # Create combinations
                types = tuple(sorted([item['type'] for item in outfit]))
                combination_counts[types] += 1
        
        frequent_combinations = [
            {'combination': list(combo), 'frequency': count}
            for combo, count in combination_counts.most_common(10)
        ]
        
        return {
            'frequentCombinations': frequent_combinations,
            'totalUniqueCombinations': len(combination_counts),
            'averageItemsPerOutfit': round(
                sum(len(outfit) for outfit in date_outfits.values()) / len(date_outfits), 1
            ) if date_outfits else 0
        }
    
    def _calculate_style_confidence(self, items, event_counts, color_counts):
        """
        Calculate style confidence score
        - Adventure score: variety in choices
        - Consistency score: repeated patterns
        - Overall confidence: 0-100
        """
        if not items:
            return {'score': 0, 'rating': 'Not enough data'}
        
        # Color diversity
        unique_colors = len(color_counts)
        total_wears = sum(color_counts.values())
        color_diversity = min(100, (unique_colors / max(1, total_wears)) * 100)
        
        # Event diversity
        unique_events = len(event_counts)
        event_diversity = min(100, unique_events * 15)  # Max ~7 events
        
        # Adventurousness: Do they try new combinations?
        worn_items = [item for item in items if item['wear_count'] > 0]
        repeat_wear_ratio = sum(1 for item in worn_items if item['wear_count'] > 5) / max(1, len(worn_items))
        adventurousness = (1 - repeat_wear_ratio) * 100
        
        # Overall confidence
        confidence_score = (color_diversity * 0.3 + event_diversity * 0.3 + adventurousness * 0.4)
        
        # Rating
        if confidence_score >= 80:
            rating = 'Very Adventurous'
        elif confidence_score >= 60:
            rating = 'Confident & Adventurous'
        elif confidence_score >= 40:
            rating = 'Balanced Classic'
        elif confidence_score >= 20:
            rating = 'Traditional & Safe'
        else:
            rating = 'Very Conservative'
        
        return {
            'score': round(confidence_score, 1),
            'rating': rating,
            'colorDiversity': round(color_diversity, 1),
            'eventDiversity': round(event_diversity, 1),
            'adventurousness': round(adventurousness, 1),
            'interpretation': self._interpret_confidence(confidence_score)
        }
    
    def _interpret_confidence(self, score):
        """Provide interpretation of confidence score"""
        if score >= 80:
            return "You love experimenting with colors and styles! Very confident in fashion choices."
        elif score >= 60:
            return "You balance classic pieces with adventurous choices. Confident dresser."
        elif score >= 40:
            return "You prefer tried-and-true combinations. Classic and reliable style."
        elif score >= 20:
            return "You stick to what you know works. Traditional and safe."
        else:
            return "Very conservative style - might benefit from trying new combinations."
    
    def _generate_style_insights(self, event_counts, color_counts, type_counts, confidence_score):
        """Generate actionable style insights"""
        insights = []
        
        # Most worn event
        if event_counts:
            top_event = event_counts.most_common(1)[0]
            insights.append(f"You dress for {top_event[0]} most often ({top_event[1]} times)")
        
        # Color preference
        if color_counts:
            top_color = color_counts.most_common(1)[0]
            insights.append(f"{top_color[0].capitalize()} is your go-to color")
        
        # Style confidence
        if confidence_score['score'] >= 60:
            insights.append("You have a confident and varied style")
        else:
            insights.append("Consider experimenting with new styles and colors")
        
        # Most worn type
        if type_counts:
            top_type = type_counts.most_common(1)[0]
            insights.append(f"{top_type[0]} items are your wardrobe staples")
        
        return insights
    
    def _predict_style_evolution(self, items):
        """
        Use LSTM model to predict future style trends
        """
        if not self.model_service:
            return {'available': False, 'message': 'ML models not loaded'}
        
        # Get wear history timeline
        all_events = []
        for item in items:
            history = json.loads(item['wear_history']) if item['wear_history'] else []
            for wear in history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    date_str = wear.get('date', '')
                    occasion = wear.get('occasion', 'Unknown')
                elif isinstance(wear, str):
                    date_str = wear
                    occasion = 'Unknown'
                else:
                    continue
                    
                all_events.append({
                    'date': date_str,
                    'occasion': occasion,
                    'type': item['clothing_type']
                })
        
        # Sort by date
        all_events.sort(key=lambda x: x['date'])
        
        # Get event sequence for prediction
        event_names = [event['occasion'] for event in all_events[-20:]]  # Last 20 events
        
        if len(event_names) >= 5:
            try:
                # Use the wardrobe model service to predict next event
                # This uses the trained LSTM/GRU
                event_sequence = self._encode_events_for_lstm(event_names)
                prediction = self.model_service.predict_next_event(event_sequence, use_gru=True)
                
                return {
                    'available': True,
                    'nextLikelyEvent': prediction['predicted_event'],
                    'confidence': max(prediction['scores'].values()),
                    'allPredictions': prediction['scores'],
                    'modelUsed': prediction['model_used'],
                    'interpretation': f"Based on your recent patterns, you're likely to attend a {prediction['predicted_event']} next"
                }
            except Exception as e:
                self.logger.error(f"Error in LSTM prediction: {e}")
                return {'available': False, 'error': str(e)}
        
        return {'available': False, 'message': 'Not enough wear history for prediction'}
    
    def _encode_events_for_lstm(self, event_names):
        """
        Encode event names to numeric values for LSTM
        Simple encoding: map event names to integers
        """
        event_mapping = {
            'Casual Outing': 0,
            'Office Meeting': 1,
            'Gym': 2,
            'Date Night': 3,
            'Wedding': 4,
            'Party': 5,
            'Family Gathering': 6,
            'Funeral': 7,
            'Shopping': 8,
            'Unknown': 9
        }
        
        encoded = [event_mapping.get(event, 9) for event in event_names]
        return encoded
    
    def get_color_palette_analysis(self):
        """
        Detailed color palette analysis
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT primary_color, all_colors, wear_count
            FROM wardrobe_items
            WHERE primary_color IS NOT NULL
        ''')
        items = cursor.fetchall()
        conn.close()
        
        # Primary colors worn
        primary_colors = Counter()
        all_colors_list = []
        
        for item in items:
            if item['primary_color']:
                primary_colors[item['primary_color']] += item['wear_count']
            
            if item['all_colors']:
                try:
                    colors = json.loads(item['all_colors'])
                    # Handle both list of strings and list of dicts
                    if colors:
                        for color in colors:
                            if isinstance(color, str):
                                all_colors_list.extend([color] * item['wear_count'])
                            elif isinstance(color, dict) and 'color' in color:
                                all_colors_list.extend([color['color']] * item['wear_count'])
                except Exception as e:
                    self.logger.debug(f"Error parsing colors: {e}")
        
        all_colors_counter = Counter(all_colors_list)
        
        return {
            'topPrimaryColors': [
                {'color': color, 'wearCount': count}
                for color, count in primary_colors.most_common(10)
            ],
            'allColorsUsed': [
                {'color': color, 'count': count}
                for color, count in all_colors_counter.most_common(15)
            ],
            'colorDiversity': len(primary_colors),
            'mostWornColor': primary_colors.most_common(1)[0][0] if primary_colors else None,
            'colorPersonality': self._determine_color_personality(primary_colors)
        }
    
    def _determine_color_personality(self, color_counts):
        """
        Determine style personality based on color preferences
        """
        if not color_counts:
            return 'Not enough data'
        
        top_colors = [color for color, _ in color_counts.most_common(5)]
        
        # Neutral palette
        neutrals = {'black', 'white', 'gray', 'beige', 'brown', 'navy'}
        neutral_count = sum(1 for color in top_colors if color.lower() in neutrals)
        
        # Bright colors
        brights = {'red', 'yellow', 'orange', 'pink', 'bright'}
        bright_count = sum(1 for color in top_colors if any(b in color.lower() for b in brights))
        
        # Cool colors
        cools = {'blue', 'green', 'purple', 'teal'}
        cool_count = sum(1 for color in top_colors if any(c in color.lower() for c in cools))
        
        if neutral_count >= 4:
            return 'Minimalist - You prefer neutral, versatile colors'
        elif bright_count >= 3:
            return 'Bold & Vibrant - You love standing out with bright colors'
        elif cool_count >= 3:
            return 'Cool & Calm - You prefer cool, soothing tones'
        else:
            return 'Eclectic - You enjoy a diverse color palette'
    
    def get_outfit_combination_intelligence(self):
        """
        Advanced analysis of outfit combinations
        Uses LSTM to predict likely next combinations
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, clothing_type, wear_history, primary_color
            FROM wardrobe_items
            WHERE wear_history != "[]"
        ''')
        items = cursor.fetchall()
        conn.close()
        
        # Build date-based outfit tracking
        outfits_by_date = defaultdict(list)
        
        for item in items:
            history = json.loads(item['wear_history']) if item['wear_history'] else []
            for wear in history:
                # Handle both dict and string formats
                if isinstance(wear, dict):
                    date = wear.get('date', '')
                    occasion = wear.get('occasion', 'Unknown')
                elif isinstance(wear, str):
                    date = wear
                    occasion = 'Unknown'
                else:
                    continue
                    
                if date:
                    outfits_by_date[date].append({
                        'id': item['id'],
                        'type': item['clothing_type'],
                        'color': item['primary_color'],
                        'occasion': occasion
                    })
        
        # Find repeated combinations
        combination_frequency = Counter()
        type_pairing_frequency = Counter()
        
        for date, outfit_items in outfits_by_date.items():
            if len(outfit_items) >= 2:
                # Track type combinations
                types = tuple(sorted([item['type'] for item in outfit_items]))
                combination_frequency[types] += 1
                
                # Track specific pairings
                for i, item1 in enumerate(outfit_items):
                    for item2 in outfit_items[i+1:]:
                        pair = tuple(sorted([item1['id'], item2['id']]))
                        type_pairing_frequency[pair] += 1
        
        # Most repeated outfit patterns
        top_combinations = [
            {'types': list(combo), 'frequency': count}
            for combo, count in combination_frequency.most_common(10)
        ]
        
        return {
            'totalOutfits': len(outfits_by_date),
            'topCombinations': top_combinations,
            'averageItemsPerOutfit': round(
                sum(len(outfit) for outfit in outfits_by_date.values()) / len(outfits_by_date), 1
            ) if outfits_by_date else 0,
            'uniqueCombinations': len(combination_frequency),
            'mostRepeatedPattern': top_combinations[0] if top_combinations else None
        }
    
    def _calculate_style_confidence(self, items, event_counts, color_counts):
        """
        Calculate overall style confidence score
        """
        if not items:
            return {'score': 0, 'level': 'insufficient_data'}
        
        # Variety metrics
        unique_events = len(event_counts)
        unique_colors = len(color_counts)
        unique_types = len(set(item['clothing_type'] for item in items if item['clothing_type']))
        
        # Wear distribution (how evenly items are worn)
        wear_counts = [item['wear_count'] for item in items if item['wear_count'] > 0]
        if wear_counts:
            wear_variance = np.var(wear_counts)
            wear_evenness = 100 - min(100, wear_variance)
        else:
            wear_evenness = 0
        
        # Calculate confidence components
        event_diversity = min(100, unique_events * 15)
        color_diversity = min(100, unique_colors * 10)
        type_diversity = min(100, unique_types * 12)
        
        # Overall score
        confidence_score = (
            event_diversity * 0.35 +
            color_diversity * 0.30 +
            type_diversity * 0.20 +
            wear_evenness * 0.15
        )
        
        # Determine level
        if confidence_score >= 75:
            level = 'very_confident'
            description = 'Fashion Forward - You experiment boldly!'
        elif confidence_score >= 60:
            level = 'confident'
            description = 'Confident Dresser - Good variety and style'
        elif confidence_score >= 40:
            level = 'moderate'
            description = 'Building Confidence - Explore more!'
        else:
            level = 'developing'
            description = 'Style Journey Beginning - Keep experimenting!'
        
        return {
            'score': round(confidence_score, 1),
            'level': level,
            'description': description,
            'components': {
                'eventDiversity': round(event_diversity, 1),
                'colorDiversity': round(color_diversity, 1),
                'typeDiversity': round(type_diversity, 1),
                'wearEvenness': round(wear_evenness, 1)
            }
        }
    
    def _empty_profile(self):
        """Return empty profile when no data available"""
        return {
            'dominantStyle': 'unknown',
            'styleBreakdown': {},
            'colorPalette': {'topColors': [], 'colorDistribution': []},
            'wearPreference': {},
            'mostWornTypes': [],
            'combinationPatterns': {'frequentCombinations': [], 'totalUniqueCombinations': 0},
            'styleConfidence': {'score': 0, 'level': 'insufficient_data'},
            'futurePrediction': {'available': False},
            'totalWears': 0
        }
    
    def get_style_evolution_timeline(self, months=6):
        """
        Track style evolution over time
        Shows how style preferences changed month by month
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT wear_history, best_event, primary_color, clothing_type
            FROM wardrobe_items
            WHERE wear_history != "[]"
        ''')
        items = cursor.fetchall()
        conn.close()
        
        # Group by month
        monthly_data = defaultdict(lambda: {
            'events': Counter(),
            'colors': Counter(),
            'types': Counter(),
            'totalWears': 0
        })
        
        for item in items:
            history = json.loads(item['wear_history']) if item['wear_history'] else []
            for wear in history:
                try:
                    # Handle both dict and string formats
                    if isinstance(wear, dict):
                        date_str = wear.get('date', '')
                    elif isinstance(wear, str):
                        date_str = wear
                    else:
                        continue
                    
                    date = datetime.fromisoformat(date_str)
                    month_key = date.strftime('%Y-%m')
                    
                    monthly_data[month_key]['totalWears'] += 1
                    if item['best_event']:
                        monthly_data[month_key]['events'][item['best_event']] += 1
                    if item['primary_color']:
                        monthly_data[month_key]['colors'][item['primary_color']] += 1
                    if item['clothing_type']:
                        monthly_data[month_key]['types'][item['clothing_type']] += 1
                except:
                    continue
        
        # Get recent months
        sorted_months = sorted(monthly_data.keys(), reverse=True)[:months]
        sorted_months.reverse()
        
        timeline = []
        for month in sorted_months:
            data = monthly_data[month]
            timeline.append({
                'month': month,
                'totalWears': data['totalWears'],
                'topEvent': data['events'].most_common(1)[0][0] if data['events'] else None,
                'topColor': data['colors'].most_common(1)[0][0] if data['colors'] else None,
                'topType': data['types'].most_common(1)[0][0] if data['types'] else None
            })
        
        return {
            'timeline': timeline,
            'monthsAnalyzed': len(timeline)
        }


# Singleton instance
style_analyzer = StyleProfileAnalyzer()
