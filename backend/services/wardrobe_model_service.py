"""
services/wardrobe_model_service.py
Handles loading and inference for all wardrobe ML models.
Compatible with TensorFlow 2.19 / Keras 3.10
Mirrors logic from old project's models_loader.py (which works correctly)
"""

import numpy as np
import pickle
import logging
from pathlib import Path
from PIL import Image
from tensorflow import keras

# Import improved event scoring from event_constants
import sys
sys.path.append(str(Path(__file__).parent.parent))
from core.event_constants import get_default_event_scores, STANDARD_EVENTS

logger = logging.getLogger(__name__)


class WardrobeModelService:

    def __init__(self, model_dir: Path):
        self.model_dir         = Path(model_dir)
        self.cnn_model         = None
        self.event_model       = None
        self.gru_model         = None
        self.lstm_model        = None
        self.label_encoder     = None
        self.event_encoder     = None
        self.event_mlb         = None
        self.metadata_encoders = None
        self._loaded           = False
        self._load_all()

    # ─────────────────────────── Loading ────────────────────────────

    def _load_all(self):
        try:
            logger.info("🧥 Loading wardrobe models...")

            # ✅ Try .h5 first (works correctly), fallback to .keras
            cnn_h5    = self.model_dir / 'cnn_visual_features.h5'
            cnn_keras = self.model_dir / 'cnn_visual_features.keras'

            if cnn_h5.exists():
                self.cnn_model = keras.models.load_model(str(cnn_h5), compile=False)
                logger.info("  ✅ CNN clothing classifier loaded (.h5)")
            elif cnn_keras.exists():
                self.cnn_model = keras.models.load_model(str(cnn_keras), compile=False)
                logger.info("  ✅ CNN clothing classifier loaded (.keras)")
            else:
                logger.error("  ❌ CNN model not found")

            # GRU / LSTM
            gru_path  = self.model_dir / 'gru_temporal_patterns.keras'
            lstm_path = self.model_dir / 'lstm_temporal_patterns.keras'
            if gru_path.exists():
                self.gru_model = keras.models.load_model(str(gru_path), compile=False)
                logger.info("  ✅ GRU temporal model loaded")
            if lstm_path.exists():
                self.lstm_model = keras.models.load_model(str(lstm_path), compile=False)
                logger.info("  ✅ LSTM temporal model loaded")

            # Event model
            event_path = self.model_dir / 'event_association_model.keras'
            if event_path.exists():
                self.event_model = keras.models.load_model(str(event_path), compile=False)
                logger.info("  ✅ Event association model loaded")

            # Encoders
            for attr, filename in [
                ('label_encoder',     'label_encoder.pkl'),
                ('event_encoder',     'event_encoder.pkl'),
                ('event_mlb',         'event_mlb.pkl'),
                ('metadata_encoders', 'metadata_encoders.pkl'),
            ]:
                path = self.model_dir / filename
                if path.exists():
                    with open(path, 'rb') as f:
                        setattr(self, attr, pickle.load(f))
                    logger.info(f"  ✅ {filename} loaded")

            self._loaded = True
            logger.info("🎉 All wardrobe models ready!")

        except Exception as e:
            logger.error(f"❌ Failed to load wardrobe models: {e}")
            self._loaded = False

    # ─────────────────────────── Image Preprocessing ────────────────

    def preprocess_image(self, image_input) -> np.ndarray:
        """Returns (224, 224, 3) float32 array — NO batch dimension."""
        if isinstance(image_input, np.ndarray):
            img = Image.fromarray(image_input)
        elif isinstance(image_input, Image.Image):
            img = image_input
        else:
            img = Image.open(image_input)
        img = img.convert('RGB').resize((224, 224))
        return np.array(img, dtype=np.float32) / 255.0   # normalize 0-1

    # ─────────────────────────── Clothing Classification ────────────

    def predict_clothing(self, image_input) -> dict:
        """
        ✅ Uses label_encoder (20 classes) matching .h5 model output.
        Returns: { clothing_type, confidence, top_5, all_scores }
        """
        if not self._loaded:
            raise RuntimeError("Wardrobe models not loaded")

        img_array  = self.preprocess_image(image_input)
        img_batch  = np.expand_dims(img_array, axis=0)          # (1,224,224,3)
        preds      = self.cnn_model.predict(img_batch, verbose=0)[0]

        # ✅ label_encoder matches .h5 model (both 20 classes)
        top_idx    = int(np.argmax(preds))
        top_type   = self.label_encoder.inverse_transform([top_idx])[0]
        confidence = float(preds[top_idx])

        # Top 5
        top5_idx = np.argsort(preds)[-5:][::-1]
        top_5 = [
            {
                'type':       self.label_encoder.inverse_transform([i])[0],
                'confidence': round(float(preds[i]), 4)
            }
            for i in top5_idx
        ]

        # All scores
        all_scores = {
            self.label_encoder.inverse_transform([i])[0]: round(float(preds[i]), 4)
            for i in range(len(preds))
        }

        return {
            "clothing_type": top_type,
            "confidence":    round(confidence, 4),
            "top_5":         top_5,
            "all_scores":    all_scores
        }

    # ─────────────────────────── Event Scoring ──────────────────────

    def predict_event_scores(self, image_input, metadata: dict = None) -> dict:
        """
        Use improved rule-based event scoring from event_constants.py
        This replaces the unreliable ML event model with accurate, consistent scoring.
        Returns: { best_event, scores }
        """
        if not self._loaded:
            raise RuntimeError("Wardrobe models not loaded")

        clothing_type = metadata.get('article', 'Tops') if metadata else 'Tops'
        
        # ✅ Use improved rule-based scoring (supports all clothing types including traditional wear)
        scores = get_default_event_scores(clothing_type)
        
        # Convert to old event name format for backward compatibility
        # Maps new standard names back to old DB format if needed
        old_format_scores = {}
        event_name_mapping = {
            'Casual': 'Casual Outing',
            'Office': 'Office Meeting',
            'Beach': 'Beach Outing',
            'Date': 'Date Night',
            'Sports': 'Sports Event',
            'Religious': 'Religious Event',
            'Family Gathering': 'Family Gathering'
        }
        
        for new_name, score in scores.items():
            old_name = event_name_mapping.get(new_name, new_name)
            old_format_scores[old_name] = score
        
        best_event = max(old_format_scores, key=old_format_scores.get)
        return {"best_event": best_event, "scores": old_format_scores}

    # ──────────────────────────────────────────────────────────────────
    # DEPRECATED: Old rule-based scoring (kept for reference only)
    # Now using get_default_event_scores() from core/event_constants.py
    # ──────────────────────────────────────────────────────────────────
    """
    def _get_rule_based_event_scores(self, clothing_type: str) -> dict:
        #Rule-based event scores - updated to match ML model event names.
        t = clothing_type.lower()

        # Map to ML model event names
        if any(x in t for x in ['suit', 'blazer', 'formal', 'tuxedo', 'evening gown']):
            return {
                'Tamil Wedding': 0.85, 'Western Wedding': 0.85, 'Party': 0.80, 
                'Office Meeting': 0.90, 'Casual Outing': 0.30, 'Beach Outing': 0.20,
                'Date Night': 0.75, 'Family Gathering': 0.70, 'Shopping': 0.50,
                'Gym': 0.05, 'Sports Event': 0.05, 'Religious Event': 0.70
            }

        if any(x in t for x in ['saree', 'kurta', 'sherwani', 'lehenga', 'salwar', 'dupatta', 'kurtis', 'patiala']):
            return {
                'Tamil Wedding': 0.95, 'Western Wedding': 0.70, 'Party': 0.75,
                'Office Meeting': 0.50, 'Casual Outing': 0.60, 'Beach Outing': 0.30,
                'Date Night': 0.70, 'Family Gathering': 0.90, 'Shopping': 0.60,
                'Gym': 0.05, 'Sports Event': 0.05, 'Religious Event': 0.95
            }

        if any(x in t for x in ['cocktail', 'party dress', 'evening', 'gown']):
            return {
                'Tamil Wedding': 0.70, 'Western Wedding': 0.75, 'Party': 0.95,
                'Office Meeting': 0.25, 'Casual Outing': 0.40, 'Beach Outing': 0.30,
                'Date Night': 0.95, 'Family Gathering': 0.70, 'Shopping': 0.50,
                'Gym': 0.05, 'Sports Event': 0.05, 'Religious Event': 0.60
            }

        if any(x in t for x in ['trousers', 'pencil skirt', 'chinos', 'formal pants']):
            return {
                'Tamil Wedding': 0.40, 'Western Wedding': 0.45, 'Party': 0.50,
                'Office Meeting': 0.90, 'Casual Outing': 0.70, 'Beach Outing': 0.30,
                'Date Night': 0.60, 'Family Gathering': 0.65, 'Shopping': 0.75,
                'Gym': 0.10, 'Sports Event': 0.10, 'Religious Event': 0.50
            }

        if any(x in t for x in ['track', 'jogger', 'sports', 'athletic', 'gym', 'legging', 'training']):
            return {
                'Tamil Wedding': 0.05, 'Western Wedding': 0.05, 'Party': 0.05,
                'Office Meeting': 0.10, 'Casual Outing': 0.85, 'Beach Outing': 0.70,
                'Date Night': 0.10, 'Family Gathering': 0.40, 'Shopping': 0.70,
                'Gym': 0.98, 'Sports Event': 0.95, 'Religious Event': 0.05
            }

        if any(x in t for x in ['jeans', 'tshirt', 't-shirt', 'shorts', 'casual', 'hoodie', 'sweatshirt']):
            return {
                'Tamil Wedding': 0.15, 'Western Wedding': 0.15, 'Party': 0.30,
                'Office Meeting': 0.35, 'Casual Outing': 0.95, 'Beach Outing': 0.75,
                'Date Night': 0.50, 'Family Gathering': 0.80, 'Shopping': 0.90,
                'Gym': 0.50, 'Sports Event': 0.40, 'Religious Event': 0.30
            }

        # Check for formal jackets/blazers first (more specific)
        if any(x in t for x in ['blazer', 'jacket']) and not any(x in t for x in ['bomber', 'denim', 'leather', 'windbreaker']):
            return {
                'Tamil Wedding': 0.70, 'Western Wedding': 0.75, 'Party': 0.80,
                'Office Meeting': 0.95, 'Casual Outing': 0.40, 'Beach Outing': 0.20,
                'Date Night': 0.75, 'Family Gathering': 0.70, 'Shopping': 0.60,
                'Gym': 0.10, 'Sports Event': 0.10, 'Religious Event': 0.65
            }
        
        # Casual outerwear (sweaters, cardigans, casual jackets)
        if any(x in t for x in ['sweater', 'sweatshirt', 'cardigan', 'hoodie']):
            return {
                'Tamil Wedding': 0.20, 'Western Wedding': 0.25, 'Party': 0.35,
                'Office Meeting': 0.50, 'Casual Outing': 0.90, 'Beach Outing': 0.40,
                'Date Night': 0.50, 'Family Gathering': 0.75, 'Shopping': 0.85,
                'Gym': 0.40, 'Sports Event': 0.30, 'Religious Event': 0.40
            }

        if any(x in t for x in ['skirt', 'tunic']):
            return {
                'Tamil Wedding': 0.50, 'Western Wedding': 0.55, 'Party': 0.65,
                'Office Meeting': 0.75, 'Casual Outing': 0.80, 'Beach Outing': 0.60,
                'Date Night': 0.75, 'Family Gathering': 0.75, 'Shopping': 0.85,
                'Gym': 0.15, 'Sports Event': 0.15, 'Religious Event': 0.60
            }

        if any(x in t for x in ['dress']):
            return {
                'Tamil Wedding': 0.50, 'Western Wedding': 0.55, 'Party': 0.70,
                'Office Meeting': 0.60, 'Casual Outing': 0.85, 'Beach Outing': 0.75,
                'Date Night': 0.85, 'Family Gathering': 0.80, 'Shopping': 0.85,
                'Gym': 0.10, 'Sports Event': 0.10, 'Religious Event': 0.55
            }

        if any(x in t for x in ['top', 'shirt', 'blouse']):
            return {
                'Tamil Wedding': 0.40, 'Western Wedding': 0.40, 'Party': 0.55,
                'Office Meeting': 0.80, 'Casual Outing': 0.85, 'Beach Outing': 0.60,
                'Date Night': 0.65, 'Family Gathering': 0.75, 'Shopping': 0.85,
                'Gym': 0.30, 'Sports Event': 0.30, 'Religious Event': 0.55
            }

        # Default for unrecognized types
        return {
            'Tamil Wedding': 0.50, 'Western Wedding': 0.50, 'Party': 0.50,
            'Office Meeting': 0.50, 'Casual Outing': 0.70, 'Beach Outing': 0.50,
            'Date Night': 0.50, 'Family Gathering': 0.65, 'Shopping': 0.70,
            'Gym': 0.30, 'Sports Event': 0.30, 'Religious Event': 0.50
        }
    """
    # ──────────────────────────────────────────────────────────────────

    # ─────────────────────────── Full Analysis ──────────────────────

    def full_analysis(self, image_input, metadata: dict = None) -> dict:
        """Run clothing classification + event scoring in one call."""
        clothing = self.predict_clothing(image_input)

        if metadata is None:
            metadata = {
                'article': clothing['clothing_type'],
                'color':   'Black',
                'usage':   'Casual',
                'gender':  'Women'
            }

        events = self.predict_event_scores(image_input, metadata)

        return {
            "clothing_type":  clothing['clothing_type'],
            "confidence":     clothing['confidence'],
            "top_5":          clothing['top_5'],
            "all_scores":     clothing['all_scores'],
            "best_event":     events['best_event'],
            "event_scores":   events['scores'],
            "metadata_used":  metadata
        }

    # ─────────────────────────── Temporal Prediction ────────────────

    def predict_next_event(self, wear_history: list, use_gru: bool = True) -> dict:
        if not self._loaded:
            raise RuntimeError("Wardrobe models not loaded")

        seq = wear_history[-10:] if len(wear_history) >= 10 else \
              [0] * (10 - len(wear_history)) + wear_history
        seq_array = np.array([seq], dtype=np.float32)

        model = self.gru_model if use_gru else self.lstm_model
        preds = model.predict(seq_array, verbose=0)[0]

        event_scores = {
            self.event_encoder.classes_[i]: round(float(preds[i]), 4)
            for i in range(len(preds))
        }
        best_event = max(event_scores, key=event_scores.get)

        return {
            "predicted_event": best_event,
            "scores":          event_scores,
            "model_used":      "GRU" if use_gru else "LSTM"
        }