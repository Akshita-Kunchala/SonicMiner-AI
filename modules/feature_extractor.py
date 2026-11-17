import librosa
import numpy as np

FEATURE_GROUPS = {
    "Core": ["RMS Energy", "Zero Crossing Rate", "Spectral Centroid", "Spectral Bandwidth", "Spectral Rolloff", "Spectral Flatness"],
    "MFCC": [f"MFCC {i}" for i in range(1, 14)],
    "Chroma": [f"Chroma {i}" for i in range(1, 13)],
    "Spectral Contrast": [f"Contrast {i}" for i in range(1, 8)],
    "Rhythm": ["Tempo"],
}

DEFAULT_FEATURES = list(FEATURE_GROUPS["Core"] + FEATURE_GROUPS["MFCC"] + FEATURE_GROUPS["Chroma"] + FEATURE_GROUPS["Spectral Contrast"] + FEATURE_GROUPS["Rhythm"])


def _safe_mean(x):
    return float(np.nan_to_num(np.mean(x)))


def extract_audio_analysis(file_path, n_mfcc=13):
    y, sr = librosa.load(file_path, sr=None, mono=True)
    if y.size == 0:
        raise ValueError("The audio file contains no readable samples.")

    hop = 512
    features = {}
    features["Duration"] = float(librosa.get_duration(y=y, sr=sr))
    features["Sample Rate"] = int(sr)

    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop)[0]
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=hop)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=hop)[0]
    flatness = librosa.feature.spectral_flatness(y=y, hop_length=hop)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, hop_length=hop)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, hop_length=hop)
    tempo = librosa.feature.tempo(y=y, sr=sr, hop_length=hop)

    scalar_series = {
        "RMS Energy": rms,
        "Zero Crossing Rate": zcr,
        "Spectral Centroid": centroid,
        "Spectral Bandwidth": bandwidth,
        "Spectral Rolloff": rolloff,
        "Spectral Flatness": flatness,
    }
    for name, arr in scalar_series.items():
        features[name] = _safe_mean(arr)

    for i in range(n_mfcc):
        features[f"MFCC {i+1}"] = _safe_mean(mfcc[i])
    for i in range(chroma.shape[0]):
        features[f"Chroma {i+1}"] = _safe_mean(chroma[i])
    for i in range(contrast.shape[0]):
        features[f"Contrast {i+1}"] = _safe_mean(contrast[i])

    features["Tempo"] = float(np.nan_to_num(np.mean(tempo))) if tempo.size else 0.0

    series = {
        "time": librosa.times_like(rms, sr=sr, hop_length=hop),
        "waveform": y,
        "rms": rms,
        "zcr": zcr,
        "centroid": centroid,
        "bandwidth": bandwidth,
        "rolloff": rolloff,
        "flatness": flatness,
        "mfcc": mfcc,
        "chroma": chroma,
        "contrast": contrast,
    }

    return {
        "file_path": file_path,
        "sample_rate": int(sr),
        "features": features,
        "series": series,
    }


def extract_features(file_path):
    return extract_audio_analysis(file_path)["features"]


def feature_vector(analysis, selected_features=None):
    data = analysis["features"]
    selected = selected_features or [k for k in DEFAULT_FEATURES if k in data]
    return np.array([float(data.get(k, 0.0)) for k in selected], dtype=np.float32)
