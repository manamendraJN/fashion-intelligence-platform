"""
AI Wardrobe System - Flask Backend API
Main application file with prediction endpoints
"""

import os
from flask import Flask, request, jsonify, send_from_directory   # <--- UPDATED IMPORT
from flask_cors import CORS
from dotenv import load_dotenv
from models_loader import get_model_loader
from utils import (
    allowed_file, 
    preprocess_image, 
    save_uploaded_file, 
    cleanup_file,
    format_prediction_response
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=cors_origins)

# Configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

# Initialize model loader
print("\n" + "="*60)
print("🚀 Starting AI Wardrobe System Backend")
print("="*60)

try:
    model_loader = get_model_loader()
    print("\n✅ Backend ready!")
except Exception as e: 
    print(f"\n❌ Failed to load models:  {e}")
    model_loader = None


# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'AI Wardrobe System Backend API',
        'version': '1.0.0'
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Detailed health check with model status"""
    
    if model_loader is None:
        return jsonify({
            'status': 'error',
            'message': 'Models not loaded'
        }), 500
    
    model_info = model_loader.get_model_info()
    
    return jsonify({
        'status': 'healthy',
        'models':  model_info
    })
import os

@app.route('/api/wardrobe', methods=['GET'])
def list_wardrobe():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify([
        {
            "filename": f,
            "url": f"/uploads/{f}"
        }
        for f in files if not f.startswith('.')
    ])


@app.route('/api/predict/clothing-type', methods=['POST'])
def predict_clothing_type():
    """
    Predict clothing type from uploaded image
    
    Request:  multipart/form-data with 'image' file
    Response: JSON with prediction results
    """
    
    # Check if model is loaded
    if model_loader is None:
        return jsonify({
            'success': False,
            'error':  'Models not loaded'
        }), 500
    
    # Check if file is present
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image file provided'
        }), 400
    
    file = request.files['image']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error':  'Invalid file type.  Allowed: jpg, jpeg, png, webp'
        }), 400
    
    filepath = None
    
    try:
        # Save uploaded file
        filepath = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        
        # Preprocess image
        image_array = preprocess_image(filepath)
        
        # Predict
        result = model_loader.predict_clothing_type(image_array)
        
        # Format response
        response = format_prediction_response(result)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    


@app.route('/api/predict/events', methods=['POST'])
def predict_events():
    """
    Predict suitable events for clothing item
    
    Request:  multipart/form-data with: 
        - image: file
        - articleType: string
        - baseColour: string
        - usage: string
        - gender: string
    
    Response: JSON with event predictions
    """
    
    # Check if model is loaded
    if model_loader is None:
        return jsonify({
            'success': False,
            'error': 'Models not loaded'
        }), 500
    
    # Check if file is present
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image file provided'
        }), 400
    
    file = request.files['image']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'success': False,
            'error':  'No file selected'
        }), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Allowed: jpg, jpeg, png, webp'
        }), 400
    
    # Get metadata from form
    try:
        metadata = {
            'articleType': request.form.get('articleType'),
            'baseColour': request.form.get('baseColour'),
            'usage': request.form.get('usage'),
            'gender':  request.form.get('gender')
        }
        
        # Validate metadata
        for key, value in metadata.items():
            if not value:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {key}'
                }), 400
                
    except Exception as e:
        return jsonify({
            'success':  False,
            'error': f'Invalid metadata: {str(e)}'
        }), 400
    
    filepath = None
    
    try:
        # Save uploaded file
        filepath = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        
        # Preprocess image
        image_array = preprocess_image(filepath)
        
        # Predict
        result = model_loader.predict_events(image_array, metadata)
        
        # Format response
        response = format_prediction_response(result)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error':  str(e)
        }), 500
        
    finally: 
        # Cleanup uploaded file
        if filepath:
            cleanup_file(filepath)


# ------- New Route: Serve Uploaded Images ----------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files so React frontend can access them.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# ---------------------------------------------------------


# ==================== RUN APP ====================

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n🌐 Starting server on http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}\n")
    
    app.run(host=host, port=port, debug=debug)