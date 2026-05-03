"""
routes/accessory_routes.py
Aggregates all accessory-recommendation sub-blueprints under /api/accessory.

Sub-blueprints:
  POST /api/accessory/classify   - classify an accessory image (Model 1)
  POST /api/accessory/dress      - extract dress attributes (Model 2)
  POST /api/accessory/recommend  - recommend accessories (Models 3 & 4)
  GET  /api/accessory/analytics/<filename> - serve analytics plots
"""

from flask import Blueprint

from routes.accessory import accessory_bp
from routes.dress import dress_bp
from routes.recommend import recommend_bp
from routes.analytics import analytics_bp

# Parent blueprint – nothing is attached directly to it; it is used only
# for the url_prefix when registered in app.py.
accessory_routes_bp = Blueprint('accessory', __name__)

__all__ = [
    'accessory_routes_bp',
    'accessory_bp',
    'dress_bp',
    'recommend_bp',
    'analytics_bp',
]
