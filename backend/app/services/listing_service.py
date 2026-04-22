"""İlan CRUD servisi."""

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Listing
from app.schemas.listing import ListingCreate, PaginatedListings


class ListingService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, listing_id: int) -> Optional[Listing]:
        return self.db.query(Listing).filter(Listing.id == listing_id).first()

    def list(
        self,
        city: Optional[str] = None,
        district: Optional[str] = None,
        listing_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedListings:
        q = self.db.query(Listing)
        if city:
            q = q.filter(Listing.city == city)
        if district:
            q = q.filter(Listing.district == district)
        if listing_type:
            q = q.filter(Listing.listing_type == listing_type)
        if min_price is not None:
            q = q.filter(Listing.price_nominal >= min_price)
        if max_price is not None:
            q = q.filter(Listing.price_nominal <= max_price)

        total = q.count()
        items = q.offset((page - 1) * page_size).limit(page_size).all()

        return PaginatedListings(
            total=total,
            page=page,
            page_size=page_size,
            items=items,
        )

    def create(self, payload: ListingCreate) -> Listing:
        listing = Listing(**payload.model_dump())
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing
