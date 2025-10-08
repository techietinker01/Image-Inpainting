import requests
import base64
from PIL import Image, ImageDraw
import io

# Create simple test images
orig = Image.new('RGB', (256,256), color=(100,150,200))
mask = Image.new('RGB', (256,256), color=(255,255,255))
ImageDraw.Draw(mask).rectangle([50,50,200,200], fill=(0,0,0))

def img_to_b64(img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

payload = {
    'original': 'data:image/png;base64,' + img_to_b64(orig),
    'mask': 'data:image/png;base64,' + img_to_b64(mask)
}

print('Testing upload_mask endpoint...')
try:
    resp = requests.post('http://127.0.0.1:5000/upload_mask', json=payload, timeout=30)
    print('Status:', resp.status_code)
    print('Content-Type:', resp.headers.get('content-type', 'unknown'))
    
    if resp.headers.get('content-type', '').startswith('image/'):
        print('SUCCESS: Got image response, size:', len(resp.content), 'bytes')
        with open('test_result.png', 'wb') as f:
            f.write(resp.content)
        print('Saved inpainted result to test_result.png')
    else:
        print('Response text:', resp.text)
except Exception as e:
    print('Error:', e)