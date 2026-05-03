"""
services/grooming_service.py
Loads ONNX skin-analysis models once at startup and provides inference helpers
for grooming recommendation endpoints.
"""

import io
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class GroomingService:
    """Wraps ONNX skin-analysis models and Gemini Vision API calls."""

    def __init__(self, model_dir: Path):
        self.model_dir = Path(model_dir)
        self.tone_sess = None
        self.color_sess = None
        self.black_sess = None
        self.tone_classes = []
        self.color_classes = []
        self.black_classes = []
        self._gemini_model = None
        self._load_models()

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    def _load_models(self):
        """Load ONNX models and label files if present; skip gracefully if not."""
        try:
            import onnxruntime as ort  # type: ignore

            tone_path  = self.model_dir / 'tone_convnext_tiny.onnx'
            color_path = self.model_dir / 'color_convnext_tiny.onnx'
            black_path = self.model_dir / 'blackhead_convnext_tiny.onnx'

            if tone_path.exists():
                self.tone_sess  = ort.InferenceSession(str(tone_path),  providers=['CPUExecutionProvider'])
                self.color_sess = ort.InferenceSession(str(color_path), providers=['CPUExecutionProvider'])
                self.black_sess = ort.InferenceSession(str(black_path), providers=['CPUExecutionProvider'])
                logger.info('✅ Grooming ONNX models loaded')
            else:
                logger.warning('⚠️  Grooming ONNX model files not found – skin analysis will be unavailable')

            for label_file, attr in [
                ('tone_labels.json',      'tone_classes'),
                ('color_labels.json',     'color_classes'),
                ('blackhead_labels.json', 'black_classes'),
            ]:
                path = self.model_dir / label_file
                if path.exists():
                    with open(path) as f:
                        setattr(self, attr, json.load(f))

        except ImportError:
            logger.warning('onnxruntime not installed – grooming skin-analysis models unavailable')
        except Exception as e:
            logger.error(f'Error loading grooming models: {e}')

    def _get_gemini_model(self):
        """Lazily return a configured Gemini generative model, or None if unconfigured."""
        if self._gemini_model is not None:
            return self._gemini_model
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return None
        try:
            import google.generativeai as genai  # type: ignore
            genai.configure(api_key=api_key)
            self._gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info('✅ Gemini Vision model configured')
        except Exception as e:
            logger.error(f'Failed to configure Gemini: {e}')
        return self._gemini_model

    @staticmethod
    def _run_onnx(sess, classes, pil_img, temp: float = 1.5):
        import torch
        from torchvision import transforms  # type: ignore

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        img = pil_img.convert('RGB')
        tensor = preprocess(img).unsqueeze(0)
        ort_inputs = {sess.get_inputs()[0].name: tensor.numpy()}
        logits = sess.run(None, ort_inputs)[0]
        probs = torch.softmax(torch.from_numpy(logits) / temp, dim=1)[0]
        top_idx = int(torch.argmax(probs))
        return {
            'top_class': classes[top_idx],
            'probs': {c: float(f'{p:.4f}') for c, p in zip(classes, probs.tolist())},
        }

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def predict_skin(self, pil_img) -> dict:
        """Run tone, colour and blackhead models on a PIL image."""
        if self.tone_sess is None:
            return {'error': 'Skin analysis models not loaded'}
        tone  = self._run_onnx(self.tone_sess,  self.tone_classes,  pil_img)
        color = self._run_onnx(self.color_sess, self.color_classes, pil_img)
        black = self._run_onnx(self.black_sess, self.black_classes, pil_img)
        return {'tone': tone, 'color': color, 'blackhead': black}

    def generate_hair_recommendation(self, img_bytes: bytes, prompt: str) -> dict:
        """Use Gemini Vision to generate a hairstyle recommendation."""
        return self.analyze_with_gemini(img_bytes, prompt)

    def analyze_with_gemini(self, img_bytes: bytes, prompt: str) -> dict:
        """Send an image + prompt to Gemini Vision and return the text response."""
        model = self._get_gemini_model()
        if model is None:
            return {'error': 'Gemini API key not configured'}
        try:
            from PIL import Image as PILImage  # type: ignore
            img = PILImage.open(io.BytesIO(img_bytes))
            response = model.generate_content([prompt, img])
            return {'success': True, 'recommendation': response.text}
        except Exception as e:
            logger.error(f'Gemini error: {e}')
            return {'error': str(e)}
