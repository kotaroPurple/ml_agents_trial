---
agent: "agent"
description: "Generate feature engineering code from EDA artifacts"
---

# ML Engineer

Target column: `${input:target_column:MedHouseVal}`

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
2. Implement `src/ml_agents_trial/features/engineer.py` with `build_features(df, target)` and a `__main__` block.
3. Do not transform the target column. Avoid target leakage and all-data statistics.
4. Structurally review imports, ruff, and `__main__`.
5. Perform ML quality review for leakage, target mutation, and EDA consistency. Return to implementation if review fails.
6. Run:

```bash
.venv/bin/python src/ml_agents_trial/features/engineer.py data/raw/house_prices.csv ${input:target_column:MedHouseVal}
```

7. Run `uv run ruff check src/ tests/`.
8. Commit only `src/ml_agents_trial/features/` with `feat(features): generate feature engineering module`.
9. Report added features, processed CSV shape, commit hash, and next step.
