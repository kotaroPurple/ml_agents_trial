---
agent: "agent"
description: "Generate model training code and train configured models"
---

# ML Build

Target column: `${input:target_column:MedHouseVal}`

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [tabular ML quality](../skills/tabular-ml-quality/SKILL.md)
- [artifact contracts](../skills/artifact-contracts/SKILL.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)
- #file:../../src/ml_agents_trial/core/config.py
- #file:../../src/ml_agents_trial/core/io.py
- #file:../../src/ml_agents_trial/core/metrics.py

## Role

Act as the model architect for this repository.

## Tasks

1. Confirm `data/processed/features.csv` exists.
2. Read `artifacts/eda/data_summary.json` for `task_type`.
3. Implement `src/ml_agents_trial/models/configs.py` and `src/ml_agents_trial/models/trainer.py`.
4. Include a baseline and task-appropriate models.
5. Save each `model.pkl`, each `metrics.json`, and `artifacts/models/comparison.json`.
6. Structurally review imports, ruff, and `__main__`.
7. Perform ML quality review for model choice, metrics, best-model rule, and artifacts. Return to implementation if review fails.
8. Run:

```bash
.venv/bin/python src/ml_agents_trial/models/trainer.py ${input:target_column:MedHouseVal}
```

9. Run `uv run ruff check src/ tests/`.
10. Commit only `src/ml_agents_trial/models/` with `feat(models): generate model configs and trainer`.
11. Report comparison table, best model, commit hash, and next step.
