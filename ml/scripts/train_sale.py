"""Satılık fiyat modelini eğitip MLflow'a kaydeder."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from ml.src.data.cleaner import clip_outliers_iqr, fill_missing, remove_duplicates
from ml.src.data.loader import load_from_db
from ml.src.evaluation.shap_utils import create_tree_explainer
from ml.src.features.builder import build_features, log_transform_target
from ml.src.features.encoders import build_preprocessor
from ml.src.models.trainer import save_model, save_preprocessor, train_and_log

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://emlak:emlak_dev_password@localhost:5432/emlak_db")
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_DIR = Path("ml/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("1) Veri yükleniyor...")
    df = load_from_db(DATABASE_URL, listing_type="sale")
    print(f"   Yüklenen ilan: {len(df)}")

    print("2) Temizleme...")
    df = remove_duplicates(df)
    df = fill_missing(df)
    df = clip_outliers_iqr(df, "price_real", group_by="district")

    print("3) Özellik mühendisliği...")
    df = build_features(df)

    print("4) Train/test bölme (kronolojik)...")
    df = df.sort_values("listing_date")
    split_idx = int(len(df) * 0.85)
    train_df, test_df = df.iloc[:split_idx], df.iloc[split_idx:]

    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(train_df)
    X_test = preprocessor.transform(test_df)
    y_train = log_transform_target(train_df["price_real"])
    y_test = log_transform_target(test_df["price_real"])

    print("5) Model eğitiliyor...")
    from xgboost import XGBRegressor
    model = XGBRegressor(
        n_estimators=500, learning_rate=0.05, max_depth=7,
        subsample=0.8, colsample_bytree=0.8, random_state=42,
    )
    model = train_and_log(
        model, X_train, y_train, X_test, y_test,
        model_name="xgboost_sale",
        experiment_name="emlak_sale",
        tracking_uri=MLFLOW_URI,
    )

    print("6) Artefactlar kaydediliyor...")
    save_model(model, MODEL_DIR / "sale_price_model.pkl")
    save_preprocessor(preprocessor, MODEL_DIR / "preprocessor.pkl")
    create_tree_explainer(model, save_path=str(MODEL_DIR / "sale_shap_explainer.pkl"))

    print("Tamamlandı ✓")


if __name__ == "__main__":
    main()
