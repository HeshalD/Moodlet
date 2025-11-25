import os
import numpy as np
import joblib
from tqdm import tqdm
from extractors import extract_vggish, get_bpm, get_key, get_loudness

ROOT_DIR = "data/genres"
OUT_FILE = "data/features.joblib"

X = []
y = []
meta = []  # Optional: store bpm/key/loudness for visualization

for genre in os.listdir(ROOT_DIR):
    genre_dir = os.path.join(ROOT_DIR, genre)
    if not os.path.isdir(genre_dir):
        continue
    print(f"Processing genre: {genre}")
    for fname in tqdm(os.listdir(genre_dir)):
        if not fname.lower().endswith(".wav"):
            continue
        path = os.path.join(genre_dir, fname)
        try:
            embedding = extract_vggish(path)
            if embedding is None:
                print("Warning: embedding is None for", path)
                continue
            X.append(embedding)
            y.append(genre)
            meta.append({
                "bpm": get_bpm(path),
                "key": get_key(path),
                "loudness_rms": get_loudness(path)[0],
                "loudness_db": get_loudness(path)[1]
            })
        except Exception as e:
            print("Error processing", path, e)

X = np.vstack(X)
y = np.array(y)
joblib.dump({"X": X, "y": y, "meta": meta}, OUT_FILE)
print("Saved dataset:", OUT_FILE)
