---
name: tabular-ml-quality
description: Use for Codex work on tabular ML quality, including leakage prevention, preprocessing, model comparison, metrics, and overfitting checks.
---

# Tabular ML Quality

Use this skill when generating or reviewing `features/`, `models/`, or `evaluation/` code.
Repo-local Codex skills are not assumed to auto-trigger; read this file explicitly when a command or agent lists it as required reading.

## Core Rules

- Never transform the target column as a feature.
- Do not use test-data statistics for training preprocessing or feature selection.
- Prefer `sklearn Pipeline` / `ColumnTransformer` for fit-dependent imputation, encoding, and scaling.
- If `build_features(df, target)` remains a DataFrame transform, do not use target-derived statistics or test-only information.
- Add interaction or log features only when EDA provides a clear column-level reason.

## Model And Metrics

- Regression: compare a linear baseline with non-linear models; primary selection metric is lowest `rmse`.
- Classification: compare simple/linear/tree models; prefer highest `f1`, otherwise highest `accuracy`.
- Use `ml_agents_trial.core.metrics` for metric calculation.
- Set `random_state=42` where supported; set LightGBM `verbose=-1`.

## Evaluation

- Record train/test method and limitations.
- Compare train and test performance when available and flag likely overfitting.
- Use stratified splits for classification where practical; avoid random splits for time-series data.

## Pass Criteria

- No obvious target leakage.
- Task type, model family, metrics, and best-model rule agree.
- Baseline comparison exists or its absence is explained.
- Evaluation limitations can be surfaced to the report.
