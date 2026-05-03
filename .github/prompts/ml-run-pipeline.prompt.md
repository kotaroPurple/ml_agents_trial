---
agent: "agent"
description: "Run the full ML pipeline from setup/analyze to report"
---

# ML Run Pipeline

CSV path: `${input:csv_path:data/raw/house_prices.csv}`
Target column: `${input:target_column:MedHouseVal}`

Run the workflow by following these prompt files in order:

1. [ml-setup](ml-setup.prompt.md) only if the environment or CSV is missing.
2. [ml-analyze](ml-analyze.prompt.md) with the CSV path and target column.
3. [ml-engineer](ml-engineer.prompt.md) with the target column.
4. [ml-build](ml-build.prompt.md) with the target column.
5. [ml-evaluate](ml-evaluate.prompt.md) with the target column.
6. [ml-report](ml-report.prompt.md).

Stop immediately if any structural review, ML quality review, execution, or validation fails.

At completion, run:

```bash
git log --oneline -6
```

Report the best model, primary metric, generated slides path, and residual risks.
