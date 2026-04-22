"""Enflasyon düzeltmesi servisi."""

from datetime import datetime
from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models import EconomicIndicator


class InflationService:
    """CPI/HPI kullanarak nominal <-> reel fiyat dönüşümü."""

    REFERENCE_MONTH = "2025-01"  # Reel fiyat için sabit referans ay

    def __init__(self, db: Session):
        self.db = db

    def get_cpi(self, year_month: str) -> Optional[float]:
        row = (
            self.db.query(EconomicIndicator)
            .filter(EconomicIndicator.year_month == year_month)
            .first()
        )
        return row.cpi if row else None

    def get_latest_cpi(self) -> Optional[float]:
        row = self.db.query(EconomicIndicator).order_by(desc(EconomicIndicator.year_month)).first()
        return row.cpi if row else None

    def nominal_to_real(self, nominal_price: float, listing_date: datetime) -> float:
        """Tarihli nominal fiyatı referans aya indirger."""
        ym = listing_date.strftime("%Y-%m")
        cpi_t = self.get_cpi(ym)
        cpi_ref = self.get_cpi(self.REFERENCE_MONTH)
        if not cpi_t or not cpi_ref:
            return nominal_price  # Veri yoksa nominal'i olduğu gibi döndür
        return nominal_price * cpi_ref / cpi_t

    def real_to_current_nominal(self, real_price: float) -> float:
        """Reel fiyatı güncel aya şişirir."""
        cpi_latest = self.get_latest_cpi()
        cpi_ref = self.get_cpi(self.REFERENCE_MONTH)
        if not cpi_latest or not cpi_ref:
            return real_price
        return real_price * cpi_latest / cpi_ref
