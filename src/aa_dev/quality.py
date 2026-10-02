from __future__ import annotations

import hashlib

import pandas as pd


REQUIRED_COLUMNS = [
    "customer_id",
    "age",
    "monthly_spend",
    "tenure_months",
    "support_calls",
    "region",
    "churn",
]


def pseudonymize(value: object, salt: str) -> str:
    raw = f"{salt}:{value}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_required_columns(df: pd.DataFrame) -> None:
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def transform_silver(df: pd.DataFrame, salt: str) -> pd.DataFrame:
    validate_required_columns(df)
    out = df.copy()
    out["customer_key"] = out["customer_id"].map(
        lambda value: pseudonymize(value, salt)
    )
    out = out.drop(columns=["customer_id"])
    return out
