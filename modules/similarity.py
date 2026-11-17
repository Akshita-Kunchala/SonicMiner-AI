import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from modules.feature_extractor import DEFAULT_FEATURES, feature_vector


def _matrix(analyses):
    names = [k for k in DEFAULT_FEATURES if all(k in a["features"] for a in analyses)]
    X = np.vstack([feature_vector(a, names) for a in analyses])
    return X, names


def handcrafted_similarity(a, b, scaler=None, feature_names=None):
    names = feature_names or DEFAULT_FEATURES
    X = np.vstack([feature_vector(a, names), feature_vector(b, names)])
    Xs = scaler.transform(X) if scaler is not None else StandardScaler().fit_transform(X)
    distance = float(np.linalg.norm(Xs[0] - Xs[1]) / max(np.sqrt(Xs.shape[1]), 1.0))
    return float(100.0 * np.exp(-0.5 * distance))


def learned_representation(analyses):
    """Unsupervised learned representation over the uploaded audio feature space.

    PCA is intentionally transparent and lightweight: it learns the dominant
    structure of the current audio collection without downloading a giant model.
    For collections with >= 2 files it provides a data-driven representation
    that can be fused with the acoustic baseline.
    """
    X, names = _matrix(analyses)
    X_scaled = StandardScaler().fit_transform(X)
    n_components = max(1, min(8, X_scaled.shape[0] - 1, X_scaled.shape[1]))
    pca = PCA(n_components=n_components, random_state=42)
    Z = pca.fit_transform(X_scaled)
    return Z, pca, names


def hybrid_similarity(analyses):
    if len(analyses) < 2:
        return [], None
    Z, pca, names = learned_representation(analyses)
    scaler = StandardScaler().fit(np.vstack([feature_vector(a, names) for a in analyses]))
    result = []
    for i in range(len(analyses)):
        for j in range(i + 1, len(analyses)):
            acoustic = handcrafted_similarity(analyses[i], analyses[j], scaler=scaler, feature_names=names)
            # Data-driven representation similarity. Unlike a raw cosine score,
            # this remains meaningful for small collections (including two files).
            distance = float(np.linalg.norm(Z[i] - Z[j]) / max(np.sqrt(Z.shape[1]), 1.0))
            learned = float(100.0 * np.exp(-0.5 * distance))
            overall = 0.4 * acoustic + 0.6 * learned
            result.append({
                "a": i, "b": j,
                "acoustic": acoustic,
                "learned": learned,
                "overall": overall,
            })
    return result, pca
