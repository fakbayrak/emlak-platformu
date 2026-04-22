"""Özellik mühendisliği."""
import numpy as np
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Türetilmiş özellikleri ekler."""
    df = df.copy()

    # Bina yaş grubu
    df["age_group"] = pd.cut(
        df["building_age"].fillna(0),
        bins=[-1, 0, 5, 15, 30, 100],
        labels=["yeni", "0_5", "5_15", "15_30", "30_plus"],
    )

    # Kat sınıfı
    def floor_class(f):
        if pd.isna(f):
            return "bilinmiyor"
        if f <= 0:
            return "giris_bodrum"
        if f == 1:
            return "zemin_ustu"
        return "ara"
    df["floor_class"] = df["floor"].apply(floor_class)

    # Konfor skoru (0-3)
    df["comfort_score"] = (
        df["has_elevator"].astype(int)
        + df["has_parking"].astype(int)
        + df["furnished"].astype(int)
    )

    # Oda başına m²
    def parse_rooms(s):
        try:
            parts = s.split("+")
            return int(parts[0]) + int(parts[1]) if len(parts) > 1 else int(parts[0])
        except (ValueError, AttributeError):
            return np.nan
    df["total_rooms"] = df["room_count"].apply(parse_rooms)
    df["m2_per_room"] = df["m2"] / df["total_rooms"].replace(0, np.nan)

    # Zaman özellikleri
    df["listing_date"] = pd.to_datetime(df["listing_date"], errors="coerce")
    df["listing_year"] = df["listing_date"].dt.year
    df["listing_month"] = df["listing_date"].dt.month

    return df


def log_transform_target(y: pd.Series) -> pd.Series:
    """log1p dönüşümü."""
    return np.log1p(y)


def inverse_log_transform(y_log: pd.Series) -> pd.Series:
    return np.expm1(y_log)
