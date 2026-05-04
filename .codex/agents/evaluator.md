# evaluator

Use this role for `codex command: evaluate`. Generate evaluation plots and report code under `src/ml_agents_trial/evaluation/`.

## Required Reading

- `.codex/skills/tabular-ml-quality/SKILL.md`
- `.codex/skills/artifact-contracts/SKILL.md`
- `artifacts/eda/data_summary.json`
- `artifacts/models/comparison.json`

## Required Outputs

Implement `src/ml_agents_trial/evaluation/plots.py` with:

- `plot_predictions(...)`
- `plot_residuals(...)`
- `plot_feature_importance(...)`
- `plot_model_comparison(...)`

Implement `src/ml_agents_trial/evaluation/report.py` with:

- `generate_report(comparison_path: Path | None = None) -> dict`
- `evaluate_all_models(X_test, y_test, target: str) -> None`
- a `__main__` block that evaluates saved models.

## Rules

- Use `apply_patch` for edits and `exec_command` for validation commands.
- Plot modules must set `matplotlib.use("Agg")` before importing `pyplot`.
- Generate model plots under `artifacts/models/*/plots/`.
- Write an evaluation summary compatible with `artifacts/evaluation/report_summary.json` when possible.
- Preserve artifact contracts and best-model rules.
- Do not use Claude-specific tool names, named-agent calls, or hook syntax.
