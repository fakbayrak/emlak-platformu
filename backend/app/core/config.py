"""
Uygulama yapılandırması.
Pydantic Settings ile .env dosyasından ortam değişkenlerini yükler.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ortam değişkenleri ve uygulama ayarları."""

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True
    API_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # Veritabanı
    DATABASE_URL: str = "postgresql+psycopg2://emlak:emlak_dev_password@localhost:5432/emlak_db"

    # JWT
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "emlak_tahmin"

    # Model dosya yolları
    SALE_MODEL_PATH: str = "../ml/models/sale_price_model.pkl"
    RENT_MODEL_PATH: str = "../ml/models/rent_price_model.pkl"
    SALE_EXPLAINER_PATH: str = "../ml/models/sale_shap_explainer.pkl"
    RENT_EXPLAINER_PATH: str = "../ml/models/rent_shap_explainer.pkl"
    PREPROCESSOR_PATH: str = "../ml/models/preprocessor.pkl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
