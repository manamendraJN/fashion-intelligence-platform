from flask import Flask
from flask_cors import CORS
import os
import logging
from pathlib import Path
from core.config import Config
from services.model_service import ModelInference
from services.image_service import image_processor
from services.wardrobe_model_service import WardrobeModelService
from services.grooming_service import GroomingService

# Import route blueprints
from routes import (
    general_bp,
    model_bp,
    analysis_bp,
    size_bp,
    wardrobe_bp,
    grooming_bp,
    accessory_bp,
    dress_bp,
    recommend_bp,
    analytics_bp,
    init_general_routes,
    init_model_routes,
    init_analysis_routes,
    init_size_routes,
    init_wardrobe_routes,
    init_grooming_routes,
    register_error_handlers,
)
from routes.admin_routes import admin_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow requests from web frontend and mobile app
CORS(app,
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
     )

# Initialize services
logger.info("🚀 Initializing Fashion Intelligence Platform...")
logger.info(f"📍 Model directory: {Config.MODEL_DIR}")

# Ensure model directory exists
if not Config.MODEL_DIR.exists():
    logger.info(f"⚠️ Creating model directory: {Config.MODEL_DIR}")
    Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ── Load body-measurement model ──────────────────────────────────────
selected_model = os.getenv('MODEL_NAME', Config.DEFAULT_MODEL)
if selected_model != Config.DEFAULT_MODEL:
    logger.info(f"🔄 Using model from environment: {selected_model}")

try:
    model_inference = ModelInference(
        model_name=selected_model,
        device='cuda' if os.getenv('USE_GPU', 'False') == 'True' else 'cpu'
    )
    logger.info(f"✅ Body measurement model loaded: {selected_model}")
except Exception as e:
    logger.error(f"❌ Error loading body measurement model: {e}")
    model_inference = None

# ── Load wardrobe AI models ──────────────────────────────────────────
try:
    wardrobe_service = WardrobeModelService(Config.WARDROBE_MODEL_DIR)
    logger.info("✅ Wardrobe AI models loaded")
except Exception as e:
    logger.error(f"❌ Error loading wardrobe models: {e}")
    wardrobe_service = None

# ── Load grooming models ─────────────────────────────────────────────
try:
    grooming_service = GroomingService(Config.MODEL_DIR)
    logger.info("✅ Grooming service initialised")
except Exception as e:
    logger.error(f"❌ Error initialising grooming service: {e}")
    grooming_service = None

logger.info("✅ All services initialised!")

# ── Initialise routes with service dependencies ──────────────────────
init_general_routes(model_inference)
init_model_routes(model_inference, image_processor)
init_analysis_routes(model_inference)
init_size_routes()
init_wardrobe_routes(wardrobe_service)
init_grooming_routes(grooming_service)

# ── Register blueprints ──────────────────────────────────────────────
# Core / body-measurement routes (no prefix – legacy paths)
app.register_blueprint(general_bp)
app.register_blueprint(model_bp)
app.register_blueprint(analysis_bp)

# Size recommendation
app.register_blueprint(size_bp, url_prefix='/api/size')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Wardrobe management
app.register_blueprint(wardrobe_bp, url_prefix='/api/wardrobe')

# Accessory recommendation
app.register_blueprint(accessory_bp, url_prefix='/api/accessory/classify')
app.register_blueprint(dress_bp,     url_prefix='/api/accessory/dress')
app.register_blueprint(recommend_bp, url_prefix='/api/accessory/recommend')
app.register_blueprint(analytics_bp, url_prefix='/api/accessory/analytics')

# Grooming recommendation
app.register_blueprint(grooming_bp, url_prefix='/api/grooming')

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
