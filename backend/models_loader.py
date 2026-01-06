"""
AI Wardrobe System - Model Loader (SAFE VERSION)
Loads all trained ML models and encoders with error handling
"""

import os
import pickle
import numpy as np
from tensorflow import keras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModelLoader:  
    """Load and manage all ML models"""
    
    def __init__(self, models_path=None):
        """Initialize model loader"""
        
        if models_path is None: 
            models_path = os. getenv('MODELS_PATH', '../models')
        
        self.models_path = os. path.abspath(models_path)
        
        print(f"🔧 Initializing Model Loader...")
        print(f"   Models directory: {self.models_path}")
        
        # Model instances
        self. cnn_model = None
        self.temporal_model = None
        self.event_model = None
        
        # Encoders
        self.label_encoder = None
        self.event_encoder = None
        self.event_mlb = None
        self. metadata_encoders = None
        
        # Load errors (for debugging)
        self.load_errors = {}
        
        # Load all models
        self._load_models()
    
    def _load_models(self):
        """Load all models and encoders with error handling"""
        
        # 1. Load CNN Model (Visual Features)
        print("\n📦 Loading CNN model...")
        try:
            cnn_h5_path = os.path. join(self.models_path, 'cnn_visual_features. h5')
            cnn_keras_path = os.path. join(self.models_path, 'cnn_visual_features.keras')
            
            if os.path.exists(cnn_h5_path):
                self.cnn_model = keras.models.load_model(cnn_h5_path, compile=False)
                print(f"   ✅ CNN model loaded (. h5 format)")
            elif os.path.exists(cnn_keras_path):
                self.cnn_model = keras. models.load_model(cnn_keras_path, compile=False)
                print(f"   ✅ CNN model loaded (. keras format)")
            else:
                print(f"   ❌ CNN model not found")
        except Exception as e:
            error_msg = str(e)[:150]
            print(f"   ⚠️  CNN model load failed: {error_msg}")
            self.load_errors['cnn'] = error_msg
            self.cnn_model = None
        
        # 2. Load Temporal Model (GRU or LSTM)
        print("\n📦 Loading temporal model...")
        try:
            gru_path = os. path.join(self.models_path, 'gru_temporal_patterns.keras')
            lstm_path = os.path.join(self.models_path, 'lstm_temporal_patterns.keras')
            
            if os. path.exists(gru_path):
                self.temporal_model = keras.models.load_model(gru_path, compile=False)
                print(f"   ✅ GRU model loaded")
            elif os. path.exists(lstm_path):
                self.temporal_model = keras.models.load_model(lstm_path, compile=False)
                print(f"   ✅ LSTM model loaded")
            else:
                print(f"   ❌ Temporal model not found")
        except Exception as e:
            error_msg = str(e)[:150]
            print(f"   ⚠️  Temporal model load failed: {error_msg}")
            self.load_errors['temporal'] = error_msg
            self.temporal_model = None
        
        # 3. Load Event Association Model
        print("\n📦 Loading event model...")
        try:
            event_path = os.path.join(self.models_path, 'event_association_model.keras')
            
            if os.path.exists(event_path):
                self.event_model = keras.models.load_model(event_path, compile=False)
                print(f"   ✅ Event model loaded")
            else:
                print(f"   ❌ Event model not found")
        except Exception as e: 
            error_msg = str(e)[:150]
            print(f"   ⚠️  Event model load failed: {error_msg}")
            self.load_errors['event'] = error_msg
            self.event_model = None
        
        # 4. Load Encoders
        print("\n📦 Loading encoders...")
        
        try:
            label_enc_path = os.path.join(self.models_path, 'label_encoder.pkl')
            if os.path.exists(label_enc_path):
                with open(label_enc_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print(f"   ✅ Label encoder loaded")
        except Exception as e:
            print(f"   ⚠️  Label encoder load failed")
            self.load_errors['label_encoder'] = str(e)[:100]
        
        try: 
            event_enc_path = os.path.join(self. models_path, 'event_encoder.pkl')
            if os.path.exists(event_enc_path):
                with open(event_enc_path, 'rb') as f:
                    self.event_encoder = pickle. load(f)
                print(f"   ✅ Event encoder loaded")
        except Exception as e:
            print(f"   ⚠️  Event encoder load failed")
            self.load_errors['event_encoder'] = str(e)[:100]
        
        try:
            event_mlb_path = os. path.join(self.models_path, 'event_mlb.pkl')
            if os.path.exists(event_mlb_path):
                with open(event_mlb_path, 'rb') as f:
                    self.event_mlb = pickle.load(f)
                print(f"   ✅ Event MLB loaded")
        except Exception as e:
            print(f"   ⚠️  Event MLB load failed")
            self.load_errors['event_mlb'] = str(e)[:100]
        
        try:
            metadata_enc_path = os.path.join(self.models_path, 'metadata_encoders.pkl')
            if os.path.exists(metadata_enc_path):
                with open(metadata_enc_path, 'rb') as f:
                    self.metadata_encoders = pickle.load(f)
                print(f"   ✅ Metadata encoders loaded")
        except Exception as e: 
            print(f"   ⚠️  Metadata encoders load failed")
            self.load_errors['metadata_encoders'] = str(e)[:100]
        
        # Summary
        loaded_count = sum([
            self.cnn_model is not None,
            self.temporal_model is not None,
            self.event_model is not None
        ])
        
        print(f"\n📊 Loaded {loaded_count}/3 models successfully")
        
        if loaded_count == 0:
            print("\n⚠️  WARNING: No models loaded!")
            print("   Reason: TensorFlow/Keras version mismatch")
            print("   Models trained with:  TensorFlow 2.19.0 / Keras 3.x (Google Colab)")
            print("   Current environment: TensorFlow 2.18.0")
            print("\n   💡 SOLUTIONS:")
            print("      1. Retrain models with current TensorFlow version")
            print("      2. Use Google Colab for inference")
            print("      3. Export models to ONNX format (version-independent)")
        else:
            print("\n✅ Backend ready with available models")
    
    def predict_clothing_type(self, image_array):
        """
        Predict clothing type from image
        
        Args: 
            image_array: numpy array of shape (224, 224, 3)
        
        Returns: 
            dict with prediction results
        """
        
        if self. cnn_model is None: 
            return {
                'error':  'CNN model not loaded',
                'reason': self.load_errors. get('cnn', 'Model file not found or incompatible'),
                'suggestion': 'Retrain model with current TensorFlow version or use Colab'
            }
        
        try: 
            img_batch = np.expand_dims(image_array, axis=0)
            predictions = self.cnn_model. predict(img_batch, verbose=0)[0]
            
            top_idx = np.argmax(predictions)
            top_type = self.label_encoder.inverse_transform([top_idx])[0]
            confidence = float(predictions[top_idx])
            
            top_5_idx = np.argsort(predictions)[-5:][::-1]
            top_5 = [
                {
                    'type':  self.label_encoder.inverse_transform([idx])[0],
                    'confidence': float(predictions[idx])
                }
                for idx in top_5_idx
            ]
            
            return {
                'type': top_type,
                'confidence': confidence,
                'top_5':  top_5
            }
            
        except Exception as e: 
            return {'error': str(e)}
    
    def predict_events(self, image_array, metadata):
        """
        Predict suitable events for clothing item
        
        Args:
            image_array: numpy array of shape (224, 224, 3)
            metadata: dict with articleType, baseColour, usage, gender
        
        Returns: 
            dict with event predictions
        """
        
        if self. event_model is None:
            return {
                'error': 'Event model not loaded',
                'reason': self.load_errors.get('event', 'Model file not found or incompatible'),
                'suggestion': 'Retrain model with current TensorFlow version or use Colab'
            }
        
        try: 
            img_batch = np.expand_dims(image_array, axis=0)
            
            metadata_features = np.array([[
                self.metadata_encoders['article']. transform([metadata['articleType']])[0],
                self.metadata_encoders['color'].transform([metadata['baseColour']])[0],
                self.metadata_encoders['usage'].transform([metadata['usage']])[0],
                self.metadata_encoders['gender'].transform([metadata['gender']])[0]
            ]])
            
            event_probs = self.event_model.predict(
                {'image_input': img_batch, 'metadata_input': metadata_features},
                verbose=0
            )[0]
            
            event_names = self.event_mlb.classes_
            events = [
                {
                    'event': event,
                    'probability': float(prob)
                }
                for event, prob in zip(event_names, event_probs)
            ]
            
            events. sort(key=lambda x: x['probability'], reverse=True)
            
            return {'events': events}
            
        except Exception as e:
            return {'error':  str(e)}
    
    def get_model_info(self):
        """Get information about loaded models"""
        
        return {
            'cnn_loaded':  self.cnn_model is not None,
            'temporal_loaded': self.temporal_model is not None,
            'event_loaded': self.event_model is not None,
            'label_encoder_loaded': self.label_encoder is not None,
            'event_encoder_loaded': self.event_encoder is not None,
            'event_mlb_loaded':  self.event_mlb is not None,
            'metadata_encoders_loaded': self.metadata_encoders is not None,
            'load_errors': self.load_errors if self.load_errors else None
        }


# Global model loader instance
model_loader = None

def get_model_loader():
    """Get or create model loader instance"""
    global model_loader
    
    if model_loader is None: 
        model_loader = ModelLoader()
    
    return model_loader