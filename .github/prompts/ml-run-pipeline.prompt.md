---
agent: "agent"
description: "Run the full ML pipeline from setup/analyze to report"
---

# ML Run Pipeline

CSV path: `${input:csv_path:data/raw/house_prices.csv}` (default from copilot-instructions.md > プロジェクト設定)
Target column: `${input:target_column:MedHouseVal}` (default from copilot-instructions.md > プロジェクト設定)

Run the workflow by following these prompt files in order. After each step, confirm that both the structural review and ML quality review returned PASS before proceeding to the next step.

1. [ml-setup](ml-setup.prompt.md) — only if the environment or CSV is missing.
2. [ml-analyze](ml-analyze.prompt.md) with the CSV path and target column. Stop if eda ML quality review fails.
3. [ml-engineer](ml-engineer.prompt.md) with the target column. Stop if features ML quality review fails.
4. [ml-build](ml-build.prompt.md) with the target column. Stop if models ML quality review fails.
5. [ml-evaluate](ml-evaluate.prompt.md) with the target column. Stop if evaluation ML quality review fails.
6. [ml-report](ml-report.prompt.md). Stop if report ML quality review fails.

Stop immediately if any structural review, ML quality review, execution, or ruff validation fails. Report the failing step and fix instructions before stopping.

At completion, run:

```bash
git log --oneline -6
```

Report the best model, primary metric, generated slides path (`artifacts/presentation/slides.html`), and residual risks.
