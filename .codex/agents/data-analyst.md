# data-analyst

Use this role for `codex command: analyze`. Generate EDA modules under `src/ml_agents_trial/eda/` for a CSV and target column.

## Required Outputs

Implement `src/ml_agents_trial/eda/analysis.py` with:

- `summarize_dataset(df: pd.DataFrame, target: str) -> dict`
- `detect_task_type(df: pd.DataFrame, target: str) -> str`
- `find_top_features(df: pd.DataFrame, target: str, n: int = 10) -> list[str]`
- a `__main__` block that reads `[CSV_PATH] [TARGET_COLUMN]`, writes `artifacts/eda/data_summary.json`, and prints task type/top features.

Implement `src/ml_agents_trial/eda/plots.py` with:

- `plot_distributions(df: pd.DataFrame, output_dir: Path) -> None`
- `plot_correlation_heatmap(df: pd.DataFrame, target: str, output_dir: Path) -> None`

## Rules

- Use `apply_patch` for edits.
- Use `from ml_agents_trial.core.xxx import ...` for project infrastructure.
- `plots.py` must use `matplotlib.use("Agg")` before importing `pyplot`.
- Keep modules standalone and typed.
- After generation, run `.venv/bin/python src/ml_agents_trial/eda/analysis.py [CSV_PATH] [TARGET_COLUMN]`.
