---
agent: "agent"
description: "Generate evaluation modules, plots, and report summary"
---

# ML Evaluate

Target column: `${input:target_column:MedHouseVal}` (default from copilot-instructions.md > プロジェクト設定)

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
2. Implement evaluation modules in `src/ml_agents_trial/evaluation/` (file structure may vary by complexity):
   - Required public functions: `plot_predictions`, `plot_residuals`, `plot_feature_importance`, `plot_model_comparison`, `evaluate_all_models`, `generate_report`.
   - Generate model plots under `artifacts/models/*/plots/`.
   - Save `report_summary.json` with keys: `best_model`, `best_metric`, `evaluation_method`, `limitations`, `next_steps`.
3. Structurally review: run `/ml-code-review` with target=`src/ml_agents_trial/evaluation/`. Return to implementation if FAIL.
4. ML quality review: run `/ml-quality-review` with phase=`evaluation`, target=`src/ml_agents_trial/evaluation/`. Return to implementation if FAIL.
5. Run:

```bash
.venv/bin/python src/ml_agents_trial/evaluation/report.py ${input:target_column:MedHouseVal}
find artifacts/models -name "*.png" | sort
```

6. Run `uv run ruff check src/ tests/`.
7. Commit only `src/ml_agents_trial/evaluation/` with:

```bash
git add src/ml_agents_trial/evaluation/
STAGED=$(git diff --name-only --cached | grep 'ml_agents_trial/evaluation/' | sed 's|src/ml_agents_trial/evaluation/||')
git commit -m "feat(evaluation): generate evaluation modules

$(echo "$STAGED" | sed 's/^/- /')"
```

8. Report generated plots, commit hash, and next step (`/ml-report`).
