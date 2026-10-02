from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import pyarrow as pa
from deltalake import write_deltalake


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source/customers.csv"
BRONZE = ROOT / "data/bronze/customers_delta"


def main() -> None:
    df = pd.read_csv(SOURCE)
    BRONZE.parent.mkdir(parents=True, exist_ok=True)
    write_deltalake(str(BRONZE), pa.Table.from_pandas(df), mode="overwrite")

    con = duckdb.connect()
    con.execute("INSTALL delta")
    con.execute("LOAD delta")
    count = con.execute(
        f"SELECT COUNT(*) FROM delta_scan('{BRONZE.as_posix()}')"
    ).fetchone()[0]
    print(f"Bronze rows: {count}")
    con.close()


if __name__ == "__main__":
    main()
