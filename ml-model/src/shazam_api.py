from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shazam_recognizer import ShazamRecognizer
import os
import tempfile
import asyncio
from typing import Dict, Any

app = FastAPI(
    title="Shazam API",
    description="A simple API for song recognition using Shazam",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recognizer = ShazamRecognizer()

@app.post("/recognize", response_model=Dict[str, Any])
async def recognize_audio(file: UploadFile = File(...)):
    """
    Recognize a song from an uploaded audio file.
    
    Supports common audio formats like MP3, WAV, M4A, etc.
    Maximum file size: 10MB
    """
    # Check file size (max 10MB)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    # Check file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.mp3', '.wav', '.m4a', '.ogg', '.flac']:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Reset file pointer
    await file.seek(0)
    
    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Recognize the song
            result = await recognizer.recognize_audio_file(temp_file_path)
            
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
            if not result['success']:
                raise HTTPException(status_code=404, detail=result.get('error', 'Song not recognized'))
                
            return {
                "status": "success",
                "data": result['track']
            }
            
        except Exception as e:
            # Clean up the temporary file in case of error
            try:
                os.unlink(temp_file_path)
            except:
                pass
            raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error handling file: {str(e)}")

@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Shazam API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("shazam_api:app", host="0.0.0.0", port=8000, reload=True)