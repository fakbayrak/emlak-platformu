"""Regresyon değerlendirme metrikleri."""
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true, y_pred, log_scale: bool = False) -> dict:
    """MAE, RMSE, R², MAPE hesaplar.

    Args:
        log_scale: Tahminler log1p uzayında ise True ver; metrikler
                   gerçek TL cinsinden hesaplanır.
    """
    if log_scale:
        y_true = np.expm1(y_true)
        y_pred = np.expm1(y_pred)

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, 1e-9, y_true))) * 100

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "mape": float(mape),
    }
