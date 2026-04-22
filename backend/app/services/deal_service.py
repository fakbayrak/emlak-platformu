"""Fırsat/uygun/pahalı analiz servisi (M3)."""

from sqlalchemy.orm import Session

from app.schemas.common import DealLabel
from app.schemas.prediction import DealAnalysisRequest, DealAnalysisResponse
from app.services.prediction_service import PredictionService


class DealService:
    """İlan fiyatını model tahmini ile karşılaştırır."""

    BARGAIN_THRESHOLD = -0.10  # Gerçek fiyat tahmin - %10'dan düşükse fırsat
    EXPENSIVE_THRESHOLD = 0.10  # Gerçek fiyat tahmin + %10'dan yüksekse pahalı

    def __init__(self, db: Session):
        self.db = db

    def analyze(self, payload: DealAnalysisRequest) -> DealAnalysisResponse:
        # Model türünü (sale/rent) listing_type'tan al; basit varsayım: varsayılan sale
        # Gerçek uygulamada payload'a listing_type eklenebilir
        predictor = PredictionService(db=self.db, model_type="sale")
        pred = predictor.predict(payload.features)

        predicted = pred.predicted_price_nominal
        asking = payload.asking_price
        deviation = (asking - predicted) / predicted

        if deviation <= self.BARGAIN_THRESHOLD:
            label = DealLabel.BARGAIN
            explanation = (
                f"İlan fiyatı tahminin %{abs(deviation)*100:.1f} altında. Bu bir fırsat olabilir."
            )
        elif deviation >= self.EXPENSIVE_THRESHOLD:
            label = DealLabel.EXPENSIVE
            explanation = (
                f"İlan fiyatı tahminin %{deviation*100:.1f} üzerinde. Pazarlık yapılabilir."
            )
        else:
            label = DealLabel.FAIR
            explanation = (
                f"İlan fiyatı tahmine yakın (sapma %{deviation*100:.1f}). Makul görünüyor."
            )

        return DealAnalysisResponse(
            label=label,
            predicted_price=predicted,
            asking_price=asking,
            deviation_pct=round(deviation * 100, 2),
            explanation=explanation,
        )
