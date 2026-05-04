---
agent: "agent"
description: "Generate EDA modules and artifacts for a CSV target"
---

# ML Analyze

CSV path: `${input:csv_path:data/raw/house_prices.csv}` (default from copilot-instructions.md > プロジェクト設定)
Target column: `${input:target_column:MedHouseVal}` (default from copilot-instructions.md > プロジェクト設定)

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)
- #file:../../src/ml_agents_trial/core/config.py
- #file:../../src/ml_agents_trial/core/io.py

## Role

Act as the data analyst for this repository.

## Tasks

1. Confirm the CSV exists.
2. Implement EDA modules in `src/ml_agents_trial/eda/` (file structure may vary by complexity):
   - Required public functions: `summarize_dataset`, `detect_task_type`, `find_top_features`, `plot_distributions`, `plot_correlation_heatmap`.
   - At least one file must have a `__main__` block.
3. Structurally review: run `/ml-code-review` with target=`src/ml_agents_trial/eda/`. Return to implementation if FAIL.
4. ML quality review: run `/ml-quality-review` with phase=`eda`, target=`artifacts/eda/data_summary.json`. Return to implementation if FAIL.
5. Run:

```bash
.venv/bin/python src/ml_agents_trial/eda/analysis.py ${input:csv_path:data/raw/house_prices.csv} ${input:target_column:MedHouseVal}
```

6. Generate EDA plots.
7. Run `uv run ruff check src/ tests/`.
8. Commit only `src/ml_agents_trial/eda/` with:

```bash
git add src/ml_agents_trial/eda/
STAGED=$(git diff --name-only --cached | grep 'ml_agents_trial/eda/' | sed 's|src/ml_agents_trial/eda/||')
git commit -m "feat(eda): generate EDA modules

$(echo "$STAGED" | sed 's/^/- /')"
```

9. Report shape, missing values, task type, top features, commit hash, and next step (`/ml-engineer`).
