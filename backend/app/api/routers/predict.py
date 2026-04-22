"""Satılık ve kiralık fiyat tahmin uç noktaları (M1, M2)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.prediction import HouseFeatures, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter()


@router.post("/sale", response_model=PredictionResponse, summary="Satılık fiyat tahmini")
def predict_sale(features: HouseFeatures, db: Session = Depends(get_db)):
    """Ev özelliklerini alır, tahmini satış fiyatı ve SHAP açıklaması döndürür."""
    service = PredictionService(db=db, model_type="sale")
    return service.predict(features)


@router.post("/rent", response_model=PredictionResponse, summary="Kiralık fiyat tahmini")
def predict_rent(features: HouseFeatures, db: Session = Depends(get_db)):
    """Ev özelliklerini alır, tahmini aylık kira ve SHAP açıklaması döndürür."""
    service = PredictionService(db=db, model_type="rent")
    return service.predict(features)
