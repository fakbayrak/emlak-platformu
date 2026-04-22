"""İlçe yatırım skoru hesaplama (M4).

Formül:
    score = 100 × (w1·yield + w2·stability + w3·liquidity
                   + w4·appreciation + w5·affordability)
"""
from dataclasses import dataclass, field
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class ScoreWeights:
    yield_w: float = 0.30
    appreciation_w: float = 0.25
    stability_w: float = 0.20
    liquidity_w: float = 0.15
    affordability_w: float = 0.10

    def as_dict(self) -> Dict[str, float]:
        return {
            "yield": self.yield_w,
            "appreciation": self.appreciation_w,
            "stability": self.stability_w,
            "liquidity": self.liquidity_w,
            "affordability": self.affordability_w,
        }

    def validate(self):
        total = sum(self.as_dict().values())
        if not np.isclose(total, 1.0, atol=1e-3):
            raise ValueError(f"Ağırlıkların toplamı 1.0 olmalı, şu an: {total}")


def minmax_normalize(series: pd.Series) -> pd.Series:
    """[0, 1] aralığına ölçekler; tüm değerler aynıysa 0.5 döner."""
    s = series.astype(float)
    rng = s.max() - s.min()
    if rng == 0:
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / rng


def compute_yield(avg_rent: pd.Series, avg_sale: pd.Series) -> pd.Series:
    """Yıllık brüt kira getirisi = (aylık_kira × 12) / satış_fiyatı."""
    return (avg_rent * 12) / avg_sale.replace(0, np.nan)


def compute_stability(volatility: pd.Series) -> pd.Series:
    """Düşük volatilite → yüksek stabilite."""
    return 1 / (1 + volatility.fillna(0))


def compute_liquidity(listing_count: pd.Series) -> pd.Series:
    """Log ölçekte normalize edilmiş ilan sayısı."""
    log_counts = np.log1p(listing_count)
    return log_counts / log_counts.max() if log_counts.max() > 0 else log_counts


def compute_affordability(avg_price_per_m2: pd.Series) -> pd.Series:
    """Daha ucuz ilçeler daha yüksek ulaşılabilirlik."""
    return 1 - minmax_normalize(avg_price_per_m2)


def compute_investment_scores(district_df: pd.DataFrame,
                              weights: ScoreWeights | None = None) -> pd.DataFrame:
    """İlçe bazlı veriden 0-100 arası yatırım skoru üretir.

    Beklenen sütunlar:
        avg_sale_price_per_m2, avg_rent_per_m2, listing_count_90d,
        price_volatility_90d, appreciation_12m
    """
    weights = weights or ScoreWeights()
    weights.validate()
    df = district_df.copy()

    # Ham bileşenler
    raw_yield = compute_yield(df["avg_rent_per_m2"], df["avg_sale_price_per_m2"])
    raw_stability = compute_stability(df["price_volatility_90d"])
    raw_liquidity = compute_liquidity(df["listing_count_90d"])
    raw_appreciation = df["appreciation_12m"].fillna(0)
    raw_affordability = compute_affordability(df["avg_sale_price_per_m2"])

    # Normalize edilmiş bileşenler
    df["yield_score"] = minmax_normalize(raw_yield)
    df["stability_score"] = minmax_normalize(raw_stability)
    df["liquidity_score"] = raw_liquidity  # zaten 0-1
    df["appreciation_score"] = minmax_normalize(raw_appreciation)
    df["affordability_score"] = raw_affordability  # zaten 0-1

    # Ağırlıklı toplam
    df["investment_score"] = 100 * (
        weights.yield_w * df["yield_score"]
        + weights.stability_w * df["stability_score"]
        + weights.liquidity_w * df["liquidity_score"]
        + weights.appreciation_w * df["appreciation_score"]
        + weights.affordability_w * df["affordability_score"]
    )

    return df
