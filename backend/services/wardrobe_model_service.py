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
        Try ML event model first → fallback to rule-based scores.
        Returns: { best_event, scores }
        """
        if not self._loaded:
            raise RuntimeError("Wardrobe models not loaded")

        clothing_type = metadata.get('article', 'Tops') if metadata else 'Tops'

        # Try ML event model
        if self.event_model and self.metadata_encoders and self.event_mlb:
            try:
                img_array = self.preprocess_image(image_input)
                img_batch = np.expand_dims(img_array, axis=0)

                meta = metadata or {}
                article = meta.get('article', clothing_type)
                color   = meta.get('color',   'Black')
                usage   = meta.get('usage',   'Casual')
                gender  = meta.get('gender',  'Women')

                # Safe encode with fallback
                def safe_encode(encoder, value, fallback):
                    if value in encoder.classes_:
                        return float(encoder.transform([value])[0])
                    return float(encoder.transform([fallback])[0])

                meta_features = np.array([[
                    safe_encode(self.metadata_encoders['article'], article, 'Tops'),
                    safe_encode(self.metadata_encoders['color'],   color,   'Black'),
                    safe_encode(self.metadata_encoders['usage'],   usage,   'Casual'),
                    safe_encode(self.metadata_encoders['gender'],  gender,  'Women'),
                ]])

                event_probs = self.event_model.predict(
                    {'image_input': img_batch, 'metadata_input': meta_features},
                    verbose=0
                )[0]

                event_names  = self.event_mlb.classes_
                event_scores = {
                    event: round(float(prob), 4)
                    for event, prob in zip(event_names, event_probs)
                }
                best_event = max(event_scores, key=event_scores.get)
                return {"best_event": best_event, "scores": event_scores}

            except Exception as e:
                logger.warning(f"Event model failed, using rule-based: {e}")

        # ✅ Fallback: rule-based (same as old project)
        scores     = self._get_rule_based_event_scores(clothing_type)
        best_event = max(scores, key=scores.get)
        return {"best_event": best_event, "scores": scores}

    def _get_rule_based_event_scores(self, clothing_type: str) -> dict:
        """Rule-based event scores — mirrors old project logic exactly."""
        t = clothing_type.lower()

        if any(x in t for x in ['suit', 'blazer', 'formal', 'tuxedo', 'evening gown']):
            return {'Tamil Wedding': 0.85, 'Western Wedding': 0.85, 'Party': 0.80, 'Office': 0.90, 'Casual': 0.30}

        if any(x in t for x in ['saree', 'kurta', 'sherwani', 'lehenga', 'salwar', 'dupatta', 'kurtis', 'patiala']):
            return {'Tamil Wedding': 0.95, 'Western Wedding': 0.70, 'Party': 0.75, 'Office': 0.50, 'Casual': 0.60}

        if any(x in t for x in ['cocktail', 'party dress', 'evening', 'gown']):
            return {'Tamil Wedding': 0.70, 'Western Wedding': 0.75, 'Party': 0.95, 'Office': 0.25, 'Casual': 0.40}

        if any(x in t for x in ['trousers', 'pencil skirt', 'chinos']):
            return {'Tamil Wedding': 0.40, 'Western Wedding': 0.45, 'Party': 0.50, 'Office': 0.85, 'Casual': 0.60}

        if any(x in t for x in ['track', 'jogger', 'sports', 'athletic', 'gym', 'legging', 'training']):
            return {'Tamil Wedding': 0.05, 'Western Wedding': 0.05, 'Party': 0.05, 'Office': 0.10, 'Casual': 0.95}

        if any(x in t for x in ['jeans', 'tshirt', 't-shirt', 'shorts', 'casual', 'hoodie', 'sweatshirt']):
            return {'Tamil Wedding': 0.15, 'Western Wedding': 0.15, 'Party': 0.30, 'Office': 0.40, 'Casual': 0.90}

        if any(x in t for x in ['jacket', 'sweater', 'sweatshirt']):
            return {'Tamil Wedding': 0.30, 'Western Wedding': 0.35, 'Party': 0.45, 'Office': 0.60, 'Casual': 0.85}

        if any(x in t for x in ['skirt', 'dress', 'tunic']):
            return {'Tamil Wedding': 0.50, 'Western Wedding': 0.55, 'Party': 0.65, 'Office': 0.70, 'Casual': 0.75}

        if any(x in t for x in ['top', 'shirt', 'blouse']):
            return {'Tamil Wedding': 0.40, 'Western Wedding': 0.40, 'Party': 0.55, 'Office': 0.75, 'Casual': 0.80}

        # Default
        return {'Tamil Wedding': 0.50, 'Western Wedding': 0.50, 'Party': 0.50, 'Office': 0.50, 'Casual': 0.70}

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