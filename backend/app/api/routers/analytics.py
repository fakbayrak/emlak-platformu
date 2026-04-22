"""Yatırım dashboard uç noktaları (M4)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.analytics import DistrictDetailResponse, DistrictListResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/districts", response_model=DistrictListResponse, summary="Tüm ilçeler — yatırım skorlu")
def list_districts(db: Session = Depends(get_db)):
    service = AnalyticsService(db=db)
    return service.list_districts()


@router.get("/district/{district_name}", response_model=DistrictDetailResponse, summary="İlçe detay")
def get_district(district_name: str, db: Session = Depends(get_db)):
    service = AnalyticsService(db=db)
    district = service.get_district_detail(district_name)
    if not district:
        raise HTTPException(status_code=404, detail=f"İlçe bulunamadı: {district_name}")
    return district
