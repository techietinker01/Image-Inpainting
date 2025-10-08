import requests
import os
import base64

UPLOADS = os.path.join(os.getcwd(), 'uploads')
OUTS = os.path.join(os.getcwd(), 'outputs')
os.makedirs(OUTS, exist_ok=True)

orig_path = os.path.join(UPLOADS, 'original.png')
mask_path = os.path.join(UPLOADS, 'mask.png')

if not (os.path.exists(orig_path) and os.path.exists(mask_path)):
    print('Please ensure uploads/original.png and uploads/mask.png exist before running this test.')
    raise SystemExit(1)

def to_data_url(path):
    with open(path, 'rb') as f:
        b = f.read()
    import mimetypes
    mtype = mimetypes.guess_type(path)[0] or 'image/png'
    return f'data:{mtype};base64,' + base64.b64encode(b).decode('ascii')

payload = {'original': to_data_url(orig_path), 'mask': to_data_url(mask_path)}

print('Posting to http://127.0.0.1:5000/upload_mask')
res = requests.post('http://127.0.0.1:5000/upload_mask', json=payload)
print('Status:', res.status_code)

ct = res.headers.get('Content-Type','')
if 'image' in ct:
    out_file = os.path.join(OUTS, 'test_response.png')
    with open(out_file, 'wb') as f:
        f.write(res.content)
    print('Wrote image to', out_file)
else:
    out_file = os.path.join(OUTS, 'test_response.json')
    with open(out_file, 'w', encoding='utf8') as f:
        f.write(res.text)
    print('Wrote json to', out_file)
import requests
import base64
from PIL import Image
import io
import json

# create a white 256x256 image and a mask with a black rectangle
img = Image.new('RGB', (256,256), color=(200,200,200))
mask = Image.new('RGB', (256,256), color=(255,255,255))
for x in range(80,176):
    for y in range(60,196):
        mask.putpixel((x,y),(0,0,0))

buf1 = io.BytesIO(); img.save(buf1, format='PNG'); b1 = base64.b64encode(buf1.getvalue()).decode('ascii')
buf2 = io.BytesIO(); mask.save(buf2, format='PNG'); b2 = base64.b64encode(buf2.getvalue()).decode('ascii')

payload = {'image': 'data:image/png;base64,'+b1, 'mask': 'data:image/png;base64,'+b2}

try:
    r = requests.post('http://localhost:7860/inpaint', json=payload, timeout=20)
    print('Status:', r.status_code)
    if r.status_code==200:
        open('tools/test_out.png','wb').write(r.content)
        print('Saved tools/test_out.png')
    else:
        print('Error response:', r.text)
except Exception as e:
    print('Request failed:', e)
