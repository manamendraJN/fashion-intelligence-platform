"""
AI Wardrobe System - Utility Functions
Helper functions for image processing and file handling
"""

import os
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    """
    Check if file has an allowed extension
    
    Args:
        filename: Name of the file
    
    Returns:
        bool: True if allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess image for model prediction
    
    Args:
        image_path: Path to the image file
        target_size: Target size tuple (height, width)
    
    Returns:
        numpy array of shape (224, 224, 3) normalized to [0, 1]
    """
    try:
        # Open image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Normalize to [0, 1]
        img_array = img_array.astype('float32') / 255.0
        
        return img_array
        
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")


def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file to upload folder
    
    Args: 
        file: Flask file object
        upload_folder: Path to upload folder
    
    Returns:
        str: Path to saved file
    """
    try:
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Generate unique filename if file already exists
        filepath = os.path.join(upload_folder, filename)
        counter = 1
        name, ext = os.path.splitext(filename)
        
        while os.path.exists(filepath):
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(upload_folder, filename)
            counter += 1
        
        # Save file
        file.save(filepath)
        
        return filepath
        
    except Exception as e: 
        raise ValueError(f"Error saving file: {str(e)}")


def cleanup_file(filepath):
    """
    Delete a file if it exists
    
    Args:
        filepath: Path to file to delete
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Warning: Could not delete file {filepath}:  {e}")


def format_prediction_response(prediction_result):
    """
    Format prediction results for API response
    
    Args:
        prediction_result:  Dictionary with prediction results
    
    Returns:
        Formatted dictionary
    """
    if 'error' in prediction_result: 
        return {
            'success': False,
            'error':  prediction_result['error']
        }
    
    return {
        'success': True,
        'data': prediction_result
    }