"""Baseline modeller."""
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge


def get_dummy():
    return DummyRegressor(strategy="mean")


def get_ridge(alpha: float = 1.0):
    return Ridge(alpha=alpha, random_state=42)
