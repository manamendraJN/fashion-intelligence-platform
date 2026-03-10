"""
routes/wardrobe_routes.py
All wardrobe AI endpoints.

THRESHOLD: 0.60
  Items scoring below 0.60 for a requested occasion are NEVER shown.
  This is critical — it's what keeps blazers out of Family Gathering,
  T-shirts out of Office, etc.

FUNERAL COLOUR FILTER:
  After the score filter, Funeral recommendations are additionally
  filtered to keep only dark/neutral coloured items.
"""

from flask import Blueprint, request, jsonify, send_from_directory
import logging
import io
import os
import json
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
from pathlib import Path
import time

import sys
sys.path.append(str(Path(__file__).parent.parent))
import database

from core.event_constants import normalize_event_name, find_event_score, get_default_event_scores
from utils.color_utils import get_complementary_items, are_colors_compatible

logger = logging.getLogger(__name__)

wardrobe_bp = Blueprint('wardrobe', __name__)
_wardrobe_service = None

UPLOAD_FOLDER = Path(__file__).parent.parent / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def init_wardrobe_routes(wardrobe_service):
    global _wardrobe_service
    _wardrobe_service = wardrobe_service


# ─────────────────────────── Threshold ───────────────────────────────
# Items below this score for the requested occasion are NEVER recommended.
RECOMMEND_THRESHOLD = 0.60


# ─────────────────────────── Weather Boost ───────────────────────────
WEATHER_BOOST = {
    "hot": {
        "boost":    ["Tank Top", "Shorts", "Sundress", "Mini Skirt", "Crop Top",
                     "Swimwear", "Denim Shorts", "Casual Dress", "T-Shirts", "T-Shirt",
                     "Sleeveless"],
        "penalise": ["Puffer Jacket", "Sweaters", "Hoodies", "Formal Coat",
                     "Leather Jacket", "Cardigan", "Sweatshirt"],
    },
    "cold": {
        "boost":    ["Sweaters", "Hoodies", "Cardigan", "Puffer Jacket", "Blazers",
                     "Jackets", "Leather Jacket", "Formal Coat"],
        "penalise": ["Shorts", "Denim Shorts", "Tank Top", "Crop Top", "Swimwear", "Sundress"],
    },
    "rainy": {
        "boost":    ["Jackets", "Puffer Jacket", "Blazers", "Sweaters", "Hoodies",
                     "Formal Coat", "Leggings", "Trousers"],
        "penalise": ["Shorts", "Denim Shorts", "Sundress", "Swimwear", "Tank Top"],
    },
}

def apply_weather_adjustment(item, weather):
    if not weather:
        return item
    rules = WEATHER_BOOST.get(weather.lower())
    if not rules:
        return item
    item_type = item.get("type", "")
    score = item.get("recommendationScore", 0)
    if any(bt.lower() in item_type.lower() for bt in rules["boost"]):
        score = min(1.0, score + 0.10)
    elif any(pt.lower() in item_type.lower() for pt in rules["penalise"]):
        score = max(0.0, score - 0.35)  # Increased penalty to filter out inappropriate items
    item["recommendationScore"] = score
    item["suitabilityScore"]    = score
    return item


# ─────────────────────────── Funeral Colour Filter ───────────────────
# For funerals we ONLY show dark / neutral coloured items.
FUNERAL_OK_COLORS = {
    "black", "dark gray", "gray", "charcoal", "navy", "dark blue",
    "dark navy", "dark grey", "charcoal gray", "white", "cream",
    "off white", "light gray", "light grey", "dark purple", "burgundy",
    "dark red", "dark brown", "dark green",
}

def is_funeral_appropriate(item):
    """Returns True if item colour is suitable for a funeral."""
    color = (item.get("primaryColor") or "").lower().strip()
    if not color or color == "unknown":
        return True   # if we don't know the colour, include it
    return any(fc in color for fc in FUNERAL_OK_COLORS)


# ─────────────────────────── Serve uploads ───────────────────────────
@wardrobe_bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ─────────────────────────── Wardrobe CRUD ───────────────────────────
@wardrobe_bp.route('/api/wardrobe', methods=['GET'])
def get_all_items():
    try:
        items = database.get_all_wardrobe_items()
        return jsonify(items), 200
    except Exception as e:
        logger.error(f"Error fetching wardrobe: {e}", exc_info=True)
        return jsonify({"error": str(e), "items": []}), 500


