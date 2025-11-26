
import joblib
from extractors import analyze_all
from mood_predictor import determine_mood, mood_label
import numpy as np

# Load genre model once globally
GENRE_MODEL = joblib.load("../models/genre_classifier.joblib")

def predict_track(path):
    """
    Full analysis: genre, BPM, key, loudness, mood
    """
    analysis = analyze_all(path)
    
    # Genre prediction
    import numpy as np
    emb = np.array(analysis["embedding"]).reshape(1, -1)  # Convert list back to numpy array
    genre = GENRE_MODEL.predict(emb)[0]
    probs = GENRE_MODEL.predict_proba(emb)[0]
    classes = GENRE_MODEL.classes_
    top_probs = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:5]
    
    # Mood prediction
    mood = determine_mood(
        bpm=analysis["bpm"],
        loudness_rms=analysis["loudness_rms"],
        key=analysis["key"]
    )
    label = mood_label(mood["energy"], mood["valence"])
    
    return {
        "genre": genre,
        "top_probabilities": {c: float(p) for c, p in top_probs},
        "bpm": analysis["bpm"],
        "key": analysis["key"],
        "loudness_rms": analysis["loudness_rms"],
        "loudness_db": analysis["loudness_db"],
        "mood": {
            "energy": mood["energy"],
            "valence": mood["valence"],
            "label": label
        }
    }
