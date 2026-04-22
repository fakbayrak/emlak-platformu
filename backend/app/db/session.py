"""
SQLAlchemy oturum yönetimi ve Base sınıfı.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.API_DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """SQLAlchemy deklaratif temel sınıf."""

    pass


def get_db():
    """FastAPI dependency — istek başına DB session üretir."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
