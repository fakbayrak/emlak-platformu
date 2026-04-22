"""Tahmin servisi — ML modelini yükler ve tahmin üretir."""

from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from loguru import logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Prediction
from app.schemas.prediction import HouseFeatures, PredictionResponse, SHAPFeature
from app.services.inflation_service import InflationService


@lru_cache(maxsize=2)
def _load_model(model_type: str):
    """Model, preprocessor ve SHAP explainer'ı belleğe yükler (cache'li)."""
    path_map = {
        "sale": (settings.SALE_MODEL_PATH, settings.SALE_EXPLAINER_PATH),
        "rent": (settings.RENT_MODEL_PATH, settings.RENT_EXPLAINER_PATH),
    }
    model_path, explainer_path = path_map[model_type]

    if not Path(model_path).exists():
        logger.warning(f"Model dosyası bulunamadı: {model_path} — dummy değer dönülecek.")
        return None, None, None

    model = joblib.load(model_path)
    explainer = joblib.load(explainer_path) if Path(explainer_path).exists() else None
    preprocessor = (
        joblib.load(settings.PREPROCESSOR_PATH)
        if Path(settings.PREPROCESSOR_PATH).exists()
        else None
    )
    return model, preprocessor, explainer


class PredictionService:
    """Tahmin işlemlerini yöneten servis."""

    def __init__(self, db: Session, model_type: str):
        self.db = db
        self.model_type = model_type
        self.model, self.preprocessor, self.explainer = _load_model(model_type)
        self.inflation = InflationService(db=db)

    def predict(self, features: HouseFeatures) -> PredictionResponse:
        """Özelliklere göre fiyat tahmini üretir."""
        if self.model is None:
            # Geliştirme aşamasında modeller yoksa placeholder yanıt
            return self._dummy_response(features)

        X = self._features_to_dataframe(features)
        X_processed = self.preprocessor.transform(X) if self.preprocessor else X

        # log1p ile eğitildiyse geri dönüşüm
        pred_log = self.model.predict(X_processed)[0]
        pred_real = float(np.expm1(pred_log))

        # Reel -> nominal (güncel aya enflasyon ile şişir)
        pred_nominal = self.inflation.real_to_current_nominal(pred_real)

        # SHAP açıklaması
        shap_features = self._get_shap_explanation(X_processed) if self.explainer else []

        response = PredictionResponse(
            predicted_price_nominal=round(pred_nominal, 2),
            predicted_price_real=round(pred_real, 2),
            model_version="v1",
            top_shap_features=shap_features,
        )

        # Tahmini veritabanına kaydet
        self._log_prediction(features, response)
        return response

    def _features_to_dataframe(self, features: HouseFeatures) -> pd.DataFrame:
        return pd.DataFrame([features.model_dump()])

    def _get_shap_explanation(self, X_processed) -> list[SHAPFeature]:
        """En önemli 5 SHAP özelliğini TL cinsinden döndürür."""
        shap_values = self.explainer.shap_values(X_processed)[0]
        feature_names = self.preprocessor.get_feature_names_out() if self.preprocessor else []

        # En büyük |shap| değerine sahip 5 özelliği seç
        idx_sorted = np.argsort(np.abs(shap_values))[::-1][:5]
        return [
            SHAPFeature(
                name=str(feature_names[i]) if i < len(feature_names) else f"feature_{i}",
                contribution_tl=float(np.expm1(shap_values[i])),
                direction="+" if shap_values[i] >= 0 else "-",
            )
            for i in idx_sorted
        ]

    def _log_prediction(self, features: HouseFeatures, response: PredictionResponse):
        """Tahmini predictions tablosuna kaydet."""
        try:
            prediction = Prediction(
                input_json=features.model_dump(),
                predicted_price_real=response.predicted_price_real,
                predicted_price_nominal=response.predicted_price_nominal,
                model_version=response.model_version,
                shap_top_features=[f.model_dump() for f in response.top_shap_features],
            )
            self.db.add(prediction)
            self.db.commit()
        except Exception as e:
            logger.error(f"Tahmin kaydedilemedi: {e}")
            self.db.rollback()

    def _dummy_response(self, features: HouseFeatures) -> PredictionResponse:
        """Model henüz eğitilmediğinde placeholder — geliştirme kolaylığı için."""
        base_price = features.m2 * (35000 if self.model_type == "sale" else 250)
        return PredictionResponse(
            predicted_price_nominal=round(base_price, 2),
            predicted_price_real=round(base_price * 0.85, 2),
            model_version="dummy-v0",
            top_shap_features=[
                SHAPFeature(name="m2", contribution_tl=base_price * 0.6, direction="+"),
            ],
        )
