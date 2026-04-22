"""Model metrik servisi (M7)."""

from sqlalchemy.orm import Session

from app.db.models import ModelMetric
from app.schemas.model import ModelMetricsResponse


class ModelService:
    def __init__(self, db: Session):
        self.db = db

    def list_metrics(self) -> ModelMetricsResponse:
        rows = self.db.query(ModelMetric).order_by(ModelMetric.trained_at.desc()).all()
        return ModelMetricsResponse(total=len(rows), metrics=rows)
