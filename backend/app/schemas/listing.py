"""İlan uç noktaları için şemalar."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import ListingType


class ListingBase(BaseModel):
    city: str
    district: str
    neighborhood: Optional[str] = None
    m2: float
    room_count: Optional[str] = None
    building_age: Optional[int] = None
    floor: Optional[int] = None
    heating_type: Optional[str] = None
    furnished: bool = False
    has_elevator: bool = False
    has_parking: bool = False
    price_nominal: float
    listing_type: ListingType
    listing_date: datetime


class ListingCreate(ListingBase):
    source_url_hash: Optional[str] = None


class ListingRead(ListingBase):
    id: int
    price_real: Optional[float] = None

    class Config:
        from_attributes = True


class ListingFilter(BaseModel):
    """Liste filtresi query parametreleri."""

    city: Optional[str] = None
    district: Optional[str] = None
    listing_type: Optional[ListingType] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_m2: Optional[float] = None
    max_m2: Optional[float] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaginatedListings(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ListingRead]


class SimilarListing(BaseModel):
    listing: ListingRead
    similarity_score: float
