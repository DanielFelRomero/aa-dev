from __future__ import annotations

from pathlib import Path

import pandas as pd

from aa_dev.monitoring import drift_flag, mean_shift, missingness_rate


ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data/gold/features.parquet"


def main() -> None:
    df = pd.read_parquet(GOLD)

    midpoint = len(df) // 2
    reference = df["monthly_spend"].iloc[:midpoint]
    current = df["monthly_spend"].iloc[midpoint:]

    print(f"Rows: {len(df)}")
    print(f"Missingness: {missingness_rate(df):.4f}")
    print(f"Monthly spend mean shift: {mean_shift(reference, current):.4f}")
    print(f"Drift flag: {drift_flag(reference, current, threshold=0.20)}")


if __name__ == "__main__":
    main()
