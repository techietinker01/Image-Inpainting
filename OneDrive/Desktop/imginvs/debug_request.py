import requests
import base64
import json
from PIL import Image
import io

# Create a simple test image and mask
test_img = Image.new('RGB', (100, 100), color='red')
mask_img = Image.new('RGB', (100, 100), color='white')

# Add a black circle on the mask (area to inpaint)
from PIL import ImageDraw
draw = ImageDraw.Draw(mask_img)
draw.ellipse([30, 30, 70, 70], fill='black')

# Convert to base64
def img_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

original_b64 = img_to_base64(test_img)
mask_b64 = img_to_base64(mask_img)

# Prepare data
data = {
    'original': f'data:image/png;base64,{original_b64}',
    'mask': f'data:image/png;base64,{mask_b64}'
}

print("Sending test request to Flask server...")
try:
    response = requests.post('http://127.0.0.1:5000/upload_mask', 
                           json=data, 
                           timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    if response.status_code == 200:
        print("SUCCESS: Image processing completed")
        if 'image' in response.headers.get('content-type', ''):
            print(f"Received image data, size: {len(response.content)} bytes")
        else:
            print(f"Response text: {response.text}")
    else:
        print(f"ERROR: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")