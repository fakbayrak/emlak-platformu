"""Kiralık fiyat modelini eğitir (train_sale.py'nin listing_type='rent' varyantı)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split  # noqa: F401

from ml.src.data.cleaner import clip_outliers_iqr, fill_missing, remove_duplicates
from ml.src.data.loader import load_from_db
from ml.src.evaluation.shap_utils import create_tree_explainer
from ml.src.features.builder import build_features, log_transform_target
from ml.src.features.encoders import build_preprocessor
from ml.src.models.trainer import save_model, save_preprocessor, train_and_log

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_DIR = Path("ml/models")


def main():
    print("Kiralık model eğitimi başlıyor...")
    df = load_from_db(DATABASE_URL, listing_type="rent")
    df = remove_duplicates(df)
    df = fill_missing(df)
    df = clip_outliers_iqr(df, "price_real", group_by="district")
    df = build_features(df)

    df = df.sort_values("listing_date")
    split_idx = int(len(df) * 0.85)
    train_df, test_df = df.iloc[:split_idx], df.iloc[split_idx:]

    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(train_df)
    X_test = preprocessor.transform(test_df)
    y_train = log_transform_target(train_df["price_real"])
    y_test = log_transform_target(test_df["price_real"])

    from lightgbm import LGBMRegressor
    model = LGBMRegressor(
        n_estimators=500, learning_rate=0.05, max_depth=7,
        subsample=0.8, colsample_bytree=0.8, random_state=42,
    )
    model = train_and_log(
        model, X_train, y_train, X_test, y_test,
        model_name="lightgbm_rent",
        experiment_name="emlak_rent",
        tracking_uri=MLFLOW_URI,
    )
    save_model(model, MODEL_DIR / "rent_price_model.pkl")
    create_tree_explainer(model, save_path=str(MODEL_DIR / "rent_shap_explainer.pkl"))
    print("Kiralık model tamam ✓")


if __name__ == "__main__":
    main()
