---
agent: "agent"
description: "Generate EDA modules and artifacts for a CSV target"
---

# ML Analyze

CSV path: `${input:csv_path:data/raw/house_prices.csv}`
Target column: `${input:target_column:MedHouseVal}`

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)
- #file:../../src/ml_agents_trial/core/config.py
- #file:../../src/ml_agents_trial/core/io.py

## Role

Act as the data analyst for this repository.

## Tasks

1. Confirm the CSV exists.
2. Implement `src/ml_agents_trial/eda/analysis.py` with `summarize_dataset`, `detect_task_type`, `find_top_features`, and a `__main__` block.
3. Implement `src/ml_agents_trial/eda/plots.py` with distribution and correlation plots.
4. Structurally review imports, ruff, and `__main__`.
5. Run:

```bash
.venv/bin/python src/ml_agents_trial/eda/analysis.py ${input:csv_path:data/raw/house_prices.csv} ${input:target_column:MedHouseVal}
```

6. Generate EDA plots.
7. Run `uv run ruff check src/ tests/`.
8. Commit only `src/ml_agents_trial/eda/` with `feat(eda): generate EDA modules`.
9. Report shape, missing values, task type, top features, commit hash, and next step.
