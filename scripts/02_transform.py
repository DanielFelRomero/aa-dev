from pathlib import Path
import pyarrow as pa
from deltalake import DeltaTable, write_deltalake
from aa_dev.features import FEATURE_COLUMNS, build_feature_dataset
from aa_dev.quality import transform_silver
ROOT=Path(__file__).resolve().parents[1]
BRONZE=ROOT/"data/bronze/customers_delta"; SILVER=ROOT/"data/silver/customers_delta"; GOLD=ROOT/"data/gold/features_delta"
def main():
    bronze=DeltaTable(str(BRONZE)).to_pandas()
    silver=transform_silver(bronze,salt="aa-dev-training-salt")
    SILVER.parent.mkdir(parents=True,exist_ok=True); write_deltalake(str(SILVER),pa.Table.from_pandas(silver),mode="overwrite")
    x,y=build_feature_dataset(silver); gold=silver[["region"]].copy(); gold[FEATURE_COLUMNS]=x; gold["churn"]=y
    GOLD.parent.mkdir(parents=True,exist_ok=True); write_deltalake(str(GOLD),pa.Table.from_pandas(gold),mode="overwrite")
    print(f"Silver rows: {len(silver)}"); print(f"Gold rows: {len(gold)}")
if __name__=="__main__": main()
