"""
routes/wardrobe_routes.py
All wardrobe AI endpoints — image upload, event scoring, recommendations.
"""

from flask import Blueprint, request, jsonify
import logging
import io
from PIL import Image

logger = logging.getLogger(__name__)

wardrobe_bp = Blueprint('wardrobe', __name__, url_prefix='/api/wardrobe')

# Will be injected from app.py
_wardrobe_service = None

def init_wardrobe_routes(wardrobe_service):
    global _wardrobe_service
    _wardrobe_service = wardrobe_service


# ─────────────────────────── Health ─────────────────────────────────

@wardrobe_bp.route('/health', methods=['GET'])
def wardrobe_health():
    """Check if wardrobe models are loaded."""
    loaded = _wardrobe_service is not None and _wardrobe_service._loaded
    return jsonify({
        "status":  "ready" if loaded else "not_loaded",
        "models":  ["CNN", "EventModel", "GRU", "LSTM"] if loaded else []
    }), 200 if loaded else 503


# ─────────────────────────── Clothing Detection ──────────────────────

@wardrobe_bp.route('/classify', methods=['POST'])
def classify_clothing():
    """
    POST /api/wardrobe/classify
    Body: multipart/form-data  →  image file
    Returns: clothing type + confidence
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided. Use key 'image'"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        result = _wardrobe_service.predict_clothing(img)

        return jsonify({
            "success":        True,
            "clothing_type":  result["clothing_type"],
            "confidence":     result["confidence"],
            "all_scores":     result["all_scores"]
        }), 200

    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Event Scoring ───────────────────────────

@wardrobe_bp.route('/event-scores', methods=['POST'])
def get_event_scores():
    """
    POST /api/wardrobe/event-scores
    Body: multipart/form-data
        - image: clothing image file
        - article (optional): e.g. "Sarees"
        - color   (optional): e.g. "Red"
        - usage   (optional): e.g. "Ethnic"
        - gender  (optional): e.g. "Women"
    Returns: event scores for all 12 event types
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    # Optional metadata from form fields
    metadata = {
        'article': request.form.get('article', 'Tops'),
        'color':   request.form.get('color',   'Black'),
        'usage':   request.form.get('usage',   'Casual'),
        'gender':  request.form.get('gender',  'Women'),
    }

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        result = _wardrobe_service.predict_event_scores(img, metadata)

        return jsonify({
            "success":    True,
            "best_event": result["best_event"],
            "scores":     result["scores"]
        }), 200

    except Exception as e:
        logger.error(f"Event scoring error: {e}")
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Full Analysis ───────────────────────────

@wardrobe_bp.route('/analyze', methods=['POST'])
def analyze_clothing():
    """
    POST /api/wardrobe/analyze
    Full pipeline: classify clothing → score events
    Body: multipart/form-data
        - image: clothing image
        - color, usage, gender (optional)
    Returns: clothing type + all event scores
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    metadata = {
        'color':  request.form.get('color',  'Black'),
        'usage':  request.form.get('usage',  'Casual'),
        'gender': request.form.get('gender', 'Women'),
    }

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        result = _wardrobe_service.full_analysis(img, metadata or None)

        return jsonify({
            "success":       True,
            "clothing_type": result["clothing"]["clothing_type"],
            "confidence":    result["clothing"]["confidence"],
            "best_event":    result["event_scores"]["best_event"],
            "event_scores":  result["event_scores"]["scores"],
            "metadata_used": result["metadata_used"]
        }), 200

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({"error": str(e)}), 500


# ─────────────────────────── Temporal Recommendation ─────────────────

@wardrobe_bp.route('/recommend-event', methods=['POST'])
def recommend_event():
    """
    POST /api/wardrobe/recommend-event
    Body: JSON  { "wear_history": [3, 7, 2, 15, ...], "use_gru": true }
    Returns: predicted best event based on wear history
    """
    data = request.get_json()
    if not data or 'wear_history' not in data:
        return jsonify({"error": "Provide 'wear_history' list in JSON body"}), 400

    wear_history = data.get('wear_history', [])
    use_gru      = data.get('use_gru', True)

    try:
        result = _wardrobe_service.predict_next_event(wear_history, use_gru)
        return jsonify({
            "success":          True,
            "predicted_event":  result["predicted_event"],
            "scores":           result["scores"],
            "model_used":       result["model_used"]
        }), 200

    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": str(e)}), 500