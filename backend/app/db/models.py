"""
SQLAlchemy ORM modelleri.
Veritabanı şeması ve proje raporunda tanımlanan tablolar.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Listing(Base):
    """Konut ilanı."""

    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(64), index=True)
    district: Mapped[str] = mapped_column(String(64), index=True)
    neighborhood: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    m2: Mapped[float] = mapped_column(Float)
    room_count: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # "3+1" gibi
    building_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    floor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    heating_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    furnished: Mapped[bool] = mapped_column(Boolean, default=False)
    has_elevator: Mapped[bool] = mapped_column(Boolean, default=False)
    has_parking: Mapped[bool] = mapped_column(Boolean, default=False)
    price_nominal: Mapped[float] = mapped_column(Float)
    price_real: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    listing_type: Mapped[str] = mapped_column(String(16))  # "sale" | "rent"
    listing_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    source_url_hash: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    price_history: Mapped[list["PriceHistory"]] = relationship(back_populates="listing")


class PriceHistory(Base):
    """İlan fiyat geçmişi (fiyat değişiklikleri)."""

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    price_nominal: Mapped[float] = mapped_column(Float)
    price_real: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime)

    listing: Mapped["Listing"] = relationship(back_populates="price_history")


class EconomicIndicator(Base):
    """Aylık ekonomik göstergeler (TÜFE, KFE, USD/TRY, faiz)."""

    __tablename__ = "economic_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year_month: Mapped[str] = mapped_column(String(7), unique=True)  # "2025-01"
    cpi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hpi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    usd_try: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    interest_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class Prediction(Base):
    """Kullanıcıya döndürülen tahminlerin kaydı."""

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    input_json: Mapped[dict] = mapped_column(JSON)
    predicted_price_real: Mapped[float] = mapped_column(Float)
    predicted_price_nominal: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(64))
    deal_label: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    deal_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    shap_top_features: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class DistrictStats(Base):
    """İlçe bazlı özet istatistikler ve yatırım skoru (nightly job ile güncellenir)."""

    __tablename__ = "district_stats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    district: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    avg_sale_price_per_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_rent_per_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    listing_count_90d: Mapped[int] = mapped_column(Integer, default=0)
    price_volatility_90d: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    appreciation_12m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    investment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    score_components: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class ModelMetric(Base):
    """ML model performans kayıtları (MLflow'a paralel özet)."""

    __tablename__ = "model_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(64))
    version: Mapped[str] = mapped_column(String(32))
    mae: Mapped[float] = mapped_column(Float)
    rmse: Mapped[float] = mapped_column(Float)
    r2: Mapped[float] = mapped_column(Float)
    mape: Mapped[float] = mapped_column(Float)
    train_size: Mapped[int] = mapped_column(Integer)
    test_size: Mapped[int] = mapped_column(Integer)
    training_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    mlflow_run_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trained_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class SimilarCache(Base):
    """Benzer ilan öneri önbelleği."""

    __tablename__ = "similar_cache"

    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), primary_key=True)
    similar_ids: Mapped[list] = mapped_column(JSON)  # [id1, id2, ...]
    similarity_scores: Mapped[list] = mapped_column(JSON)  # [0.92, 0.88, ...]
    computed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
