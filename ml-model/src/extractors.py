# src/extractors.py
import numpy as np
import librosa
import tensorflow_hub as hub
from collections import Counter
import crema
from pymusickit.key_finder import KeyFinder

from scipy.signal import windows

def frame_signal(signal, frame_size, hop_size):
    w = windows.hann(frame_size, sym=True)  # Hann window
    frames = []
    for i in range(0, len(signal) - frame_size + 1, hop_size):
        frames.append(signal[i:i+frame_size] * w)
    return np.array(frames)

# Load VGGish once (slow)
VGGISH_URL = "https://tfhub.dev/google/vggish/1"
print("Loading VGGish model... (may take a few seconds)")
vggish_model = hub.load(VGGISH_URL)

def get_vggish_embedding_from_wave(y, sr=16000):
    """
    Accepts waveform y (np.float32) resampled to 16000 Hz and returns mean 128D embedding.
    """
    if sr != 16000:
        raise ValueError("VGGish requires 16kHz input. Resample before calling.")
    # The model expects a 1D float32 array
    emb = vggish_model(y).numpy()   # shape (T, 128)
    return np.mean(emb, axis=0)     # collapse to single 128-d vector

def extract_vggish(path):
    y, sr = librosa.load(path, sr=16000, mono=True)
    y = y.astype(np.float32)
    return get_vggish_embedding_from_wave(y, sr)

def get_bpm(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    return float(tempo)

KEYS = [
    "C Major","C# Major","D Major","D# Major","E Major","F Major","F# Major",
    "G Major","G# Major","A Major","A# Major","B Major",
    "C Minor","C# Minor","D Minor","D# Minor","E Minor","F Minor","F# Minor",
    "G Minor","G# Minor","A Minor","A# Minor","B Minor"
]

def get_key(audio_path, t_start=None, t_end=None):
    """
    Detects the musical key of an audio file using PyMusicKit.
    Optionally, you can provide t_start and t_end (in seconds) for segment-based analysis.
    Returns: key as string, e.g. "C major" or "A minor".
    """
    try:
        # If you want to analyze the whole track:
        if t_start is None and t_end is None:
            song = KeyFinder(audio_path)
        else:
            song = KeyFinder(audio_path, t_start=t_start, t_end=t_end)
        return song.key_primary  # Changed from get_key() to key_primary
    except Exception as e:
        print(f"[get_key] error on {audio_path}: {e}")
        return None

        
def get_loudness(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    rms = librosa.feature.rms(y=y)[0]
    loudness = float(np.mean(rms))
    loudness_db = float(librosa.amplitude_to_db([loudness], ref=1.0)[0])
    return loudness, loudness_db

def analyze_all(path):
    return {
        "embedding": extract_vggish(path),
        "bpm": get_bpm(path),
        "key": get_key(path),
        "loudness_rms": get_loudness(path)[0],
        "loudness_db": get_loudness(path)[1]
    }
