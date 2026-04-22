"""Veri temizleme fonksiyonları."""
import pandas as pd


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Yinelenen ilanları kaldırır."""
    subset = subset or ["source_url_hash"]
    return df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)


def clip_outliers_iqr(df: pd.DataFrame, column: str, k: float = 1.5,
                      group_by: str | None = None) -> pd.DataFrame:
    """IQR yöntemi ile aykırı değerleri kırpar. İlçe bazında da gruplanabilir."""
    df = df.copy()
    if group_by:
        for group_val, group_df in df.groupby(group_by):
            q1 = group_df[column].quantile(0.25)
            q3 = group_df[column].quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - k * iqr, q3 + k * iqr
            mask = (df[group_by] == group_val)
            df.loc[mask, column] = df.loc[mask, column].clip(lower, upper)
    else:
        q1, q3 = df[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        df[column] = df[column].clip(q1 - k * iqr, q3 + k * iqr)
    return df


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Eksik değerleri doldurur."""
    df = df.copy()
    # Sayısal: medyan
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())
    # Kategorik: mod
    for col in df.select_dtypes(include="object").columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else "bilinmiyor")
    return df
