# Image Inpainting (Flask + Canvas)# Image Inpainting UI



Remove unwanted objects from photos by painting a mask. The web UI lets you upload an image, brush over areas to remove, and generate a clean result. Backend uses a TensorFlow/Keras model if available, with an OpenCV fallback.This workspace contains a Jupyter notebook `image-inpainting-pjt.ipynb` and a small Flask frontend to test image inpainting locally.



- Built by Rupam Kumari • MIT LicenseQuick start (Windows PowerShell):

- Frontend: HTML5 Canvas + Vanilla JS

- Backend: Flask, Pillow, NumPy, OpenCV (optional TensorFlow)1.Activate your environment (assuming `.venv` exists in the project root):



## Quick Start (Windows)```powershell

& ./.venv/Scripts/Activate.ps1

```powershell```

# Clone and setup

git clone https://github.com/techietinker01/Image-Inpainting.git2.Install required packages (if not already):

cd Image-Inpainting

```powershell

# Create virtual environmentpip install -r requirements.txt

python -m venv .venv-tf```

.\.venv-tf\Scripts\Activate.ps1

3.Run the Flask app:

# Install dependencies

pip install -r requirements.txt```powershell

python app.py

# Run the app```

python app.py

```4.Open a browser at <http://127.0.0.1:7860/> to use the UI.



Open http://127.0.0.1:5000Notes:

-The backend will try to import `Generator` from `image_inpainting_model.py` and load `generator_weights.h5` if present. If you want the actual trained generator to run, export your model weights to `generator_weights.h5` and add a small `image_inpainting_model.py` file that defines `Generator()` (copy the model code from the notebook into that file).

## Usage-If no generator is found, the server returns the input image as a fallback.


1. **Upload** → Choose an image file
2. **Highlight** → Brush over objects to remove  
3. **Generate** → AI processes the image
4. **Download** → Save the result

## Features

- Drag & drop image upload
- Adjustable brush size and eraser tool
- Touch support for mobile devices
- Real-time status detection (TensorFlow/OpenCV)
- Clean, responsive UI

## API Endpoints

- `GET /` → Web interface
- `POST /upload_mask` → Process image (returns PNG)
- `GET /api/status` → Server status
- `GET /about` → App metadata

## Tech Stack

- **Frontend**: HTML5 Canvas, Vanilla JavaScript, CSS
- **Backend**: Flask, Pillow, NumPy, OpenCV
- **Optional**: TensorFlow/Keras for advanced inpainting

## License

MIT License - see [LICENSE](LICENSE) file