"""SHAP açıklama yardımcıları."""
import joblib
import shap


def create_tree_explainer(model, save_path: str | None = None):
    """Ağaç tabanlı model için TreeExplainer oluşturur."""
    explainer = shap.TreeExplainer(model)
    if save_path:
        joblib.dump(explainer, save_path)
    return explainer


def top_k_features(shap_values, feature_names, k: int = 5):
    """|SHAP| mutlak değerine göre en önemli k özelliği döndürür."""
    import numpy as np
    abs_vals = np.abs(shap_values)
    idx = np.argsort(abs_vals)[::-1][:k]
    return [(feature_names[i], float(shap_values[i])) for i in idx]
