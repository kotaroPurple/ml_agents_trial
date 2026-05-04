---
name: artifact-contracts
description: Use for Codex work that reads or writes ML pipeline artifacts JSON and must preserve expected keys and compatibility.
---

# Artifact Contracts

Use this skill when generating or reviewing models, evaluation, or presentation code.
Repo-local Codex skills are not assumed to auto-trigger; read this file explicitly when a command or agent lists it as required reading.

## General Rules

- Read/write JSON through `ml_agents_trial.core.io.load_json()` and `save_json()`.
- Preserve existing key meanings; add new keys rather than changing semantics.
- If a downstream-required key is absent, fail clearly or emit an explicit fallback in the report.

## Expected Artifacts

`artifacts/eda/data_summary.json` should expose:

- `shape`
- `dtypes`
- `missing_values`
- `target` when available
- `target_stats`
- `task_type`: `"regression"` or `"classification"`
- `top_features`

`artifacts/models/<model_name>/metrics.json` should expose:

- `model`
- `task_type`
- `metrics` or top-level metric keys
- `train_time_sec`
- `n_train` and `n_test` when available

`artifacts/models/comparison.json` should be a list of model rows with:

- `model`
- `task_type`
- `train_time_sec`
- regression: `rmse`, `mae`, `r2`
- classification: `accuracy`, `f1`

`artifacts/evaluation/report_summary.json` should expose:

- `target`
- `task_type`
- `best_model`
- `best_metric`
- `model_count`
- `evaluation_method`
- `limitations`
- `next_steps`

## Pass Criteria

- Downstream commands can read the artifacts they need.
- Best-model selection can be derived from `comparison.json`.
- Reporter can obtain assumptions, limitations, and next steps.
