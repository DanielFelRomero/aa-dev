from __future__ import annotations

import pandas as pd


FEATURE_COLUMNS = [
    "age",
    "monthly_spend",
    "tenure_months",
    "support_calls",
]

TARGET_COLUMN = "churn"


def build_feature_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    x = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    return x, y
