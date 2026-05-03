from pathlib import Path


def download(output_path: Path | None = None) -> Path:
    from sklearn.datasets import fetch_california_housing

    from ml_agents_trial.core.config import DATA_RAW

    dest = output_path or (DATA_RAW / "house_prices.csv")
    dest.parent.mkdir(parents=True, exist_ok=True)

    housing = fetch_california_housing(as_frame=True)
    df = housing.frame
    df.to_csv(dest, index=False)
    print(f"Saved {len(df)} rows → {dest}")
    return dest
