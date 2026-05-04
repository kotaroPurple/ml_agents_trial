# feature-engineer

Use this role for `codex command: engineer`. Generate feature engineering code under `src/ml_agents_trial/features/`.

## Required Reading

- `.codex/skills/tabular-ml-quality/SKILL.md`
- `artifacts/eda/data_summary.json`

## Required Output

Implement `src/ml_agents_trial/features/engineer.py` with:

- `build_features(df: pd.DataFrame, target: str) -> pd.DataFrame`
- a `__main__` block that reads `[CSV_PATH] [TARGET_COLUMN]` and writes `data/processed/features.csv`.

## Rules

- Do not transform the target column.
- Avoid target leakage and test-data statistics.
- Use EDA-backed transformations only.
- Prefer Pipeline/ColumnTransformer for fit-dependent preprocessing where the existing interface allows it.
- Use `apply_patch` for edits and `exec_command` for validation commands.
- Run the module after generation and report the output file shape.
- Do not use Claude-specific tool names, named-agent calls, or hook syntax.
