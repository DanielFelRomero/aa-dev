from pathlib import Path
import joblib
from deltalake import DeltaTable
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from aa_dev.features import FEATURE_COLUMNS
ROOT=Path(__file__).resolve().parents[1]; GOLD=ROOT/"data/gold/features_delta"; MODEL=ROOT/"data/gold/model.joblib"
def main():
    df=DeltaTable(str(GOLD)).to_pandas(); x=df[FEATURE_COLUMNS]; y=df["churn"]
    xtr,xte,ytr,yte=train_test_split(x,y,test_size=.2,random_state=42,stratify=y)
    model=Pipeline([("scaler",StandardScaler()),("classifier",LogisticRegression(max_iter=500,random_state=42))])
    model.fit(xtr,ytr); print(f"Accuracy: {accuracy_score(yte,model.predict(xte)):.3f}")
    MODEL.parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,MODEL)
if __name__=="__main__": main()
