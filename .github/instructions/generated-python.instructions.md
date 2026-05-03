---
applyTo: "src/ml_agents_trial/{eda,features,models,evaluation,presentation}/**/*.py"
---

# Generated Python Phase Code

- Use project infrastructure from `ml_agents_trial.core.*`.
- External packages such as pandas, numpy, sklearn, lightgbm, matplotlib, and seaborn are allowed.
- Avoid cross-imports between generated phase directories, such as importing `ml_agents_trial.eda` from `evaluation`.
- At least one file per generated phase directory must contain `if __name__ == "__main__":`.
- Plot modules must call `matplotlib.use("Agg")` before importing `matplotlib.pyplot`.
- Keep type hints on public functions.
- Validate with `uv run ruff check src/ tests/` and the command-specific execution step.
