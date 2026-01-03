import os
from pathlib import Path

class Config:
    # API Configuration
    API_TITLE = "Body Measurement AI API"
    API_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Model Configuration
    BASE_DIR = Path(__file__).parent.parent
    MODEL_DIR = BASE_DIR / 'models'
    
    MODEL_FILES = {
        'model_v1': 'efficientnet-b3_model.pth',     #main model
        'model_v2': 'mobilenetv3_model.pth',         
        'model_v3': 'resnet50_model.pth',            
    }
    
    # Available models (using aliases mapped to actual files above)
    MODELS = {
        'model_v1': {
            'filename': MODEL_FILES['model_v1'],
            'path': MODEL_DIR / MODEL_FILES['model_v1'],
            'backbone': 'efficientnet_b3',
            'name': 'Model V1 (EfficientNet-B3)',
            'description': 'Balanced accuracy and speed',
            'speed': 'medium',
            'accuracy': 'high'
        },
        'model_v2': {
            'filename': MODEL_FILES['model_v2'],
            'path': MODEL_DIR / MODEL_FILES['model_v2'],
            'backbone': 'mobilenetv3_large_100',
            'name': 'Model V2 (MobileNetV3)',
            'description': 'Lightweight and fast',
            'speed': 'fast',
            'accuracy': 'medium'
        },
        'model_v3': {
            'filename': MODEL_FILES['model_v3'],
            'path': MODEL_DIR / MODEL_FILES['model_v3'],
            'backbone': 'resnet50',
            'name': 'Model V3 (ResNet50)',
            'description': 'High accuracy',
            'speed': 'slow',
            'accuracy': 'high'
        }
    }
    
    DEFAULT_MODEL = 'model_v1'  # Change to model_v2 or model_v3 as needed
    
    # Image Configuration
    IMG_SIZE = (512, 384)  # height, width
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Measurement Configuration
    MEASUREMENT_COLUMNS = [
        'ankle', 'arm-length', 'bicep', 'calf', 'chest', 'forearm',
        'height', 'hip', 'leg-length', 'shoulder-breadth',
        'shoulder-to-crotch', 'thigh', 'waist', 'wrist'
    ]
       
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
