---
agent: "agent"
description: "Generate evaluation modules, plots, and report summary"
---

# ML Evaluate

Target column: `${input:target_column:MedHouseVal}`

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [tabular ML quality](../skills/tabular-ml-quality/SKILL.md)
- [artifact contracts](../skills/artifact-contracts/SKILL.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)
- #file:../../src/ml_agents_trial/core/config.py
- #file:../../src/ml_agents_trial/core/io.py

## Role

Act as the evaluator for this repository.

## Tasks

1. Confirm `artifacts/models/comparison.json` exists.
2. Implement `src/ml_agents_trial/evaluation/plots.py` and `src/ml_agents_trial/evaluation/report.py`.
3. Generate model plots under `artifacts/models/*/plots/`.
4. Write or update an evaluation summary compatible with `artifacts/evaluation/report_summary.json` when possible.
5. Structurally review imports, ruff, `matplotlib.use("Agg")`, and `__main__`.
6. Perform ML quality review for evaluation method, overfitting checks, best-model rule, artifacts, and plot relevance. Return to implementation if review fails.
7. Run:

```bash
.venv/bin/python src/ml_agents_trial/evaluation/report.py ${input:target_column:MedHouseVal}
find artifacts/models -name "*.png" | sort
```

8. Run `uv run ruff check src/ tests/`.
9. Commit only `src/ml_agents_trial/evaluation/` with `feat(evaluation): generate evaluation modules`.
10. Report generated plots, commit hash, and next step.
