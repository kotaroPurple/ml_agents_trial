import matplotlib

matplotlib.use("Agg")
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_predictions(y_true: pd.Series, y_pred: pd.Series, output_path: Path) -> None:
    """予測 vs 実績の散布図"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(y_true, y_pred, alpha=0.3, s=10, color="steelblue", label="predictions")

    vmin = min(y_true.min(), y_pred.min())
    vmax = max(y_true.max(), y_pred.max())
    ax.plot([vmin, vmax], [vmin, vmax], "r--", linewidth=1.5, label="perfect fit")

    ax.set_xlabel("Actual", fontsize=12)
    ax.set_ylabel("Predicted", fontsize=12)
    ax.set_title("Predicted vs Actual", fontsize=14)
    ax.legend()
    ax.set_xlim(vmin, vmax)
    ax.set_ylim(vmin, vmax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)


def plot_residuals(y_true: pd.Series, y_pred: pd.Series, output_path: Path) -> None:
    """残差プロット（上段: 残差 vs 予測値, 下段: 残差分布）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    residuals = y_true.values - np.asarray(y_pred)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # 残差 vs 予測値
    axes[0].scatter(y_pred, residuals, alpha=0.3, s=10, color="steelblue")
    axes[0].axhline(0, color="red", linestyle="--", linewidth=1.5)
    axes[0].set_xlabel("Predicted", fontsize=12)
    axes[0].set_ylabel("Residual", fontsize=12)
    axes[0].set_title("Residuals vs Predicted", fontsize=13)

    # 残差分布（ヒストグラム）
    axes[1].hist(residuals, bins=50, color="steelblue", edgecolor="white", alpha=0.8)
    axes[1].axvline(0, color="red", linestyle="--", linewidth=1.5)
    axes[1].set_xlabel("Residual", fontsize=12)
    axes[1].set_ylabel("Count", fontsize=12)
    axes[1].set_title("Residual Distribution", fontsize=13)

    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)


def plot_feature_importance(
    importances: dict[str, float], output_path: Path, top_n: int = 20
) -> None:
    """特徴量重要度の水平バーチャート（上位 top_n 件）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not importances:
        return

    sorted_items = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:top_n]
    features = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(9, max(4, len(features) * 0.4)))
    ax.barh(features[::-1], values[::-1], color="steelblue", alpha=0.85)
    ax.set_xlabel("Importance", fontsize=12)
    ax.set_title(f"Feature Importance (top {len(features)})", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)


def plot_model_comparison(
    comparison: list[dict], output_path: Path, metric: str = "rmse"
) -> None:
    """モデル比較バーチャート"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not comparison:
        return

    models = [entry["model_name"] for entry in comparison]
    values = [entry[metric] for entry in comparison]

    # 昇順ソート（RMSE などは小さいほど良い）
    paired = sorted(zip(values, models, strict=False), reverse=False)
    values_sorted = [p[0] for p in paired]
    models_sorted = [p[1] for p in paired]

    fig, ax = plt.subplots(figsize=(9, max(4, len(models) * 0.6)))
    colors = ["steelblue"] * len(models_sorted)
    bars = ax.barh(models_sorted, values_sorted, color=colors, alpha=0.85)

    # 値ラベル
    for bar, val in zip(bars, values_sorted, strict=False):
        ax.text(
            bar.get_width() + max(values_sorted) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.4f}",
            va="center",
            fontsize=10,
        )

    ax.set_xlabel(metric.upper(), fontsize=12)
    ax.set_title(f"Model Comparison — {metric.upper()}", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
