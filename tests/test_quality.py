import pandas as pd

from aa_dev.quality import pseudonymize, transform_silver


def test_pseudonymization_is_deterministic():
    assert pseudonymize("C001", "salt") == pseudonymize("C001", "salt")
    assert pseudonymize("C001", "salt") != pseudonymize("C002", "salt")


def test_transform_silver_removes_raw_identifier():
    df = pd.DataFrame(
        {
            "customer_id": ["C001"],
            "age": [30],
            "monthly_spend": [100.0],
            "tenure_months": [12],
            "support_calls": [2],
            "region": ["north"],
            "churn": [0],
        }
    )
    out = transform_silver(df, salt="salt")
    assert "customer_id" not in out.columns
    assert "customer_key" in out.columns
