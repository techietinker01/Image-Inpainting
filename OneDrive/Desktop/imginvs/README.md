# Image Inpainting Web Application

Remove unwanted objects from photos by painting a mask. The web UI lets you upload an image, brush over areas to remove, and generate a clean result. Backend uses a TensorFlow/Keras model if available, with an OpenCV fallback.

**Built by Rupam Kumari**  MIT License

## Quick Start

```powershell
git clone https://github.com/techietinker01/Image-Inpainting.git
cd Image-Inpainting

python -m venv .venv-tf
.\.venv-tf\Scripts\Activate.ps1

pip install -r requirements.txt

python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage

1. **Upload**  Choose an image file
2. **Highlight**  Brush over objects to remove
3. **Generate**  AI processes the image
4. **Download**  Save the result

## Features

- Drag & drop image upload
- Adjustable brush size and eraser tool
- Touch support for mobile devices
- Real-time status detection (TensorFlow/OpenCV)
- Clean, responsive UI

## API Endpoints

- GET /  Web interface
- POST /upload_mask  Process image (returns PNG)
- GET /api/status  Server status
- GET /about  App metadata

## Tech Stack

- **Frontend**: HTML5 Canvas, Vanilla JavaScript, CSS
- **Backend**: Flask, Pillow, NumPy, OpenCV
- **Optional**: TensorFlow/Keras for advanced inpainting

## License

MIT License - see [LICENSE](LICENSE) file
