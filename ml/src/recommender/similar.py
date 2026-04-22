"""Cosine similarity ile benzer ilan öneri sistemi (M6)."""
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

SIMILARITY_FEATURES = ["m2", "total_rooms", "building_age", "floor", "comfort_score"]


def compute_similarity_matrix(df: pd.DataFrame,
                              feature_cols: list[str] | None = None) -> np.ndarray:
    """Normalize edilmiş özellik vektörleri üzerinden cosine similarity matrisi üretir."""
    cols = feature_cols or SIMILARITY_FEATURES
    X = df[cols].fillna(df[cols].median())
    X_scaled = StandardScaler().fit_transform(X)
    return cosine_similarity(X_scaled)


def top_k_similar(sim_matrix: np.ndarray, idx: int, k: int = 10) -> list[tuple[int, float]]:
    """Belirli bir satıra en benzer k komşuyu döndürür (kendisi hariç)."""
    scores = sim_matrix[idx]
    order = np.argsort(scores)[::-1]
    order = order[order != idx][:k]
    return [(int(i), float(scores[i])) for i in order]
