import base64
import requests
from PIL import Image, ImageDraw
import os

os.makedirs('uploads', exist_ok=True)
# Create original image
orig = Image.new('RGB', (300,300), color=(70,130,180))
d = ImageDraw.Draw(orig)
d.rectangle([50,50,250,250], outline=(255,255,255), width=5)
orig.save('uploads/original.png')

# Create mask image (white bg, black strokes)
mask = Image.new('RGB', (300,300), color=(255,255,255))
dm = ImageDraw.Draw(mask)
dm.line((20,20,280,280), fill=(0,0,0), width=15)
dm.ellipse((100,50,200,150), fill=(0,0,0))
mask.save('uploads/mask.png')

# Prepare base64 payload
with open('uploads/original.png', 'rb') as f:
    orig_b = base64.b64encode(f.read()).decode('ascii')
with open('uploads/mask.png', 'rb') as f:
    mask_b = base64.b64encode(f.read()).decode('ascii')

payload = {'original': 'data:image/png;base64,' + orig_b, 'mask': 'data:image/png;base64,' + mask_b}

print('Posting to /upload_mask ...')
resp = requests.post('http://127.0.0.1:5000/upload_mask', json=payload, timeout=10)
print('status', resp.status_code)
out_dir = 'outputs'
os.makedirs(out_dir, exist_ok=True)

# Try to save image response; otherwise print JSON/text for debugging
ct = resp.headers.get('Content-Type', '')
if resp.status_code == 200 and ('image/png' in ct or resp.content[:8] == b'\x89PNG\r\n\x1a\n'):
    out_path = os.path.join(out_dir, 'api_result.png')
    with open(out_path, 'wb') as f:
        f.write(resp.content)
    print('saved image to:', os.path.abspath(out_path), f'({os.path.getsize(out_path)} bytes)')
else:
    try:
        print('json:', resp.json())
    except Exception:
        # Fall back to raw text (may be binary/gibberish if content-type misreported)
        print('resp text:', resp.text)

print('\nuploads dir now:')
print(os.listdir('uploads'))

print('\noutputs dir:')
print(os.listdir('outputs') if os.path.exists('outputs') else 'no outputs')
