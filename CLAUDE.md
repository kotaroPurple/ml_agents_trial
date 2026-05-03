# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

汎用テーブルデータ ML パイプライン。Claude Code の Skills・Subagents・Hooks を活用して、EDA → 特徴量エンジニアリング → モデル学習 → Marp プレゼン資料生成を自動化する。
分析・特徴量・モデル・評価コードは **subagents が `src/` に生成**する。固定インフラは `src/ml_agents_trial/core/` のみ。

## Setup

```bash
uv venv --python 3.12
uv pip install -e ".[dev]"
```

## Commands

| コマンド | 内容 |
|---|---|
| `pytest tests/` | コアモジュールのテスト |
| `ruff format src/ tests/` | フォーマット |
| `ruff check src/ tests/` | Lint |

## Claude Code Skills（実行順）

| スラッシュコマンド | 説明 |
|---|---|
| `/setup` | venv・依存・データ取得 |
| `/analyze [CSV] [TARGET]` | EDA → `src/eda/` 生成 |
| `/engineer [TARGET]` | 特徴量変換 → `src/features/` 生成 |
| `/build [TARGET]` | モデル学習 → `src/models/` 生成 |
| `/evaluate [TARGET]` | 評価プロット → `src/evaluation/` 生成 |
| `/report` | Marp スライド → `src/presentation/` 生成 |

## Architecture

```
src/ml_agents_trial/
  core/                ← 固定インフラ（agents は変更しない）
    config.py          — ROOT・データ・artifacts のパス定数
    io.py              — load_csv(), save_json(), load_json(), train_test_split_df()
    metrics.py         — compute_regression_metrics(), compute_classification_metrics()
  data/
    datasets/
      house_prices.py  — California Housing → CSV 変換
  eda/                 ← /analyze で data-analyst が生成
    analysis.py        — summarize_dataset(), detect_task_type(), find_top_features()
    plots.py           — plot_distributions(), plot_correlation_heatmap()
  features/            ← /engineer で feature-engineer が生成
    engineer.py        — build_features(df, target) -> pd.DataFrame
  models/              ← /build で model-architect が生成
    configs.py         — MODEL_CONFIGS: dict[str, dict]
    trainer.py         — train_all(X_train, y_train, X_test, y_test) -> dict
  evaluation/          ← /evaluate で evaluator が生成
    plots.py           — plot_predictions(), plot_residuals(), plot_feature_importance()
    report.py          — evaluate_all_models(), generate_report()
  presentation/        ← /report で reporter が生成
    builder.py         — collect_slide_data(), build_slides()
    templates/
      base.marp.md     — Marp テンプレート（固定）

artifacts/             — 実行結果（git管理対象外）
  eda/                 — data_summary.json + plots/
  models/<name>/       — model.pkl + metrics.json + plots/
  models/comparison.json
  presentation/        — slides.md + slides.html

.claude/
  agents/              — Subagent 定義（コード生成専門家）
    data-analyst.md    — eda/ を生成
    feature-engineer.md — features/ を生成
    model-architect.md — models/ を生成
    evaluator.md       — evaluation/ を生成
    reporter.md        — presentation/builder.py を生成
    code-reviewer.md   — 構造チェック専門（import・__main__・ruff）
  commands/            — Skills 定義
    setup.md / analyze.md / engineer.md / build.md / evaluate.md / report.md
```

## Subagent コード生成のルール

各 subagent が `src/` にコードを書くとき:
1. `from ml_agents_trial.core.xxx import ...` のみ依存可（他パッケージへの cross-import 禁止）
2. 各モジュールは `if __name__ == "__main__":` で単独実行できること
3. 生成後は必ず `.venv/bin/python` で実行して動作確認
4. @code-reviewer が構造チェック → メインがドメインレビュー → 実行 → git commit

## Git ワークフロー

各コマンドは最終ステップで生成したモジュールを自動コミットする。

| コマンド | コミット対象 | メッセージプレフィックス |
|---|---|---|
| `/setup` | src/core/, .claude/, tests/, pyproject.toml 等 | `chore: initial project scaffold` |
| `/analyze` | `src/ml_agents_trial/eda/` | `feat(eda):` |
| `/engineer` | `src/ml_agents_trial/features/` | `feat(features):` |
| `/build` | `src/ml_agents_trial/models/` | `feat(models):` |
| `/evaluate` | `src/ml_agents_trial/evaluation/` | `feat(evaluation):` |
| `/report` | `src/ml_agents_trial/presentation/builder.py` | `feat(presentation):` |

パイプライン完了後の git log イメージ:
```
feat(presentation): generate slide builder
feat(evaluation): generate evaluation modules
feat(models): generate model configs and trainer
feat(features): generate feature engineering module
feat(eda): generate EDA modules
chore: initial project scaffold
```

## code-reviewer の役割

構造的な品質チェック（haiku で高速・安価に実行）:
- import が `ml_agents_trial.core` のみに依存しているか
- `if __name__ == "__main__":` ブロックがあるか
- `ruff check` でエラーがないか

ドメインロジックのレビュー（メインが担当）:
- EDA 結果と特徴量変換の根拠が一致しているか
- タスク種別に合ったモデルが選ばれているか

## Key Conventions

- タスク種別は `artifacts/eda/data_summary.json` の `task_type` フィールドで管理（`"regression"` or `"classification"`）
- 評価指標は `core/metrics.py` の関数を必ず使う（独自実装禁止）
- artifacts パスは必ず `core/config.py` の定数経由で参照する
- Python ファイルを書き込むと ruff が自動実行される（PostToolUse hook）
