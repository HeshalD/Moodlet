# src/mood_predictor.py
import numpy as np

# Simple rule-based mood determination
# Energy: based on BPM and loudness
# Valence (happiness): based on key (Major = positive, Minor = negative)
# You can later replace this with a trained ML model

MAJOR_KEYS = [
    "C Major","C# Major","D Major","D# Major","E Major","F Major","F# Major",
    "G Major","G# Major","A Major","A# Major","B Major"
]

def determine_mood(bpm, loudness_rms, key):
    """
    Returns energy and valence scores between 0 and 1
    """
    # Normalize BPM (assuming 40-200 bpm)
    energy_bpm = min(max((bpm - 40) / (200 - 40), 0), 1)
    
    # Normalize loudness (RMS)
    # RMS usually between 0.0 - 0.3 for normalized audio
    energy_loudness = min(max(loudness_rms / 0.3, 0), 1)
    
    # Combine to get energy (simple average)
    energy = (energy_bpm + energy_loudness) / 2.0

    # Determine valence (happiness) from key
    if key is None:
        valence = 0.5  # unknown
    else:
        valence = 1.0 if key in MAJOR_KEYS else 0.0

    return {
        "energy": round(energy, 3),
        "valence": round(valence, 3)
    }

# Optional: simple mood label based on energy + valence
def mood_label(energy, valence):
    if energy > 0.6 and valence > 0.5:
        return "Happy / Energetic"
    elif energy > 0.6 and valence <= 0.5:
        return "Angry / Intense"
    elif energy <= 0.6 and valence > 0.5:
        return "Relaxed / Calm"
    else:
        return "Sad / Calm"
