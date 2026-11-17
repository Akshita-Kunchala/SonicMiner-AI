import os
from pathlib import Path
import librosa

SUPPORTED_FORMATS = ["mp3", "wav", "flac", "ogg", "m4a"]


def save_uploaded_files(uploaded_files, upload_dir="uploads"):
    os.makedirs(upload_dir, exist_ok=True)
    saved_files = []
    for file in uploaded_files:
        extension = Path(file.name).suffix.lower().lstrip(".")
        if extension not in SUPPORTED_FORMATS:
            continue
        # Avoid accidental path traversal and collisions.
        safe_name = Path(file.name).name
        path = Path(upload_dir) / safe_name
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        saved_files.append(str(path))
    return saved_files


def get_audio_metadata(file_path):
    y_mono, sr = librosa.load(file_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y_mono, sr=sr)
    try:
        y_stereo, _ = librosa.load(file_path, sr=None, mono=False)
        channels = 1 if getattr(y_stereo, "ndim", 1) == 1 else int(y_stereo.shape[0])
    except Exception:
        channels = 1
    return {
        "File Name": os.path.basename(file_path),
        "Sample Rate": int(sr),
        "Duration (sec)": round(float(duration), 2),
        "Channels": channels,
        "File Size (MB)": round(os.path.getsize(file_path) / (1024 * 1024), 2),
    }


def load_audio(file_path, sr=None):
    return librosa.load(file_path, sr=sr, mono=True)
