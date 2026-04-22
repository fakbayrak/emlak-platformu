"""ColumnTransformer tabanlı preprocessing pipeline."""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_COLS = ["m2", "building_age", "floor", "comfort_score", "total_rooms",
                "m2_per_room", "listing_year", "listing_month"]
CATEGORICAL_COLS = ["city", "district", "heating_type", "age_group", "floor_class"]


def build_preprocessor() -> ColumnTransformer:
    """Sayısal + kategorik veri için ortak preprocessor."""
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer([
        ("num", numeric_pipeline, NUMERIC_COLS),
        ("cat", categorical_pipeline, CATEGORICAL_COLS),
    ], remainder="drop")
