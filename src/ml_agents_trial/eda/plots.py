import matplotlib

matplotlib.use("Agg")
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_distributions(df: pd.DataFrame, output_dir: Path) -> None:
    """数値列のヒストグラムを保存"""
    output_dir.mkdir(parents=True, exist_ok=True)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    cols_per_row = 3
    n_cols = cols_per_row
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
    axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, col in enumerate(numeric_cols):
        ax = axes_flat[i]
        df[col].dropna().hist(bins=30, ax=ax, color="steelblue", edgecolor="white")
        ax.set_title(col, fontsize=11)
        ax.set_xlabel(col)
        ax.set_ylabel("Count")

    # 余ったサブプロットを非表示
    for j in range(len(numeric_cols), len(axes_flat)):
        axes_flat[j].set_visible(False)

    fig.tight_layout()
    out_path = output_dir / "distributions.png"
    fig.savefig(out_path, dpi=100)
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_correlation_heatmap(df: pd.DataFrame, target: str, output_dir: Path) -> None:
    """相関ヒートマップを保存"""
    output_dir.mkdir(parents=True, exist_ok=True)
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr()

    n = len(corr)
    fig, ax = plt.subplots(figsize=(max(6, n), max(5, n - 1)))

    im = ax.imshow(corr.values, vmin=-1, vmax=1, cmap="coolwarm", aspect="auto")
    fig.colorbar(im, ax=ax, label="Pearson r")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(corr.index, fontsize=9)
    ax.set_title("Correlation Heatmap", fontsize=13)

    # セル内に数値を表示
    for i in range(n):
        for j in range(n):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.6 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7, color=color)

    fig.tight_layout()
    out_path = output_dir / "correlation_heatmap.png"
    fig.savefig(out_path, dpi=100)
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import sys

    from ml_agents_trial.core.config import ARTIFACTS_EDA
    from ml_agents_trial.core.io import load_csv

    csv_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else str(ARTIFACTS_EDA.parent.parent / "data/raw/house_prices.csv")
    )
    target = sys.argv[2] if len(sys.argv) > 2 else "MedHouseVal"
    output_dir = ARTIFACTS_EDA / "plots"

    df = load_csv(csv_path)
    plot_distributions(df, output_dir)
    plot_correlation_heatmap(df, target, output_dir)
