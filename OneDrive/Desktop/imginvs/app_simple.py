from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os
import base64
from PIL import Image
import cv2
import numpy as np
import io
import time
from datetime import datetime

app = Flask(__name__)

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get system status"""
    try:
        # Check if TensorFlow is available (but don't import it to avoid errors)
        tf_available = False
        model_loaded = False
        
        status = {
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'tensorflow_available': tf_available,
            'model_loaded': model_loaded,
            'processing_method': 'opencv_fallback'
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_mask', methods=['POST'])
def upload_mask():
    """Handle image upload and mask processing"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data or 'original_image' not in data or 'mask_image' not in data:
            return jsonify({'error': 'Missing image data'}), 400

        # Decode base64 images
        original_b64 = data['original_image'].split(',')[1] if ',' in data['original_image'] else data['original_image']
        mask_b64 = data['mask_image'].split(',')[1] if ',' in data['mask_image'] else data['mask_image']
        
        original_bytes = base64.b64decode(original_b64)
        mask_bytes = base64.b64decode(mask_b64)
        
        # Convert to PIL Images
        original_image = Image.open(io.BytesIO(original_bytes)).convert('RGB')
        mask_image = Image.open(io.BytesIO(mask_bytes)).convert('L')
        
        # Save uploaded images
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_path = f'uploads/original_{timestamp}.png'
        mask_path = f'uploads/mask_{timestamp}.png'
        
        original_image.save(original_path)
        mask_image.save(mask_path)
        
        # Process with OpenCV inpainting (fallback method)
        result_image = process_with_opencv(original_image, mask_image)
        
        # Convert result to base64
        img_buffer = io.BytesIO()
        result_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        result_b64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        processing_time = time.time() - start_time
        
        # Return as image with headers
        response = app.response_class(
            response=img_buffer.getvalue(),
            status=200,
            mimetype='image/png'
        )
        response.headers['X-Processing-Method'] = 'opencv_telea'
        response.headers['X-Processing-Time'] = f'{processing_time:.2f}s'
        
        return response
        
    except Exception as e:
        print(f"Error in upload_mask: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_with_opencv(original_image, mask_image):
    """Process image inpainting using OpenCV"""
    try:
        # Convert PIL to OpenCV format
        original_cv = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
        mask_cv = np.array(mask_image)
        
        # Ensure mask and image have same dimensions
        if original_cv.shape[:2] != mask_cv.shape[:2]:
            mask_cv = cv2.resize(mask_cv, (original_cv.shape[1], original_cv.shape[0]))
        
        # Ensure proper data types
        original_cv = original_cv.astype(np.uint8)
        mask_cv = mask_cv.astype(np.uint8)
        
        # Apply inpainting using Telea algorithm
        result_cv = cv2.inpaint(original_cv, mask_cv, 3, cv2.INPAINT_TELEA)
        
        # Convert back to PIL
        result_rgb = cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB)
        result_image = Image.fromarray(result_rgb)
        
        return result_image
        
    except Exception as e:
        print(f"OpenCV processing error: {str(e)}")
        # Return original image if processing fails
        return original_image

if __name__ == '__main__':
    print("Starting Flask server...")
    print("TensorFlow functionality disabled due to import issues")
    print("Using OpenCV inpainting fallback")
    app.run(host='0.0.0.0', port=5000, debug=False)