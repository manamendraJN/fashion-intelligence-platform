from routes.general_routes import general_bp, init_general_routes, register_error_handlers
from routes.model_routes import model_bp, init_model_routes
from routes.analysis_routes import analysis_bp, init_analysis_routes
from routes.size_routes import size_bp, init_size_routes
from routes.wardrobe_routes import wardrobe_bp, init_wardrobe_routes
from routes.grooming_routes import grooming_bp, init_grooming_routes
from routes.accessory import accessory_bp
from routes.dress import dress_bp
from routes.recommend import recommend_bp
from routes.analytics import analytics_bp

__all__ = [
    # Core / shared
    'general_bp',
    'model_bp',
    'analysis_bp',
    'init_general_routes',
    'init_model_routes',
    'init_analysis_routes',
    'register_error_handlers',
    # Size recommendation
    'size_bp',
    'init_size_routes',
    # Wardrobe management
    'wardrobe_bp',
    'init_wardrobe_routes',
    # Grooming recommendation
    'grooming_bp',
    'init_grooming_routes',
    # Accessory recommendation (sub-blueprints)
    'accessory_bp',
    'dress_bp',
    'recommend_bp',
    'analytics_bp',
]
