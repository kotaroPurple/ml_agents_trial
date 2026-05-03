---
description: プロジェクト初期セットアップ。Python 3.12 venv 作成・依存インストール・データ取得を順番に実行し、全プロジェクトファイルを git に初回コミットする。
---

MLプロジェクトを初期セットアップします。以下を**順番に**実行し、各ステップの結果を報告してください。

## Step 1: 仮想環境の作成
```bash
uv venv --python 3.12
```

## Step 2: 依存パッケージのインストール
```bash
uv pip install -e ".[dev]"
```

## Step 3: インストール確認
```bash
.venv/bin/python -c "import pandas, sklearn, lightgbm; print('OK')"
```

## Step 4: データセット取得（California Housing → CSV）
```bash
.venv/bin/python -c "from ml_agents_trial.data.datasets.house_prices import download; download()"
```

## Step 5: core モジュール疎通確認
```bash
.venv/bin/python -c "
from ml_agents_trial.core.config import DATA_RAW, ARTIFACTS_EDA
from ml_agents_trial.core.io import load_csv
df = load_csv(DATA_RAW / 'house_prices.csv')
print(f'dataset: {df.shape}')
"
```

## Step 6: git 初回コミット

まず現在の git 状態を確認してください:
```bash
git status --short
```

コミット対象のファイルをステージして初回コミットを作成してください:
```bash
git add \
  src/ tests/ hooks/ .claude/ \
  pyproject.toml uv.lock .python-version \
  CLAUDE.md README.md .gitignore
git diff --cached --stat
```

差分を確認した上でコミットしてください:
```bash
git commit -m "chore: initial project scaffold

- src/ml_agents_trial/core/: config, io, metrics (fixed infrastructure)
- src/ml_agents_trial/{eda,features,models,evaluation,presentation}/: stubs (to be generated)
- .claude/agents/: data-analyst, feature-engineer, model-architect, evaluator, reporter, code-reviewer
- .claude/commands/: setup, analyze, engineer, build, evaluate, report
- tests/: conftest, test_core
- hooks/on_stop.py: session-end leaderboard"
```

コミット後に確認してください:
```bash
git log --oneline -3
```

## 完了報告

Python バージョン・主要パッケージバージョン・データセット行列数・git コミットハッシュを表形式で報告してください。
失敗したステップで即座に停止し、エラーと修正案を提示してください。
