"""Tüm site spider'ları için ortak temel sınıf."""
import scrapy

from emlak_scraper.items import ListingItem


class BaseListingSpider(scrapy.Spider):
    """Ortak parse yardımcıları."""

    # Alt sınıflar override etmelidir
    name = "base"
    allowed_domains: list[str] = []
    start_urls: list[str] = []

    def parse(self, response):
        raise NotImplementedError("Alt sınıf parse() metodunu implement etmelidir.")

    def new_item(self) -> ListingItem:
        return ListingItem()

    @staticmethod
    def clean_price(text: str) -> float | None:
        if not text:
            return None
        s = "".join(ch for ch in text if ch.isdigit() or ch == ",")
        s = s.replace(",", "")
        try:
            return float(s)
        except ValueError:
            return None

    @staticmethod
    def clean_int(text: str) -> int | None:
        if not text:
            return None
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else None
