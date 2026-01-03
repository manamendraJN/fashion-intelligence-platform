from flask import Flask
from flask_cors import CORS
import os
import logging
from core.config import Config
from services.model_service import ModelInference
from services.image_service import image_processor

# Import route blueprints
from routes import (
    general_bp,
    model_bp,
    analysis_bp,
    init_general_routes,
    init_model_routes,
    init_analysis_routes,
    register_error_handlers
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=Config.CORS_ORIGINS)

# Initialize services
logger.info("🚀 Initializing Body Measurement AI API...")
logger.info(f"📍 Model directory: {Config.MODEL_DIR}")

# Check if models exist
if not Config.MODEL_DIR.exists():
    logger.info(f"⚠️ Creating model directory: {Config.MODEL_DIR}")
    Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Load model
selected_model = os.getenv('MODEL_NAME', Config.DEFAULT_MODEL)
if selected_model != Config.DEFAULT_MODEL:
    logger.info(f"🔄 Using model from environment: {selected_model}")

try:
    model_inference = ModelInference(
        model_name=selected_model,
        device='cuda' if os.getenv('USE_GPU', 'False') == 'True' else 'cpu'
    )
    logger.info(f"✅ Model loaded: {selected_model}")
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    model_inference = None

logger.info("✅ API initialized successfully!")

# Initialize routes with dependencies
init_general_routes(model_inference)
init_model_routes(model_inference, image_processor)
init_analysis_routes(model_inference)

# Register blueprints
app.register_blueprint(general_bp)
app.register_blueprint(model_bp)
app.register_blueprint(analysis_bp)

# Register error handlers
register_error_handlers(app)

# Run server
if __name__ == '__main__':
    logger.info(f"\n{'='*60}")
    logger.info(f"🚀 Starting {Config.API_TITLE} v{Config.API_VERSION}")
    logger.info(f"📍 Host: {Config.HOST}:{Config.PORT}")
    logger.info(f"🔧 Debug: {Config.DEBUG}")
    logger.info(f"{'='*60}\n")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
