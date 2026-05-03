import pandas as pd

from ml_agents_trial.core.config import ARTIFACTS_EDA
from ml_agents_trial.core.io import load_csv, save_json


def summarize_dataset(df: pd.DataFrame, target: str) -> dict:
    """shape, dtypes, 欠損値, ターゲット統計を集計して返す"""
    shape = {"rows": int(df.shape[0]), "cols": int(df.shape[1])}

    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    missing = {
        col: int(df[col].isna().sum())
        for col in df.columns
        if df[col].isna().sum() > 0
    }

    target_stats: dict = {}
    if target in df.columns:
        s = df[target]
        target_stats = {
            "mean": float(s.mean()),
            "std": float(s.std()),
            "min": float(s.min()),
            "25%": float(s.quantile(0.25)),
            "50%": float(s.median()),
            "75%": float(s.quantile(0.75)),
            "max": float(s.max()),
            "nunique": int(s.nunique()),
        }

    return {
        "shape": shape,
        "dtypes": dtypes,
        "missing": missing,
        "target_stats": target_stats,
    }


def detect_task_type(df: pd.DataFrame, target: str) -> str:
    """ターゲット列のユニーク数・dtype から 'regression' or 'classification' を返す"""
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in DataFrame.")

    col = df[target]
    dtype = col.dtype

    # 数値型でユニーク数が多ければ回帰、少なければ分類
    if pd.api.types.is_float_dtype(dtype):
        return "regression"

    if pd.api.types.is_integer_dtype(dtype):
        nunique = col.nunique()
        threshold = min(20, int(len(df) * 0.05))
        if nunique <= threshold:
            return "classification"
        return "regression"

    # 文字列・カテゴリ型は分類
    return "classification"


def find_top_features(df: pd.DataFrame, target: str, n: int = 10) -> list[str]:
    """ターゲットとの相関が高い特徴量名リストを返す"""
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in DataFrame.")

    numeric_df = df.select_dtypes(include="number")
    if target not in numeric_df.columns:
        raise ValueError(f"Target column '{target}' is not numeric; cannot compute correlation.")

    corr = numeric_df.corr()[target].drop(labels=[target])
    top = corr.abs().sort_values(ascending=False).head(n)
    return list(top.index)


if __name__ == "__main__":
    import sys

    csv_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else str(ARTIFACTS_EDA.parent.parent / "data/raw/house_prices.csv")
    )
    target = sys.argv[2] if len(sys.argv) > 2 else "MedHouseVal"

    df = load_csv(csv_path)
    summary = summarize_dataset(df, target)
    task_type = detect_task_type(df, target)
    top_features = find_top_features(df, target)

    save_json(
        {**summary, "task_type": task_type, "top_features": top_features},
        ARTIFACTS_EDA / "data_summary.json",
    )

    print(f"task_type: {task_type}")
    print(f"top_features: {top_features[:5]}")
