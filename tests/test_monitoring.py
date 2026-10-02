import pandas as pd

from aa_dev.monitoring import drift_flag, missingness_rate


def test_missingness_rate():
    df = pd.DataFrame({"a": [1, None], "b": [2, 3]})
    assert missingness_rate(df) == 0.25


def test_drift_flag():
    reference = pd.Series([100.0, 100.0])
    current = pd.Series([130.0, 130.0])
    assert drift_flag(reference, current, threshold=0.20)
