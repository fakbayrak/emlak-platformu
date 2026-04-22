"""Benzer ilan öneri servisi (M6)."""
from typing import List

from sqlalchemy.orm import Session

from app.db.models import Listing, SimilarCache
from app.schemas.listing import ListingRead, SimilarListing


class RecommenderService:
    def __init__(self, db: Session):
        self.db = db

    def find_similar(self, listing_id: int, limit: int = 10) -> List[SimilarListing]:
        """Cache'den benzer ilanları getirir; cache yoksa boş liste döner."""
        cache = (
            self.db.query(SimilarCache)
            .filter(SimilarCache.listing_id == listing_id)
            .first()
        )
        if not cache:
            return []

        results: List[SimilarListing] = []
        for sim_id, score in zip(cache.similar_ids[:limit], cache.similarity_scores[:limit]):
            listing = self.db.query(Listing).filter(Listing.id == sim_id).first()
            if listing:
                results.append(
                    SimilarListing(
                        listing=ListingRead.model_validate(listing),
                        similarity_score=float(score),
                    )
                )
        return results
