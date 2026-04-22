"""Analitik uç noktaları için Pydantic şemaları."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class ScoreComponents(BaseModel):
    """Yatırım skoru bileşenleri."""

    yield_score: float
    stability_score: float
    liquidity_score: float
    appreciation_score: float
    affordability_score: float


class DistrictAnalytics(BaseModel):
    """İlçe özet analizi."""

    district: str
    avg_sale_price_per_m2: Optional[float]
    avg_rent_per_m2: Optional[float]
    listing_count_90d: int
    price_volatility_90d: Optional[float]
    appreciation_12m: Optional[float]
    investment_score: Optional[float]
    score_components: Optional[ScoreComponents] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class DistrictListResponse(BaseModel):
    """Tüm ilçelerin özet listesi."""

    total: int
    districts: List[DistrictAnalytics]


class DistrictDetailResponse(DistrictAnalytics):
    """İlçe detay — ek olarak trend verileri."""

    price_trend: Optional[List[Dict]] = None  # [{"month": "2025-01", "avg_price_per_m2": 35000}]
    rent_trend: Optional[List[Dict]] = None
