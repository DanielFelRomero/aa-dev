from __future__ import annotations

from pathlib import Path

import pandas as pd
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

from aa_dev.features import build_feature_dataset
from aa_dev.quality import transform_silver


ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "data/bronze/customers_delta"
SILVER = ROOT / "data/silver/customers_delta"
GOLD = ROOT / "data/gold/features.parquet"


def main() -> None:
    bronze = DeltaTable(str(BRONZE)).to_pandas()
    silver = transform_silver(bronze, salt="aa-dev-training-salt")

    SILVER.parent.mkdir(parents=True, exist_ok=True)
    write_deltalake(str(SILVER), pa.Table.from_pandas(silver), mode="overwrite")

    x, y = build_feature_dataset(silver)
    gold = x.copy()
    gold["churn"] = y

    GOLD.parent.mkdir(parents=True, exist_ok=True)
    gold.to_parquet(GOLD, index=False)

    print(f"Silver rows: {len(silver)}")
    print(f"Gold rows: {len(gold)}")


if __name__ == "__main__":
    main()
