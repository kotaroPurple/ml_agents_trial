---
name: ml-reporting
description: Use for Codex work that builds or reviews Marp slides for ML experiment reporting.
---

# ML Reporting

Use this skill when generating or reviewing presentation code and slide content.

## Required Content

Generated slides must include:

- Purpose: prediction/classification goal.
- Dataset overview: rows, columns, target, missingness, task type.
- Preprocessing: key transformations and missing/category handling.
- Evaluation method: split method, primary metric, best-model rule.
- Model comparison: compared models and primary metrics.
- Best model: reason and representative plots.
- Limitations: holdout-only, no external validation, possible leakage risk, or other applicable limits.
- Next actions: cross-validation, feature improvement, extra validation, business metric alignment.

## Writing Rules

- Tie conclusions to metrics and evaluation conditions.
- Avoid claims that exceed the evaluation design.
- If plots are missing, state that briefly rather than referencing unavailable images.
- Replace all Marp template placeholders.
- Copy referenced images into `artifacts/presentation/images/` and use relative paths.

## Pass Criteria

- Purpose, evaluation method, limitations, and next actions are present.
- Best-model claims agree with `comparison.json`.
- The deck does not overstate weak evidence.
