"""Ham veri okuma ve veritabanından yükleme."""
from pathlib import Path
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine


def load_raw_csv(path: str | Path) -> pd.DataFrame:
    """Ham CSV dosyasını okur."""
    return pd.read_csv(path, encoding="utf-8")


def load_from_db(database_url: str, listing_type: Optional[str] = None) -> pd.DataFrame:
    """Veritabanından ilanları DataFrame olarak çeker."""
    engine = create_engine(database_url)
    query = "SELECT * FROM listings"
    if listing_type:
        query += f" WHERE listing_type = '{listing_type}'"
    return pd.read_sql(query, engine)
