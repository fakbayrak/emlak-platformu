"""Veritabanındaki tüm ilanlar için benzerlik matrisini hesaplayıp similar_cache tablosuna yazar."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from ml.src.data.loader import load_from_db
from ml.src.features.builder import build_features
from ml.src.recommender.similar import compute_similarity_matrix, top_k_similar

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
TOP_K = 20


def main():
    print("İlanlar çekiliyor...")
    df = load_from_db(DATABASE_URL)
    df = build_features(df)
    print(f"Matris hesaplanıyor ({len(df)}×{len(df)})...")
    sim = compute_similarity_matrix(df)

    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM similar_cache"))
        for pos, listing_id in enumerate(df["id"].values):
            top = top_k_similar(sim, pos, k=TOP_K)
            ids = [t[0] for t in top]
            scores = [t[1] for t in top]
            conn.execute(text(
                "INSERT INTO similar_cache (listing_id, similar_ids, similarity_scores, computed_at) "
                "VALUES (:lid, :ids, :scores, NOW())"
            ), {"lid": int(listing_id), "ids": json.dumps(ids), "scores": json.dumps(scores)})
    print("Similarity cache güncellendi ✓")


if __name__ == "__main__":
    main()
