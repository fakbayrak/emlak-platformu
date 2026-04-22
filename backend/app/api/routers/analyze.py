"""Fırsat analizi uç noktası (M3)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.prediction import DealAnalysisRequest, DealAnalysisResponse
from app.services.deal_service import DealService

router = APIRouter()


@router.post(
    "/deal", response_model=DealAnalysisResponse, summary="Fırsat / Uygun / Pahalı analizi"
)
def analyze_deal(payload: DealAnalysisRequest, db: Session = Depends(get_db)):
    """Gerçek ilan fiyatını model tahmini ile karşılaştırır."""
    service = DealService(db=db)
    return service.analyze(payload)
