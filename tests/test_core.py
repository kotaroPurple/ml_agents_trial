import numpy as np
import pandas as pd

from ml_agents_trial.core.io import load_csv, load_json, save_json, train_test_split_df
from ml_agents_trial.core.metrics import compute_regression_metrics


def test_load_csv_roundtrip(sample_df, tmp_path):
    p = tmp_path / "test.csv"
    sample_df.to_csv(p, index=False)
    loaded = load_csv(p)
    assert loaded.shape == sample_df.shape


def test_save_and_load_json(tmp_path):
    data = {"key": [1, 2, 3], "nested": {"a": 1}}
    p = tmp_path / "test.json"
    save_json(data, p)
    loaded = load_json(p)
    assert loaded == data


def test_train_test_split_sizes(sample_df):
    X_train, X_test, y_train, y_test = train_test_split_df(sample_df, "MedHouseVal")
    assert len(X_train) == 80
    assert len(X_test) == 20
    assert "MedHouseVal" not in X_train.columns


def test_regression_metrics_perfect():
    y = pd.Series([1.0, 2.0, 3.0])
    m = compute_regression_metrics(y, y)
    assert m["rmse"] == 0.0
    assert m["r2"] == 1.0


def test_regression_metrics_keys(sample_df):
    rng = np.random.default_rng(0)
    y_true = pd.Series(rng.uniform(0, 5, 50))
    y_pred = pd.Series(rng.uniform(0, 5, 50))
    m = compute_regression_metrics(y_true, y_pred)
    for key in ["rmse", "mae", "r2", "mape"]:
        assert key in m
