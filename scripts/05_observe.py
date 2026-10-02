from pathlib import Path
from deltalake import DeltaTable
from aa_dev.monitoring import drift_flag,mean_shift,missingness_rate
ROOT=Path(__file__).resolve().parents[1]; GOLD=ROOT/"data/gold/features_delta"
def main():
    df=DeltaTable(str(GOLD)).to_pandas(); midpoint=len(df)//2
    ref=df["monthly_spend"].iloc[:midpoint]; cur=df["monthly_spend"].iloc[midpoint:]
    print(f"Rows: {len(df)}"); print(f"Missingness: {missingness_rate(df):.4f}")
    print(f"Monthly spend mean shift: {mean_shift(ref,cur):.4f}")
    print(f"Drift flag: {drift_flag(ref,cur,threshold=.20)}")
if __name__=="__main__": main()
