"""Model metrik uç noktaları için şemalar."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ModelMetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    model_name: str
    version: str
    mae: float
    rmse: float
    r2: float
    mape: float
    train_size: int
    test_size: int
    training_seconds: Optional[float] = None
    mlflow_run_id: Optional[str] = None
    trained_at: datetime


class ModelMetricsResponse(BaseModel):
    total: int
    metrics: List[ModelMetricRead]
