from pathlib import Path


def test_source_dataset_exists():
    assert Path("data/source/customers.csv").exists()
