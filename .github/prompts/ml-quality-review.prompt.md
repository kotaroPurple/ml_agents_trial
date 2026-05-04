---
agent: "agent"
description: "Review generated ML pipeline code and artifacts for domain quality (phase-based)"
---

# ML Quality Review

Phase: `${input:phase:features}` — `eda` / `features` / `models` / `evaluation` / `report`
Target: `${input:target:src/ml_agents_trial/}`

Load the skills for the specified phase before reviewing:

| Phase | Skills to load | Focus |
|---|---|---|
| eda | artifact-contracts | `data_summary.json` required key contract |
| features | tabular-ml-quality, artifact-contracts | leakage, target mutation, all-data stats, EDA consistency |
| models | tabular-ml-quality, artifact-contracts | task type, model set, baseline, metrics, best-model rule, artifact keys |
| evaluation | tabular-ml-quality, artifact-contracts | evaluation method, overfitting checks, `report_summary.json` keys |
| report | artifact-contracts, ml-reporting | artifact consistency, conclusions, limitations, next actions |

Use:

- [tabular ML quality](../skills/tabular-ml-quality/SKILL.md)
- [artifact contracts](../skills/artifact-contracts/SKILL.md)
- [ML reporting](../skills/ml-reporting/SKILL.md)

Do not edit files. Return PASS or FAIL with concrete fix instructions.

## Output

```text
PASS: [phase] [target]
- Leakage: OK
- Metrics and model selection: OK
- Artifact contracts: OK
- Reporting quality: OK
Residual risk:
- ...
```

or:

```text
FAIL: [phase] [target]
Issues:
- [file:line or artifact] [problem]
Fix instructions:
- [specific requested change]
```
