---
agent: "agent"
description: "Generate model training code and train configured models"
---

# ML Build

Target column: `${input:target_column:MedHouseVal}` (default from copilot-instructions.md > プロジェクト設定)

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
3. Implement model modules in `src/ml_agents_trial/models/` (file structure may vary by complexity):
   - Required public functions: `train_model(name, config, X_train, y_train, X_test, y_test) -> dict`, `train_all(X_train, y_train, X_test, y_test) -> dict`.
   - Include a baseline and task-appropriate models.
   - Save each `model.pkl`, each `metrics.json`, and `artifacts/models/comparison.json`.
4. Structurally review: run `/ml-code-review` with target=`src/ml_agents_trial/models/`. Return to implementation if FAIL.
5. ML quality review: run `/ml-quality-review` with phase=`models`, target=`src/ml_agents_trial/models/`. Return to implementation if FAIL.
6. Run:

```bash
.venv/bin/python src/ml_agents_trial/models/trainer.py ${input:target_column:MedHouseVal}
```

7. Run `uv run ruff check src/ tests/`.
8. Commit only `src/ml_agents_trial/models/` with:

```bash
git add src/ml_agents_trial/models/
STAGED=$(git diff --name-only --cached | grep 'ml_agents_trial/models/' | sed 's|src/ml_agents_trial/models/||')
git commit -m "feat(models): generate model configs and trainer

$(echo "$STAGED" | sed 's/^/- /')"
```

9. Report comparison table, best model, commit hash, and next step (`/ml-evaluate`).
