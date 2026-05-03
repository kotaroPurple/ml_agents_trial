import importlib
import pickle
import time
from pathlib import Path

import pandas as pd

from ml_agents_trial.core.config import ARTIFACTS_EDA, ARTIFACTS_MODELS, DATA_PROCESSED
from ml_agents_trial.core.io import load_csv, load_json, save_json, train_test_split_df
from ml_agents_trial.core.metrics import (
    compute_classification_metrics,
    compute_regression_metrics,
)
from ml_agents_trial.models.configs import MODEL_CONFIGS


def _get_task_type() -> str:
    """Determine task type from data_summary.json."""
    summary_path = ARTIFACTS_EDA / "data_summary.json"
    if summary_path.exists():
        summary = load_json(summary_path)
        return summary.get("task_type", "regression")
    return "regression"


def _instantiate_model(config: dict):
    """Instantiate a model class from its import path string."""
    class_path: str = config["class"]
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    return cls(**config.get("params", {}))


def train_model(
    name: str,
    config: dict,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """Train a single model, save model.pkl and metrics.json, return metrics dict."""
    task_type = _get_task_type()

    model = _instantiate_model(config)

    start = time.time()
    model.fit(X_train, y_train)
    elapsed = round(time.time() - start, 3)

    y_pred = model.predict(X_test)

    if task_type == "classification":
        metrics = compute_classification_metrics(y_test, y_pred)
    else:
        metrics = compute_regression_metrics(y_test, y_pred)

    metrics["train_time_sec"] = elapsed
    metrics["model_name"] = name

    # Save model pickle
    model_dir: Path = ARTIFACTS_MODELS / name
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    # Save metrics
    metrics_path = model_dir / "metrics.json"
    save_json(metrics, metrics_path)

    print(f"  [{name}] trained in {elapsed}s | metrics: {metrics}")
    return metrics


def train_all(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """Train all models defined in MODEL_CONFIGS and save comparison.json."""
    task_type = _get_task_type()
    results: dict[str, dict] = {}

    print(f"Task type: {task_type}")
    print(f"Training {len(MODEL_CONFIGS)} models...")

    for name, config in MODEL_CONFIGS.items():
        try:
            metrics = train_model(name, config, X_train, y_train, X_test, y_test)
            results[name] = metrics
        except Exception as exc:
            print(f"  [{name}] FAILED: {exc}")
            results[name] = {"error": str(exc), "model_name": name}

    # Sort by RMSE (regression) or accuracy descending (classification), save as list
    if task_type == "regression":
        sorted_list = sorted(
            results.values(),
            key=lambda m: m.get("rmse", float("inf")),
        )
    else:
        sorted_list = sorted(
            results.values(),
            key=lambda m: m.get("accuracy", 0.0),
            reverse=True,
        )

    comparison_path = ARTIFACTS_MODELS / "comparison.json"
    save_json(sorted_list, comparison_path)
    print(f"\nComparison saved to: {comparison_path}")

    return {m["model_name"]: m for m in sorted_list}


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "MedHouseVal"

    df = load_csv(DATA_PROCESSED / "features.csv")
    X_train, X_test, y_train, y_test = train_test_split_df(df, target)

    results = train_all(X_train, y_train, X_test, y_test)

    task_type = _get_task_type()
    if task_type == "regression":
        best = min(
            (k for k in results if "error" not in results[k]),
            key=lambda k: results[k].get("rmse", float("inf")),
        )
        print(f"\nBest model: {best}  RMSE={results[best]['rmse']}  R2={results[best]['r2']}")
    else:
        best = max(
            (k for k in results if "error" not in results[k]),
            key=lambda k: results[k].get("accuracy", 0.0),
        )
        print(f"\nBest model: {best}  Accuracy={results[best]['accuracy']}")
