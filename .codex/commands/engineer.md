# codex command: engineer

Generate feature engineering modules from EDA artifacts.

## Arguments

`[TARGET_COLUMN]`

- Default TARGET_COLUMN: `MedHouseVal`

## Steps

1. Confirm `artifacts/eda/data_summary.json` exists.
2. Read:
   - `.codex/agents/feature-engineer.md`
   - `.codex/skills/tabular-ml-quality/SKILL.md`
3. Act as `feature-engineer` and implement `src/ml_agents_trial/features/engineer.py`.
4. Act as `code-reviewer` by reading `.codex/agents/code-reviewer.md` and checking `src/ml_agents_trial/features/`.
5. Domain review:
   - `build_features(df, target)` signature is unchanged.
   - Target column is not transformed.
   - EDA-backed skew/category/missing-value handling is reasonable.
6. Act as `ml-reviewer` by reading `.codex/agents/ml-reviewer.md` and checking leakage, target mutation, all-data statistics, and EDA consistency.
7. Execute:

```bash
.venv/bin/python src/ml_agents_trial/features/engineer.py data/raw/house_prices.csv [TARGET_COLUMN]
```

8. Validate:

```bash
uv run ruff check src/ tests/
```

9. Commit only feature files:

```bash
git add src/ml_agents_trial/features/
git commit -m "feat(features): generate feature engineering module"
```

10. Report added features, `data/processed/features.csv` shape, commit hash, and next command.
