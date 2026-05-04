---
agent: "agent"
description: "Set up the ml-agents-trial environment and demo dataset"
---

# ML Setup

Set up this repository for the tabular ML pipeline.

Use repository instructions from [copilot-instructions](../copilot-instructions.md).

## Steps

1. Run `uv venv --python 3.12`.
2. Run `uv pip install -e ".[dev]"`.
3. Verify imports with `.venv/bin/python -c "import pandas, sklearn, lightgbm; print('OK')"`.
4. Download data using the command in copilot-instructions.md > プロジェクト設定 > データ取得コマンド.
5. Verify CSV loading using `ml_agents_trial.core.io.load_csv` (core module from copilot-instructions.md > プロジェクト設定).
6. Report Python/package status and dataset shape.

Do not modify `.claude/` or `.codex/`.
