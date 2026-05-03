# codex command: analyze

Analyze a CSV and generate EDA modules/artifacts.

## Arguments

`[CSV_PATH] [TARGET_COLUMN]`

- Default CSV_PATH: `data/raw/house_prices.csv`
- Default TARGET_COLUMN: `MedHouseVal`

## Steps

1. Confirm `[CSV_PATH]` exists.
2. Read `.codex/agents/data-analyst.md`.
3. Act as `data-analyst` and implement `src/ml_agents_trial/eda/analysis.py` and `src/ml_agents_trial/eda/plots.py`.
4. Act as `code-reviewer` by reading `.codex/agents/code-reviewer.md` and checking `src/ml_agents_trial/eda/`.
5. Domain review:
   - `summarize_dataset`, `detect_task_type`, and `find_top_features` exist.
   - `detect_task_type` uses target dtype and cardinality reasonably.
6. Execute:

```bash
.venv/bin/python src/ml_agents_trial/eda/analysis.py [CSV_PATH] [TARGET_COLUMN]
.venv/bin/python -c "from ml_agents_trial.core.io import load_csv; from ml_agents_trial.eda.plots import plot_distributions, plot_correlation_heatmap; from ml_agents_trial.core.config import ARTIFACTS_EDA; df = load_csv('[CSV_PATH]'); plot_distributions(df, ARTIFACTS_EDA / 'plots'); plot_correlation_heatmap(df, '[TARGET_COLUMN]', ARTIFACTS_EDA / 'plots'); print('plots saved')"
```

7. Validate:

```bash
uv run ruff check src/ tests/
```

8. Commit only EDA files:

```bash
git add src/ml_agents_trial/eda/
git commit -m "feat(eda): generate EDA modules"
```

9. Report data shape, missing values, task type, top 5 features, commit hash, and next command.
