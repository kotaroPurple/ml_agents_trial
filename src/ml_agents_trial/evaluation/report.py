import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from ml_agents_trial.core.config import ARTIFACTS_MODELS, DATA_PROCESSED
from ml_agents_trial.core.io import load_csv, load_json, save_json, train_test_split_df
from ml_agents_trial.core.metrics import compute_regression_metrics
from ml_agents_trial.evaluation.plots import (
    plot_feature_importance,
    plot_model_comparison,
    plot_predictions,
    plot_residuals,
)


def _load_model(model_dir: Path):
    """model.pkl を読み込んで返す"""
    model_path = model_dir / "model.pkl"
    with open(model_path, "rb") as f:
        return pickle.load(f)


def _extract_feature_importances(model, feature_names: list[str]) -> dict[str, float]:
    """モデルから特徴量重要度を抽出する（未対応モデルは空 dict を返す）"""
    if hasattr(model, "feature_importances_"):
        return dict(zip(feature_names, model.feature_importances_.tolist(), strict=False))
    if hasattr(model, "coef_"):
        coefs = np.abs(model.coef_).tolist()
        return dict(zip(feature_names, coefs, strict=False))
    return {}


def evaluate_all_models(X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    artifacts/models/*/model.pkl を全て読み込んで予測・評価プロットを生成する。

    各モデルのプロットを artifacts/models/{name}/plots/ に保存し、
    メトリクスの dict を返す。
    """
    results: dict[str, dict] = {}
    feature_names = X_test.columns.tolist()

    model_dirs = sorted(ARTIFACTS_MODELS.iterdir())
    model_dirs = [d for d in model_dirs if d.is_dir()]

    for model_dir in model_dirs:
        name = model_dir.name
        model_pkl = model_dir / "model.pkl"
        if not model_pkl.exists():
            continue

        model = _load_model(model_dir)
        y_pred_arr = model.predict(X_test)
        y_pred = pd.Series(y_pred_arr, index=y_test.index, name="predicted")

        metrics = compute_regression_metrics(y_test, y_pred)
        metrics["model_name"] = name

        plots_dir = model_dir / "plots"
        plots_dir.mkdir(parents=True, exist_ok=True)

        plot_predictions(y_test, y_pred, plots_dir / "predictions.png")
        plot_residuals(y_test, y_pred, plots_dir / "residuals.png")

        importances = _extract_feature_importances(model, feature_names)
        if importances:
            plot_feature_importance(importances, plots_dir / "feature_importance.png")

        results[name] = metrics
        print(f"  [{name}] rmse={metrics['rmse']} r2={metrics['r2']}")

    # モデル比較プロット（全モデル分）
    comparison_list = list(results.values())
    if comparison_list:
        plot_model_comparison(
            comparison_list,
            ARTIFACTS_MODELS / "plots" / "model_comparison.png",
            metric="rmse",
        )

    return results


def generate_report(comparison_path: Path | None = None) -> dict:
    """
    comparison.json を読んで評価サマリーを生成して返す。

    Returns
    -------
    dict
        {
            "best_model": str,
            "best_rmse": float,
            "models": list[dict],
        }
    """
    if comparison_path is None:
        comparison_path = ARTIFACTS_MODELS / "comparison.json"

    if not comparison_path.exists():
        return {}

    models: list[dict] = load_json(comparison_path)

    best = min(models, key=lambda m: m["rmse"])
    summary = {
        "best_model": best["model_name"],
        "best_rmse": best["rmse"],
        "best_r2": best["r2"],
        "models": models,
    }
    save_json(summary, ARTIFACTS_MODELS / "report_summary.json")
    return summary


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "MedHouseVal"

    print(f"Loading processed features (target={target}) ...")
    df = load_csv(DATA_PROCESSED / "features.csv")
    _, X_test, _, y_test = train_test_split_df(df, target)

    print("Evaluating all models ...")
    results = evaluate_all_models(X_test, y_test)

    print("Generating report summary ...")
    summary = generate_report()
    if summary:
        print(f"Best model: {summary['best_model']}  RMSE={summary['best_rmse']}  R2={summary['best_r2']}")

    print("DONE: evaluation report generated")
