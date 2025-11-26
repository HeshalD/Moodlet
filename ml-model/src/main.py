# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from predict import predict_track  # import the function

app = FastAPI(
    title="Moodlet Audio Analysis API",
    description="Upload audio tracks and get genre, key, BPM, loudness, and mood analysis.",
    version="1.0.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/analyze/", response_class=JSONResponse, summary="Analyze an audio track")
async def analyze(file: UploadFile = File(..., description="Upload a WAV audio file")):
    """
    Accepts an audio file and returns full analysis:
    - Genre (top 5 probabilities)
    - BPM
    - Key
    - Loudness
    - Mood (energy, valence, label)
    """
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = predict_track(str(file_path))
    return result
