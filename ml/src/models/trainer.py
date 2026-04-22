"""Model eğitim yardımcıları."""
import time
from typing import Dict

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

from ml.src.evaluation.metrics import compute_metrics


def train_and_log(
    model: BaseEstimator,
    X_train, y_train, X_test, y_test,
    model_name: str,
    experiment_name: str = "emlak_tahmin",
    tracking_uri: str | None = None,
    params: Dict | None = None,
) -> BaseEstimator:
    """Modeli eğitir, metriklerini hesaplar ve MLflow'a kaydeder."""
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=model_name):
        if params:
            mlflow.log_params(params)

        start = time.time()
        model.fit(X_train, y_train)
        duration = time.time() - start

        preds = model.predict(X_test)
        metrics = compute_metrics(y_test, preds, log_scale=True)

        mlflow.log_metrics(metrics)
        mlflow.log_metric("training_seconds", duration)
        mlflow.sklearn.log_model(model, name="model")

    return model


def hyperparameter_search(
    estimator: BaseEstimator,
    X, y,
    param_distributions: Dict,
    n_iter: int = 50,
    cv: int = 5,
    mode: str = "random",
) -> BaseEstimator:
    """RandomizedSearchCV veya GridSearchCV ile en iyi modeli bulur."""
    if mode == "random":
        search = RandomizedSearchCV(
            estimator, param_distributions,
            n_iter=n_iter, cv=cv, scoring="neg_mean_absolute_error",
            n_jobs=-1, random_state=42, verbose=1,
        )
    else:
        search = GridSearchCV(
            estimator, param_distributions,
            cv=cv, scoring="neg_mean_absolute_error",
            n_jobs=-1, verbose=1,
        )
    search.fit(X, y)
    return search.best_estimator_


def save_model(model, path: str):
    joblib.dump(model, path)


def save_preprocessor(preprocessor, path: str):
    joblib.dump(preprocessor, path)
