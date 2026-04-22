"""Model performans metrikleri uç noktası (M7)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.model import ModelMetricsResponse
from app.services.model_service import ModelService

router = APIRouter()


@router.get("/metrics", response_model=ModelMetricsResponse, summary="Tüm modellerin metrikleri")
def get_metrics(db: Session = Depends(get_db)):
    service = ModelService(db=db)
    return service.list_metrics()
