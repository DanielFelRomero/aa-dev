from __future__ import annotations

import pandas as pd


def missingness_rate(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    return float(df.isna().mean().mean())


def mean_shift(reference: pd.Series, current: pd.Series) -> float:
    ref_mean = float(reference.mean())
    cur_mean = float(current.mean())
    scale = abs(ref_mean) if abs(ref_mean) > 1e-12 else 1.0
    return abs(cur_mean - ref_mean) / scale


def drift_flag(reference: pd.Series, current: pd.Series, threshold: float) -> bool:
    return mean_shift(reference, current) >= threshold
