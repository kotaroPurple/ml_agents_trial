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
3. Act as `feature-engineer` and implement `src/ml_agents_trial/features/engineer.py` using `apply_patch`.
4. Act as `code-reviewer` by reading `.codex/agents/code-reviewer.md` and checking `src/ml_agents_trial/features/`.
   - If review returns FAIL, fix the reported issues as `feature-engineer`, then repeat this review before continuing.
5. Domain review:
   - `build_features(df, target)` signature is unchanged.
   - Target column is not transformed.
   - EDA-backed skew/category/missing-value handling is reasonable.
   - If review fails, fix the issue and return to step 4.
6. Act as `ml-reviewer` by reading `.codex/agents/ml-reviewer.md` and checking leakage, target mutation, all-data statistics, and EDA consistency.
   - If review returns FAIL, fix the reported issues as `feature-engineer`, then repeat steps 4-6.
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

## Codex Notes

- This command is invoked as `codex command: engineer [TARGET_COLUMN]`; it is not a slash command.
- Do not use Claude-specific named-agent calls, hooks, or settings files.
- Use `exec_command` for shell validation and commit only the files named in this command.
