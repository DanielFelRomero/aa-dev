from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "data/gold/features.parquet"
MODEL = ROOT / "data/gold/model.joblib"


def main() -> None:
    df = pd.read_parquet(GOLD)
    x = df.drop(columns=["churn"])
    y = df["churn"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=500, random_state=42)),
        ]
    )

    model.fit(x_train, y_train)
    pred = model.predict(x_test)

    print(f"Accuracy: {accuracy_score(y_test, pred):.3f}")

    MODEL.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL)


if __name__ == "__main__":
    main()
