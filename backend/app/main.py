"""
Emlak Platformu — FastAPI uygulaması
Ana giriş noktası.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.routers import (
    analytics,
    analyze,
    health,
    listings,
    model,
    predict,
)
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış olayları."""
    logger.info("Emlak Platformu API başlıyor...")
    # TODO: Model dosyalarını belleğe yükle
    # TODO: APScheduler başlat (nightly district_stats job)
    yield
    logger.info("Emlak Platformu API kapanıyor...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Akıllı Emlak Fiyat Tahmin ve Analiz Platformu",
        description="Türkiye konut piyasası için ML tabanlı tahmin, fırsat ve yatırım analizi API'si.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.API_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Router kayıtları
    app.include_router(health.router, tags=["Sağlık"])
    app.include_router(predict.router, prefix="/predict", tags=["Tahmin"])
    app.include_router(analyze.router, prefix="/analyze", tags=["Analiz"])
    app.include_router(analytics.router, prefix="/analytics", tags=["Analitik"])
    app.include_router(listings.router, prefix="/listings", tags=["İlanlar"])
    app.include_router(model.router, prefix="/model", tags=["Model"])

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG,
    )
