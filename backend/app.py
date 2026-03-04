from flask import Flask
from flask_cors import CORS

# Import blueprints
from routes.accessory import accessory_bp
from routes.dress import dress_bp
from routes.recommend import recommend_bp
from routes.analytics import analytics_bp

app = Flask(__name__, static_folder="static")
CORS(app)

app.register_blueprint(accessory_bp, url_prefix="/predict/accessory")
app.register_blueprint(dress_bp, url_prefix="/predict/dress")
app.register_blueprint(recommend_bp, url_prefix="/predict/recommend")
app.register_blueprint(analytics_bp, url_prefix="/plots")

if __name__ == "__main__":
    app.run(debug=True)