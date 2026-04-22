"""İlan listeleme ve benzer ilan uç noktaları (M6)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.listing import (
    ListingCreate,
    ListingRead,
    PaginatedListings,
    SimilarListing,
)
from app.services.listing_service import ListingService
from app.services.recommender_service import RecommenderService

router = APIRouter()


@router.get("", response_model=PaginatedListings, summary="İlanları filtrele")
def list_listings(
    city: str | None = None,
    district: str | None = None,
    listing_type: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = ListingService(db=db)
    return service.list(
        city=city,
        district=district,
        listing_type=listing_type,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size,
    )


@router.get("/{listing_id}", response_model=ListingRead, summary="Tek ilan detayı")
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    service = ListingService(db=db)
    listing = service.get(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="İlan bulunamadı")
    return listing


@router.get("/similar/{listing_id}", response_model=list[SimilarListing], summary="Benzer ilanlar (M6)")
def similar_listings(listing_id: int, limit: int = 10, db: Session = Depends(get_db)):
    service = RecommenderService(db=db)
    return service.find_similar(listing_id=listing_id, limit=limit)


@router.post("", response_model=ListingRead, status_code=201, summary="(Admin) İlan ekle")
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    # TODO: Admin auth kontrolü ekle
    service = ListingService(db=db)
    return service.create(payload)
