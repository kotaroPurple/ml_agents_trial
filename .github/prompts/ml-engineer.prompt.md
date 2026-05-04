---
agent: "agent"
description: "Generate feature engineering code from EDA artifacts"
---

# ML Engineer

Target column: `${input:target_column:MedHouseVal}` (default from copilot-instructions.md > プロジェクト設定)

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [tabular ML quality](../skills/tabular-ml-quality/SKILL.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)
- #file:../../src/ml_agents_trial/core/config.py
- #file:../../src/ml_agents_trial/core/io.py

## Role

Act as the feature engineer for this repository.

## Tasks

1. Confirm `artifacts/eda/data_summary.json` exists.
2. Implement feature engineering modules in `src/ml_agents_trial/features/` (file structure may vary by complexity):
   - Required public function: `build_features(df, target) -> pd.DataFrame`.
   - Do not transform the target column. Avoid target leakage and all-data statistics.
3. Structurally review: run `/ml-code-review` with target=`src/ml_agents_trial/features/`. Return to implementation if FAIL.
4. ML quality review: run `/ml-quality-review` with phase=`features`, target=`src/ml_agents_trial/features/`. Return to implementation if FAIL.
5. Run:

```bash
.venv/bin/python src/ml_agents_trial/features/engineer.py ${input:csv_path:data/raw/house_prices.csv} ${input:target_column:MedHouseVal}
```

6. Run `uv run ruff check src/ tests/`.
7. Commit only `src/ml_agents_trial/features/` with:

```bash
git add src/ml_agents_trial/features/
STAGED=$(git diff --name-only --cached | grep 'ml_agents_trial/features/' | sed 's|src/ml_agents_trial/features/||')
git commit -m "feat(features): generate feature engineering module

$(echo "$STAGED" | sed 's/^/- /')"
```

8. Report added features, processed CSV shape, commit hash, and next step (`/ml-build`).
