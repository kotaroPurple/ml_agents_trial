---
applyTo: "src/ml_agents_trial/{features,models,evaluation}/**/*.py"
---

# Tabular ML Quality

Use the detailed Copilot Agent Skill at `.github/skills/tabular-ml-quality/SKILL.md` when generating or reviewing feature engineering, model training, or evaluation code.

Always preserve these short rules:

- Never transform the target column as a feature.
- Do not use test-data statistics in training preprocessing.
- Use `ml_agents_trial.core.metrics` for metrics.
- Regression selects lowest `rmse`; classification selects highest `f1`, otherwise highest `accuracy`.
