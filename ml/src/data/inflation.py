"""Enflasyon düzeltmesi — nominal <-> reel fiyat dönüşümü."""
import pandas as pd


def deflate_prices(df: pd.DataFrame, cpi_series: pd.Series,
                   reference_ym: str = "2025-01",
                   price_col: str = "price_nominal",
                   date_col: str = "listing_date") -> pd.DataFrame:
    """Nominal fiyatları referans aya indirger.

    Args:
        df: İlan verisi.
        cpi_series: index = "YYYY-MM" formatında CPI/HPI değerleri.
        reference_ym: Reel fiyatların referans alacağı ay.
        price_col: Nominal fiyat sütunu adı.
        date_col: İlan tarihi sütunu adı.

    Returns:
        df + price_real sütunu.
    """
    df = df.copy()
    df["year_month"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m")
    cpi_ref = cpi_series.loc[reference_ym]
    df["cpi_t"] = df["year_month"].map(cpi_series)
    df["price_real"] = df[price_col] * cpi_ref / df["cpi_t"]
    return df.drop(columns=["cpi_t"])
