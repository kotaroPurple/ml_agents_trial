# model-architect

Use this role for `codex command: build`. Generate model configs and training code under `src/ml_agents_trial/models/`.

## Required Reading

- `.codex/skills/tabular-ml-quality/SKILL.md`
- `.codex/skills/artifact-contracts/SKILL.md`
- `artifacts/eda/data_summary.json`

## Required Outputs

Implement `src/ml_agents_trial/models/configs.py`:

- `MODEL_CONFIGS: dict[str, dict]` with class paths and parameters.
- Regression models should include a linear baseline and tree/boosting models.
- Classification models should include simple/linear/tree models.

Implement `src/ml_agents_trial/models/trainer.py`:

- `train_model(name: str, config: dict, X_train, y_train, X_test, y_test) -> dict`
- `train_all(X_train, y_train, X_test, y_test) -> dict`
- a `__main__` block that reads `data/processed/features.csv`, trains all models, and writes `artifacts/models/comparison.json`.

## Rules

- Use `apply_patch` for edits and `exec_command` for validation commands.
- Use `ml_agents_trial.core.metrics` for metrics.
- Save each model to `artifacts/models/{name}/model.pkl`.
- Save each metrics file and `comparison.json` according to artifact contracts.
- Select best model by lowest `rmse` for regression and highest `f1`/`accuracy` for classification.
- Do not use Claude-specific tool names, named-agent calls, or hook syntax.
