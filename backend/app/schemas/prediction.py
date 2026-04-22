"""Tahmin uç noktaları için Pydantic şemaları."""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import DealLabel


class HouseFeatures(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    """Konut özellikleri (tahmin girdisi)."""
    city: str = Field(..., examples=["İstanbul"])
    district: str = Field(..., examples=["Kadıköy"])
    neighborhood: Optional[str] = Field(None, examples=["Caddebostan"])
    m2: float = Field(..., gt=0, lt=1000, examples=[120])
    room_count: str = Field(..., examples=["3+1"])
    building_age: Optional[int] = Field(None, ge=0, le=100, examples=[10])
    floor: Optional[int] = Field(None, ge=-3, le=60, examples=[3])
    heating_type: Optional[str] = Field(None, examples=["kombi"])
    furnished: bool = False
    has_elevator: bool = True
    has_parking: bool = False


class SHAPFeature(BaseModel):
    """Tek bir özelliğin SHAP katkısı."""
    name: str
    contribution_tl: float
    direction: str  # "+" veya "-"


class PredictionResponse(BaseModel):
    """Tahmin yanıtı."""
    model_config = ConfigDict(protected_namespaces=())

    predicted_price_nominal: float = Field(..., description="Güncel aya enflasyonla şişirilmiş fiyat (TL)")
    predicted_price_real: float = Field(..., description="Reel (deflate edilmiş) fiyat (TL)")
    confidence_interval: Optional[List[float]] = Field(None, description="[alt, üst] tahmin bandı")
    model_version: str
    top_shap_features: List[SHAPFeature]
    currency: str = "TRY"


class DealAnalysisRequest(BaseModel):
    """Fırsat analizi isteği."""
    features: HouseFeatures
    asking_price: float = Field(..., gt=0, description="İlandaki gerçek fiyat (TL)")


class DealAnalysisResponse(BaseModel):
    """Fırsat analizi yanıtı."""
    label: DealLabel
    predicted_price: float
    asking_price: float
    deviation_pct: float = Field(..., description="(asking - predicted) / predicted * 100")
    explanation: str
