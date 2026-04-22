"""İlçe istatistikleri ve yatırım skoru servisi (M4)."""
from sqlalchemy.orm import Session

from app.db.models import DistrictStats
from app.schemas.analytics import (
    DistrictAnalytics,
    DistrictDetailResponse,
    DistrictListResponse,
    ScoreComponents,
)


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def list_districts(self) -> DistrictListResponse:
        rows = (
            self.db.query(DistrictStats)
            .order_by(DistrictStats.investment_score.desc().nullslast())
            .all()
        )
        districts = [self._row_to_schema(r) for r in rows]
        return DistrictListResponse(total=len(districts), districts=districts)

    def get_district_detail(self, name: str) -> DistrictDetailResponse | None:
        row = (
            self.db.query(DistrictStats)
            .filter(DistrictStats.district == name)
            .first()
        )
        if not row:
            return None

        base = self._row_to_schema(row).model_dump()
        # TODO: price_trend ve rent_trend için ilan verisi üzerinden aylık aggregate
        return DistrictDetailResponse(**base, price_trend=None, rent_trend=None)

    def _row_to_schema(self, row: DistrictStats) -> DistrictAnalytics:
        components = None
        if row.score_components:
            components = ScoreComponents(**row.score_components)
        return DistrictAnalytics(
            district=row.district,
            avg_sale_price_per_m2=row.avg_sale_price_per_m2,
            avg_rent_per_m2=row.avg_rent_per_m2,
            listing_count_90d=row.listing_count_90d,
            price_volatility_90d=row.price_volatility_90d,
            appreciation_12m=row.appreciation_12m,
            investment_score=row.investment_score,
            score_components=components,
            updated_at=row.updated_at,
        )
