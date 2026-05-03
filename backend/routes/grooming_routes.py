"""
routes/grooming_routes.py
Grooming recommendation endpoints.

Wraps the skin-tone analysis (ONNX models) and Gemini Vision AI endpoints
for hair style, nail care, and dental hygiene recommendations.
"""

from flask import Blueprint, request, jsonify
import logging
import io
import os

logger = logging.getLogger(__name__)

grooming_bp = Blueprint('grooming', __name__)

# Services are initialised at startup via init_grooming_routes()
_grooming_service = None


def init_grooming_routes(grooming_service):
    """Inject the GroomingService instance (loaded at startup)."""
    global _grooming_service
    _grooming_service = grooming_service


@grooming_bp.route('/predict', methods=['POST'])
def predict():
    """Analyse skin tone, hair colour and blackhead presence from an uploaded image."""
    if _grooming_service is None:
        return jsonify({'error': 'Grooming service not initialised'}), 503
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    try:
        file = request.files['file']
        from PIL import Image as PILImage
        img = PILImage.open(file.stream)
        result = _grooming_service.predict_skin(img)
        return jsonify(result)
    except Exception as e:
        logger.error(f'Grooming predict error: {e}')
        return jsonify({'error': str(e)}), 500


@grooming_bp.route('/generate-hair', methods=['POST'])
def generate_hair():
    """Return an AI-generated hairstyle recommendation for the uploaded face image."""
    if _grooming_service is None:
        return jsonify({'error': 'Grooming service not initialised'}), 503
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    try:
        file = request.files['file']
        prompt = request.form.get(
            'prompt',
            'Generate a professional hairstyle recommendation for this person'
        )
        img_bytes = file.read()
        result = _grooming_service.generate_hair_recommendation(img_bytes, prompt)
        return jsonify(result)
    except Exception as e:
        logger.error(f'Hair generation error: {e}')
        return jsonify({'error': str(e)}), 500


@grooming_bp.route('/analyze-nail', methods=['POST'])
def analyze_nail():
    """Return nail-care recommendations based on an uploaded nail photo."""
    if _grooming_service is None:
        return jsonify({'error': 'Grooming service not initialised'}), 503
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    try:
        file = request.files['file']
        prompt = request.form.get(
            'prompt',
            'You are a professional manicurist. Analyse the nails in this photo for '
            'cleanliness, nail health, cuticle condition, discoloration, ridges, or '
            'damage. Provide a brief summary and 3-5 actionable care recommendations.'
        )
        img_bytes = file.read()
        result = _grooming_service.analyze_with_gemini(img_bytes, prompt)
        return jsonify(result)
    except Exception as e:
        logger.error(f'Nail analysis error: {e}')
        return jsonify({'error': str(e)}), 500


@grooming_bp.route('/analyze-dental', methods=['POST'])
def analyze_dental():
    """Return dental-hygiene recommendations based on an uploaded dental photo."""
    if _grooming_service is None:
        return jsonify({'error': 'Grooming service not initialised'}), 503
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    try:
        file = request.files['file']
        prompt = request.form.get(
            'prompt',
            'You are a dental hygienist. Analyse the teeth and gums in this photo for '
            'plaque, tartar, staining, gum inflammation, alignment concerns, and enamel '
            'wear. Provide a concise summary and 3-5 specific hygiene recommendations.'
        )
        img_bytes = file.read()
        result = _grooming_service.analyze_with_gemini(img_bytes, prompt)
        return jsonify(result)
    except Exception as e:
        logger.error(f'Dental analysis error: {e}')
        return jsonify({'error': str(e)}), 500
