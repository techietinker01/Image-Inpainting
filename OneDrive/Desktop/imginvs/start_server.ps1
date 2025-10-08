# Activate virtual environment and start Flask server with TensorFlow warnings suppressed
& ./.venv-tf/Scripts/Activate.ps1
$env:TF_ENABLE_ONEDNN_OPTS="0"
Write-Host "Starting Flask server with TensorFlow warnings suppressed..."
python app.py