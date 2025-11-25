# src/predict.py
import sys
import joblib
from extractors import analyze_all
import numpy as np

def predict(path):
    print("Analyzing", path)
    analysis = analyze_all(path)
    emb = analysis["embedding"].reshape(1, -1)
    clf = joblib.load("models/genre_classifier.joblib")
    genre = clf.predict(emb)[0]
    probs = clf.predict_proba(emb)[0]
    classes = clf.classes_
    print("Predicted genre:", genre)
    print("Top probabilities:")
    for c, p in sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {c}: {p:.3f}")
    print("BPM:", analysis["bpm"])
    print("Key:", analysis["key"])
    print("Loudness (RMS, dB):", analysis["loudness_rms"], analysis["loudness_db"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/predict.py path/to/song.wav")
        sys.exit(1)
    predict(sys.argv[1])