@wardrobe_bp.route('/api/predict/clothing-type', methods=['POST'])
def predict_and_save_clothing():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    try:
        filename        = secure_filename(file.filename)
        unique_filename = f"{int(time.time() * 1000)}_{filename}"
        filepath        = UPLOAD_FOLDER / unique_filename
        file.save(filepath)
        img = Image.open(filepath)

        if _wardrobe_service:
            result        = _wardrobe_service.full_analysis(img, None)
            clothing_type = result["clothing_type"]
            confidence    = result["confidence"]
            top_5         = result["top_5"]
            event_scores  = result["event_scores"]
            best_event    = result["best_event"]
            primary_color = result.get("primary_color", "Unknown")
            color_rgb     = result.get("color_rgb", [0, 0, 0])
            all_colors    = result.get("all_colors", [])
        else:
            clothing_type = "Unknown"
            confidence    = 0.0
            top_5         = []
            event_scores  = get_default_event_scores("Unknown")
            best_event    = "Casual"
            primary_color = "Unknown"
            color_rgb     = [0, 0, 0]
            all_colors    = []

        image_path = f"/uploads/{unique_filename}"
        item_id = database.add_wardrobe_item(
            filename=filename, image_path=image_path,
            clothing_type=clothing_type, confidence=confidence, top_5=top_5,
            event_scores=event_scores, best_event=best_event,
            primary_color=primary_color, color_rgb=color_rgb, all_colors=all_colors
        )
        return jsonify({
            "success": True, "id": item_id, "filename": filename,
            "url": image_path, "type": clothing_type, "confidence": confidence,
            "primaryColor": primary_color, "colorRgb": color_rgb,
            "allColors": all_colors, "top5": top_5,
            "eventScores": event_scores, "bestEvent": best_event
        }), 200
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/<int:item_id>/favorite', methods=['POST'])
def toggle_favorite_item(item_id):
    try:
        return jsonify({"success": True, "isFavorite": database.toggle_favorite(item_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/<int:item_id>/dislike', methods=['POST'])
def toggle_dislike_item(item_id):
    try:
        return jsonify({"success": True, "isDisliked": database.toggle_dislike(item_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/<int:item_id>/mark-worn', methods=['POST'])
def mark_worn_item(item_id):
    try:
        data    = request.get_json() or {}
        success = database.mark_item_worn(item_id, data.get('occasion', 'General'), data.get('date'))
        return (jsonify({"success": True}) if success
                else jsonify({"error": "Item not found"})), (200 if success else 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/<int:item_id>/update-type', methods=['POST'])
def update_item_clothing_type(item_id):
    try:
        data     = request.get_json()
        new_type = data.get('type')
        if not new_type:
            return jsonify({"error": "Type is required"}), 400
        event_scores = get_default_event_scores(new_type)
        database.update_item_type(item_id, new_type, event_scores)
        return jsonify({"success": True, "type": new_type, "eventScores": event_scores}), 200
    except Exception as e:
        logger.error(f"Update type error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/<int:item_id>', methods=['DELETE'])
def delete_wardrobe_item(item_id):
    try:
        item = database.get_wardrobe_item(item_id)
        if item:
            database.delete_item(item_id)
            img_path = UPLOAD_FOLDER / item['url'].replace('/uploads/', '')
            if img_path.exists():
                img_path.unlink()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/recalculate-all', methods=['POST'])
def recalculate_all_event_scores():
    """
    RE-SCORES every item in the database with the latest event_constants rules.
    MUST be called after deploying updated event_constants.py so that existing
    items get corrected scores.  Without this, old items keep their stale scores.
    """
    try:
        all_items     = database.get_all_wardrobe_items()
        updated_count = 0
        for item in all_items:
            new_scores = get_default_event_scores(item.get('type', 'Unknown'))
            database.update_item_type(item['id'], item.get('type', 'Unknown'), new_scores)
            updated_count += 1
        logger.info(f"Recalculated scores for {updated_count} items")
        return jsonify({"success": True, "updated_count": updated_count}), 200
    except Exception as e:
        logger.error(f"Recalculate all error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics', methods=['GET'])
def get_analytics():
    try:
        analytics = database.get_analytics()
        return jsonify({
            "stats": {
                "totalItems":    analytics['totalItems'],
                "unwornItems":   analytics['unwornItems'],
                "avgWearCount":  analytics['avgWearCount'],
                "eventsCovered": 5, "totalEvents": 7
            },
            "notifications": [],
            "charts": {
                "composition": [
                    {"name": i['name'], "value": i['value'], "fill": "#8B5A5A"}
                    for i in analytics['composition']
                ]
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Smart Recommendations ───────────────────
@wardrobe_bp.route('/api/recommend-smart', methods=['POST'])
def recommend_smart():
    """
    Core recommendation engine.

    Steps:
    1. Normalise occasion name
    2. Filter by score >= RECOMMEND_THRESHOLD (0.60)
    3. For Funeral: additionally filter by colour (dark/neutral only)
    4. Apply wear-history penalty and recency penalty
    5. Apply weather boost/penalise
    6. Return top 8 sorted by final score

    IMPORTANT: The threshold (0.60) is what prevents blazers showing for
    Family Gathering, T-shirts for Office Meeting, etc.
    """
    try:
        from datetime import datetime

        data         = request.get_json() or {}
        raw_occasion = data.get('occasion', 'Casual')
        weather      = data.get('weather')

        occasion = normalize_event_name(raw_occasion)
        logger.info(f"[recommend-smart] '{raw_occasion}' → '{occasion}' | weather={weather}")

        all_items       = database.get_all_wardrobe_items()
        recommendations = []
        skipped_recent  = []

        for item in all_items:
            # Skip disliked items
            if item.get('isDisliked'):
                continue

            event_scores = item.get('eventScores', {})
            score        = find_event_score(event_scores, occasion)

            # ── SCORE GATE ──────────────────────────────────────────────
            # This is the key filter.  Items with score < 0.60 are NEVER shown.
            if score < RECOMMEND_THRESHOLD:
                continue

            # ── FUNERAL COLOUR GATE ─────────────────────────────────────
            if occasion == "Funeral" and not is_funeral_appropriate(item):
                continue

            # ── RECENCY PENALTY ─────────────────────────────────────────
            last_worn       = item.get('lastWorn')
            is_recent       = False
            days_since_worn = 0

            if last_worn:
                try:
                    lw_str = last_worn.replace('Z', '+00:00') if isinstance(last_worn, str) else ''
                    try:
                        lw_date = datetime.fromisoformat(lw_str)
                    except Exception:
                        lw_date = datetime.fromisoformat(last_worn.split('T')[0])
                    if lw_date.tzinfo:
                        lw_date = lw_date.replace(tzinfo=None)
                    days_since_worn = (datetime.now() - lw_date).days
                    is_recent       = days_since_worn < 7
                except Exception as ex:
                    logger.warning(f"Could not parse lastWorn for item {item.get('id')}: {ex}")

            wear_count      = item.get('wearCount', 0)
            wear_penalty    = wear_count * 0.04
            recency_penalty = 0.25 if is_recent else 0.0
            final_score     = max(0, score - wear_penalty - recency_penalty)

            # ── REASON TEXT ─────────────────────────────────────────────
            if wear_count == 0:
                reason = "Never worn — perfect to try!"
            elif is_recent:
                reason = f"Worn recently ({days_since_worn}d ago)"
            elif wear_count < 3:
                reason = "Lightly worn, great choice"
            else:
                reason = f"Worn {wear_count}× — a reliable pick"

            item_copy = {
                **item,
                "recommendationScore": final_score,
                "suitabilityScore":    final_score,
                "reason":              reason,
            }
            item_copy = apply_weather_adjustment(item_copy, weather)
            recommendations.append(item_copy)

            if is_recent:
                skipped_recent.append(item)

        # Sort best first
        recommendations.sort(key=lambda x: x.get("recommendationScore", 0), reverse=True)
        top_recommendations = recommendations[:8]

        if not top_recommendations:
            message = (
                f"No items found for {occasion}. "
                "Try uploading more clothes or tap 'Recalculate All Scores' in Settings "
                "to refresh your wardrobe data."
            )
        else:
            message = f"Found {len(top_recommendations)} items suitable for {occasion}"
            if skipped_recent:
                message += f" · skipped {len(skipped_recent)} recently worn"

        return jsonify({
            "success":         True,
            "recommendations": top_recommendations,
            "recentlyWorn":    [{"id": i["id"], "type": i.get("type")} for i in skipped_recent],
            "message":         message,
        }), 200

    except Exception as e:
        logger.error(f"Smart recommendation error: {e}", exc_info=True)
        return jsonify({"error": str(e), "success": False}), 500


# ─────────────────────────── Outfit Pairing ──────────────────────────
@wardrobe_bp.route('/api/outfit-pairing/<int:item_id>', methods=['GET'])
def get_outfit_pairing(item_id):
    try:
        from utils.color_utils import get_event_based_pairing, is_same_category

        item = database.get_wardrobe_item(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        item_type  = item.get('type', 'Unknown')
        item_color = item.get('primaryColor', 'Unknown')
        event_type = request.args.get('event_type') or "casual"
        weather    = request.args.get('weather')  # Add weather parameter

        recommendations  = get_event_based_pairing(item_type, item_color, event_type)
        matching_types   = recommendations['matching_types']
        matching_colors  = recommendations['matching_colors']
        avoid_types      = recommendations.get('avoid_types', [])
        pairing_note     = recommendations.get('pairing_note', '')
        pairing_category = recommendations.get('pairing_category', '')

        matches     = database.get_matching_items(item_id, matching_types, matching_colors)
        avoid_lower = [a.lower() for a in avoid_types]
        
        # Filter out items in avoid_types AND same category (tops with tops, etc.)
        matches     = [
            m for m in matches
            if not any(
                a in m.get('type', '').lower() or m.get('type', '').lower() in a
                for a in avoid_lower
            )
            and not is_same_category(item_type, m.get('type', ''))
        ]
        
        # Apply weather-based filtering
        if weather:
            # Initialize base score for pairing items (they don't have recommendationScore from DB)
            for m in matches:
                if 'recommendationScore' not in m:
                    m['recommendationScore'] = 0.7  # Base pairing score
            
            matches = [apply_weather_adjustment(m, weather) for m in matches]
            # Remove items heavily penalized by weather (score dropped below threshold)
            matches = [m for m in matches if m.get('recommendationScore', 0.7) >= 0.4]

        matching_types_lower  = [t.lower() for t in matching_types]
        matching_colors_lower = [c.lower() for c in matching_colors]
        enhanced_matches      = []

        for match in matches:
            match_type  = match.get('type', '')
            match_color = (match.get('primaryColor') or 'Unknown').lower()

            compatibility_score = 0
            reasons = []

            type_matched = any(
                t in match_type.lower() or match_type.lower() in t
                for t in matching_types_lower
            )
            if type_matched:
                compatibility_score += 80
                reasons.append(f"{match_type} pairs with {item_type}")

            color_ok = (
                match_color in matching_colors_lower
                or are_colors_compatible(item_color, match.get('primaryColor', 'Unknown'))
            )
            if color_ok:
                compatibility_score += 20
                reasons.append(f"{match.get('primaryColor', '?')} matches {item_color}")

            if compatibility_score > 0:
                match['matchScore']         = compatibility_score
                match['compatibilityScore'] = compatibility_score
                match['reasons']            = reasons
                enhanced_matches.append(match)

        enhanced_matches.sort(key=lambda x: x['matchScore'], reverse=True)

        message = f"Found {len(enhanced_matches)} items that pair well with your {item_color} {item_type}"
        if event_type and event_type != "casual":
            message += f" for {event_type}"
        if weather:
            weather_desc = {"hot": "hot weather", "cold": "cold weather", "rainy": "rainy weather"}
            message += f" in {weather_desc.get(weather.lower(), weather)}"

        return jsonify({
            "success":         True,
            "item":            {"id": item["id"], "type": item_type, "color": item_color, "url": item["url"]},
            "matches":         enhanced_matches[:10],
            "matchingTypes":   matching_types,
            "matchingColors":  matching_colors,
            "avoidTypes":      avoid_types,
            "pairingNote":     pairing_note,
            "pairingCategory": pairing_category,
            "eventType":       event_type,
            "weather":         weather,
            "message":         message,
        }), 200

    except Exception as e:
        logger.error(f"Pairing error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Health / Misc ───────────────────────────
@wardrobe_bp.route('/api/wardrobe/health', methods=['GET'])
def wardrobe_health():
    loaded = _wardrobe_service is not None and _wardrobe_service._loaded
    return jsonify({
        "status": "ready" if loaded else "not_loaded",
        "models": ["CNN", "EventModel", "GRU", "LSTM"] if loaded else [],
    }), 200 if loaded else 503


@wardrobe_bp.route('/api/wardrobe/classify', methods=['POST'])
def classify_clothing():
    if 'image' not in request.files:
        return jsonify({"error": "No image file. Use key 'image'"}), 400
    try:
        img    = Image.open(io.BytesIO(request.files['image'].read()))
        result = _wardrobe_service.predict_clothing(img)
        return jsonify({"success": True, "clothing_type": result["clothing_type"],
                        "confidence": result["confidence"], "all_scores": result["all_scores"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/event-scores', methods=['POST'])
def get_event_scores():
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
    metadata = {k: request.form.get(k, d) for k, d in
                [('article', 'Tops'), ('color', 'Black'), ('usage', 'Casual'), ('gender', 'Women')]}
    try:
        img    = Image.open(io.BytesIO(request.files['image'].read()))
        result = _wardrobe_service.predict_event_scores(img, metadata)
        return jsonify({"success": True, "best_event": result["best_event"], "scores": result["scores"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/analyze', methods=['POST'])
def analyze_clothing():
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400
    metadata = {k: request.form.get(k, d) for k, d in
                [('color', 'Black'), ('usage', 'Casual'), ('gender', 'Women')]}
    try:
        img    = Image.open(io.BytesIO(request.files['image'].read()))
        result = _wardrobe_service.full_analysis(img, metadata or None)
        return jsonify({
            "success": True, "clothing_type": result["clothing_type"],
            "confidence": result["confidence"], "top_5": result["top_5"],
            "best_event": result["best_event"], "event_scores": result["event_scores"],
            "metadata_used": result["metadata_used"],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/recommend-event', methods=['POST'])
def recommend_event():
    data = request.get_json()
    if not data or 'wear_history' not in data:
        return jsonify({"error": "Provide 'wear_history' list in JSON body"}), 400
    try:
        result = _wardrobe_service.predict_next_event(data['wear_history'], data.get('use_gru', True))
        return jsonify({"success": True, "predicted_event": result["predicted_event"],
                        "scores": result["scores"], "model_used": result["model_used"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/user-profile', methods=['GET'])
def get_user_profile():
    try:
        profile   = database.get_user_profile()
        analytics = database.get_analytics()
        if profile:
            return jsonify({
                "success": True,
                "profile": {
                    **profile,
                    "favoriteCount":    analytics.get('favoriteCount', 0),
                    "stylePersonality": "Developing" if profile['totalInteractions'] < 10 else "Established",
                }
            }), 200
        return jsonify({"error": "Profile not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Advanced Analytics Routes ───────────────────
@wardrobe_bp.route('/api/analytics/advanced', methods=['GET'])
def get_advanced_analytics():
    """
    Get comprehensive analytics dashboard
    Includes: mostWorn, leastWorn, eventFrequency, seasonDistribution, colorDistribution
    """
    try:
        from services.analytics_service import analytics_service
        
        # Get wear pattern insights
        patterns = analytics_service.get_wear_pattern_insights()
        
        # Get seasonal distribution
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT season, COUNT(*) as count
            FROM wardrobe_items
            WHERE season IS NOT NULL
            GROUP BY season
        ''')
        seasons = cursor.fetchall()
        
        # Get event frequency from wear history
        cursor.execute('''
            SELECT wear_history FROM wardrobe_items WHERE wear_history != "[]" AND wear_history IS NOT NULL
        ''')
        history_rows = cursor.fetchall()
        
        # Parse event frequency
        event_counts = {}
        for row in history_rows:
            try:
                history = json.loads(row['wear_history'])
                for wear in history:
                    occasion = wear.get('occasion', 'Unknown') if isinstance(wear, dict) else 'Unknown'
                    event_counts[occasion] = event_counts.get(occasion, 0) + 1
            except:
                continue
        
        # Get color distribution
        cursor.execute('''
            SELECT primary_color, COUNT(*) as count
            FROM wardrobe_items
            WHERE primary_color IS NOT NULL
            GROUP BY primary_color
            ORDER BY count DESC
        ''')
        colors = cursor.fetchall()
        conn.close()
        
        return jsonify({
            "mostWorn": patterns['mostWorn'],
            "leastWorn": patterns['leastWorn'],
            "eventFrequency": [{"event": k, "count": v} for k, v in sorted(event_counts.items(), key=lambda x: x[1], reverse=True)],
            "seasonDistribution": [{"season": s['season'], "count": s['count']} for s in seasons],
            "colorDistribution": [{"color": c['primary_color'], "count": c['count']} for c in colors]
        }), 200
    except Exception as e:
        logger.error(f"Error in advanced analytics: {e}")
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/wear-patterns', methods=['GET'])
def get_wear_patterns():
    """Get wear pattern insights"""
    try:
        from services.analytics_service import analytics_service
        
        patterns = analytics_service.get_wear_pattern_insights()
        return jsonify({
            "success": True,
            "patterns": patterns
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/cost-per-wear', methods=['GET'])
def get_cost_analysis():
    """Get cost per wear analysis"""
    try:
        from services.analytics_service import analytics_service
        
        analysis = analytics_service.get_cost_per_wear_analysis()
        return jsonify({
            "success": True,
            "costAnalysis": analysis
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/timeline', methods=['GET'])
def get_wear_timeline():
    """Get wear frequency timeline"""
    try:
        from services.analytics_service import analytics_service
        
        period = request.args.get('period', 'monthly')  # daily, weekly, monthly
        limit = int(request.args.get('limit', 12))
        
        timeline = analytics_service.get_wear_frequency_timeline(period=period, limit=limit)
        return jsonify({
            "success": True,
            "timeline": timeline
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/seasonal', methods=['GET'])
def get_seasonal_analysis():
    """Get seasonal wear analysis"""
    try:
        from services.analytics_service import analytics_service
        
        seasonal = analytics_service.get_seasonal_analysis()
        return jsonify({
            "success": True,
            "seasonal": seasonal
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/events', methods=['GET'])
def get_event_tracking():
    """Get event preference tracking"""
    try:
        from services.analytics_service import analytics_service
        
        events = analytics_service.get_event_preference_tracking()
        return jsonify({
            "success": True,
            "events": events
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/forgotten-items', methods=['GET'])
def get_forgotten_items():
    """Get forgotten items alert"""
    try:
        from services.analytics_service import analytics_service
        
        threshold = int(request.args.get('threshold', 90))
        forgotten = analytics_service.get_forgotten_items(days_threshold=threshold)
        
        return jsonify(forgotten), 200
    except Exception as e:
        logger.error(f"Error in forgotten items: {e}")
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/cost-efficiency', methods=['GET'])
def get_cost_efficiency():
    """Get cost per wear efficiency analysis"""
    try:
        from services.analytics_service import analytics_service
        
        analysis = analytics_service.get_cost_per_wear_analysis()
        return jsonify(analysis), 200
    except Exception as e:
        logger.error(f"Error in cost efficiency: {e}")
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/wear-timeline', methods=['GET'])
def get_wear_timeline_with_params():
    """Get wear frequency timeline with custom parameters"""
    try:
        from services.analytics_service import analytics_service
        
        days = int(request.args.get('days', 90))
        granularity = request.args.get('granularity', 'weekly')
        
        # Map granularity to period
        period_map = {'weekly': 'weekly', 'daily': 'daily', 'monthly': 'monthly'}
        period = period_map.get(granularity, 'weekly')
        
        # Calculate limit based on days and granularity
        if period == 'daily':
            limit = days
        elif period == 'weekly':
            limit = days // 7
        else:  # monthly
            limit = days // 30
        
        timeline = analytics_service.get_wear_frequency_timeline(period=period, limit=max(limit, 1))
        return jsonify(timeline), 200
    except Exception as e:
        logger.error(f"Error in wear timeline: {e}")
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/predictions', methods=['GET'])
def get_ai_predictions():
    """Get AI-powered predictions for next items to wear"""
    try:
        from services.wardrobe_model_service import WardrobeModelService
        from pathlib import Path
        import json
        
        # Get all items with wear history
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, filename, image_path, clothing_type, wear_count, 
                   wear_history, primary_color
            FROM wardrobe_items
            WHERE wear_history != "[]" AND wear_history IS NOT NULL
            ORDER BY wear_count DESC
        ''')
        items = cursor.fetchall()
        conn.close()
        
        if not items or len(items) < 3:
            return jsonify({
                "predictions": [],
                "message": "Not enough wear history for predictions"
            }), 200
        
        # Calculate prediction scores based on wear patterns
        predictions = []
        for item in items[:15]:  # Top 15 most worn items
            # Simple prediction score based on frequency
            score = min(100, (item['wear_count'] * 10))
            predictions.append({
                "item": {
                    "id": item['id'],
                    "filename": item['filename'],
                    "url": item['image_path'],
                    "type": item['clothing_type'],
                    "primaryColor": item['primary_color']
                },
                "score": score
            })
        
        # Sort by score
        predictions.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            "predictions": predictions,
            "model": "Frequency-based prediction",
            "generatedAt": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error in predictions: {e}")
        return jsonify({"predictions": [], "error": str(e)}), 500


@wardrobe_bp.route('/api/analytics/style-profile', methods=['GET'])
def get_analytics_style_profile():
    """Alias for /api/style/profile for frontend compatibility"""
    try:
        from services.style_analyzer import style_analyzer
        
        profile = style_analyzer.analyze_style_profile()
        return jsonify(profile), 200
    except Exception as e:
        logger.error(f"Error in style profile: {e}")
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Style Profile Routes ───────────────────
@wardrobe_bp.route('/api/style/profile', methods=['GET'])
def get_style_profile():
    """
    Get personal style profile with ML-powered insights
    Uses LSTM models to analyze and predict style preferences
    """
    try:
        from services.style_analyzer import style_analyzer
        
        profile = style_analyzer.analyze_style_profile()
        return jsonify({
            "success": True,
            "styleProfile": profile
        }), 200
    except Exception as e:
        logger.error(f"Error in style profile: {e}")
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/style/color-palette', methods=['GET'])
def get_color_palette():
    """Get detailed color palette analysis"""
    try:
        from services.style_analyzer import style_analyzer
        
        palette = style_analyzer.get_color_palette_analysis()
        return jsonify({
            "success": True,
            "colorPalette": palette
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/style/combinations', methods=['GET'])
def get_outfit_combinations():
    """Get outfit combination intelligence"""
    try:
        from services.style_analyzer import style_analyzer
        
        combinations = style_analyzer.get_outfit_combination_intelligence()
        return jsonify({
            "success": True,
            "combinations": combinations
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/style/evolution', methods=['GET'])
def get_style_evolution():
    """Get style evolution timeline"""
    try:
        from services.style_analyzer import style_analyzer
        
        months = int(request.args.get('months', 6))
        evolution = style_analyzer.get_style_evolution_timeline(months=months)
        
        return jsonify({
            "success": True,
            "evolution": evolution
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wardrobe_bp.route('/api/wardrobe/<int:item_id>/purchase-info', methods=['PUT'])
def update_purchase_info(item_id):
    """Update item purchase information"""
    try:
        data = request.get_json() or {}
        
        purchase_price = data.get('purchasePrice')
        purchase_date = data.get('purchaseDate')
        season = data.get('season')
        
        success = database.update_item_purchase_info(
            item_id, 
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            season=season
        )
        
        if success:
            return jsonify({
                "success": True,
                "message": "Purchase info updated"
            }), 200
        else:
            return jsonify({"error": "Item not found or no updates provided"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
