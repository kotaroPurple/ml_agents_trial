import numpy as np
import pandas as pd

from ml_agents_trial.core.config import DATA_PROCESSED


def build_features(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    入力DataFrameに特徴量変換を適用して返す。
    ターゲット列は変更しない。

    EDA (artifacts/eda/data_summary.json) に基づく変換方針:
    - 右スキューが強い列 (skewness > 1) に log1p 変換:
        MedInc (1.65), AveRooms (20.70), AveBedrms (31.32),
        Population (4.94), AveOccup (97.64)
    - Latitude/Longitude から地理的クラスタリング特徴量を生成
    - MedInc と住居密度の交互作用特徴量を追加
    - 欠損値なし (data_summary.json の missing: {})
    """
    df = df.copy()

    # --- 右スキュー列の log1p 変換 (skewness > 1) ---
    skewed_cols = ["MedInc", "AveRooms", "AveBedrms", "Population", "AveOccup"]
    for col in skewed_cols:
        if col in df.columns and col != target:
            df[f"{col}_log"] = np.log1p(df[col])

    # --- 地理的特徴量 ---
    if "Latitude" in df.columns and "Longitude" in df.columns:
        # 緯度経度の積 (地域の方向性を捉える)
        df["lat_lon_interact"] = df["Latitude"] * df["Longitude"]
        # カリフォルニア主要都市からのユークリッド距離
        # SF: (37.77, -122.42), LA: (34.05, -118.24)
        df["dist_sf"] = np.sqrt(
            (df["Latitude"] - 37.77) ** 2 + (df["Longitude"] - (-122.42)) ** 2
        )
        df["dist_la"] = np.sqrt(
            (df["Latitude"] - 34.05) ** 2 + (df["Longitude"] - (-118.24)) ** 2
        )

    # --- 交互作用特徴量 ---
    # 所得 × 平均部屋数 (物件の価値を反映)
    if "MedInc" in df.columns and "AveRooms" in df.columns:
        df["inc_x_rooms"] = df["MedInc"] * df["AveRooms"]

    # 人口密度: 人口 / 平均居住者数 (混雑度の代理指標)
    if "Population" in df.columns and "AveOccup" in df.columns:
        df["pop_density"] = df["Population"] / (df["AveOccup"] + 1e-6)

    # 寝室比率: AveBedrms / AveRooms (間取りの特性)
    if "AveBedrms" in df.columns and "AveRooms" in df.columns:
        df["bedroom_ratio"] = df["AveBedrms"] / (df["AveRooms"] + 1e-6)

    return df


if __name__ == "__main__":
    import sys

    from ml_agents_trial.core.io import load_csv

    csv_path = (
        sys.argv[1] if len(sys.argv) > 1 else "data/raw/house_prices.csv"
    )
    target = sys.argv[2] if len(sys.argv) > 2 else "MedHouseVal"
    df = load_csv(csv_path)
    df_out = build_features(df, target)
    out_path = DATA_PROCESSED / "features.csv"
    df_out.to_csv(out_path, index=False)
    print(f"Features saved: {df_out.shape} → {out_path}")
    print(f"Added columns: {[c for c in df_out.columns if c not in df.columns]}")
