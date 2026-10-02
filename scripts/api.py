from __future__ import annotations

from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data/gold/model.joblib"

app = FastAPI(title="AA Dev Model Serving", version="0.1.0")
model = joblib.load(MODEL_PATH)


class CustomerFeatures(BaseModel):
    age: int
    monthly_spend: float
    tenure_months: int
    support_calls: int


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "AA Dev Model Serving", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict(features: CustomerFeatures) -> dict[str, int]:
    result = model.predict(
        [[
            features.age,
            features.monthly_spend,
            features.tenure_months,
            features.support_calls,
        ]]
    )
    return {"churn_prediction": int(result[0])}
