"""Scrapy pipeline'ları: tekilleştirme ve DB kaydı."""
import hashlib
import os
from datetime import datetime

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DuplicatesPipeline:
    """Aynı kaynaktan gelen yinelenen ilanları filtreler."""

    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url_hash = adapter.get("source_url_hash")
        if url_hash and url_hash in self.seen:
            raise DropItem(f"Duplicate: {url_hash}")
        if url_hash:
            self.seen.add(url_hash)
        return item


class PostgresPipeline:
    """İlanları PostgreSQL'e kaydeder."""

    def open_spider(self, spider):
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            spider.logger.warning("DATABASE_URL tanımsız — DB pipeline pasif.")
            self.enabled = False
            return
        self.enabled = True
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        if not self.enabled:
            return item
        # Model import burada — scrapy worker'ı açılışta app'i import etmesin diye
        try:
            import sys
            from pathlib import Path
            backend_path = Path(__file__).resolve().parents[2] / "backend"
            if str(backend_path) not in sys.path:
                sys.path.insert(0, str(backend_path))
            from app.db.models import Listing

            session = self.Session()
            data = dict(item)
            data["price_nominal"] = data.pop("price", 0.0)
            data["listing_date"] = data.get("listing_date") or datetime.utcnow()
            listing = Listing(**{k: v for k, v in data.items() if hasattr(Listing, k)})
            session.add(listing)
            session.commit()
            session.close()
        except Exception as e:
            spider.logger.error(f"DB'ye yazılamadı: {e}")
        return item


def url_to_hash(url: str) -> str:
    """Kaynak URL'sinden sabit hash üretir (tekilleştirme için)."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]
