---
agent: "agent"
description: "Review generated ML pipeline code and artifacts for domain quality"
---

# ML Quality Review

Target path or artifact: `${input:target:src/ml_agents_trial/}`

Use:

- [tabular ML quality](../skills/tabular-ml-quality/SKILL.md)
- [artifact contracts](../skills/artifact-contracts/SKILL.md)
- [ML reporting](../skills/ml-reporting/SKILL.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)

Do not edit files. Return PASS or FAIL with concrete fix instructions.

## Checks

- Feature code: target leakage, target mutation, all-data statistics, EDA consistency.
- Model code: task type, model set, baseline comparison, metrics, best-model rule, artifact saving.
- Evaluation code: evaluation method, overfitting checks, plots, `report_summary.json`.
- Presentation code: artifact consistency, evaluation method, limitations, next actions, conclusion strength.

## Output

Return:

```text
PASS: [target]
- Leakage: OK
- Metrics and model selection: OK
- Artifact contracts: OK
- Reporting quality: OK
Residual risk:
- ...
```

or:

```text
FAIL: [target]
Issues:
- ...
Fix instructions:
- ...
```
