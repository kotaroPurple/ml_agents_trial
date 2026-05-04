# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Codex 用の並行ワークフローは `AGENTS.md` と `.codex/` を参照する。Claude Code 用の `.claude/` は維持する。

## プロジェクト設定（他プロジェクト転用時はここを変更）

| 設定項目 | 値 |
|---|---|
| パッケージ名 | `ml_agents_trial` |
| ソースパス | `src/ml_agents_trial/` |
| コアモジュール | `ml_agents_trial.core` |
| デフォルトCSVパス | `data/raw/house_prices.csv` |
| デフォルトターゲット列 | `MedHouseVal` |
| データ取得コマンド | `.venv/bin/python -c "from ml_agents_trial.data.datasets.house_prices import download; download()"` |

## Project Overview

汎用テーブルデータ ML パイプライン。Claude Code の Commands・Subagents・Skills・Hooks を活用して、EDA → 特徴量エンジニアリング → モデル学習 → Marp プレゼン資料生成を自動化する。
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

## Claude Code Commands（実行順）

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
    ml-reviewer.md     — ML品質チェック専門（リーク・指標・artifact・資料妥当性）
  commands/            — Slash command 定義
    setup.md / analyze.md / engineer.md / build.md / evaluate.md / report.md
  skills/              — 共通品質基準
    tabular-ml-quality.md — データリーク防止・評価指標・ベースライン比較
    artifact-contracts.md — artifacts JSON の期待キーと互換性ルール
    ml-reporting.md      — Marp資料の必須構成・限界・次アクション
```

## Commands / Subagents / Skills の責務

- Commands: `/analyze`, `/engineer`, `/build`, `/evaluate`, `/report` の実行順序、前提確認、レビュー、実行、コミット手順を定義する。
- Subagents: 担当領域のコード生成またはレビューを行う。生成系 subagent は `src/` にコードを書き、reviewer は修正指示のみ返す。
- Skills: 複数 subagent で共有する品質基準を定義する。ML妥当性、artifact契約、資料品質は `.claude/skills/` を参照する。
- Hooks: Pythonファイル書き込み後のruff自動実行と、セッション終了時処理を担う。

## Subagent コード生成のルール

各 subagent が `src/` にコードを書くとき（パス・パッケージ名は上記「プロジェクト設定」の値を使う）:
1. `from {コアモジュール}.xxx import ...` のみ依存可（他パッケージへの cross-import 禁止）
2. 各モジュールは `if __name__ == "__main__":` で単独実行できること
3. 生成後は必ず `.venv/bin/python` で実行して動作確認
4. @code-reviewer が構造チェック → メインがドメインレビュー → @ml-reviewer がML品質レビュー → 実行 → git commit

## AI活用上の既知リスク

- ドメイン妥当性: 生成コードが動いても、EDA解釈・特徴量・モデル選択が妥当とは限らない。
- データリーク: 全データ由来の統計量、ターゲット列変換、テスト情報の利用に注意する。
- 評価信頼性: 単純なホールドアウトのみでは、過学習や分割依存を見落とす可能性がある。
- artifact契約不整合: 前段のJSONキー変更により、後段の評価・資料生成が壊れる可能性がある。
- 自動コミット: AI生成物が品質確認前に履歴へ入らないよう、reviewerのPASS後にコミットする。

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
- import が `{コアモジュール}`（プロジェクト設定参照）のみに依存しているか
- `if __name__ == "__main__":` ブロックがあるか
- `ruff check` でエラーがないか

ドメインロジックのレビュー（メインが担当）:
- EDA 結果と特徴量変換の根拠が一致しているか
- タスク種別に合ったモデルが選ばれているか

## ml-reviewer の役割

ML品質チェック（sonnet で実行）:
- `.claude/skills/tabular-ml-quality.md` に沿って、ターゲットリーク、前処理、指標、ベースライン、過学習確認をレビューする
- `.claude/skills/artifact-contracts.md` に沿って、`data_summary.json`, `comparison.json`, `metrics.json`, `report_summary.json` の整合性を確認する
- `.claude/skills/ml-reporting.md` に沿って、資料に目的・評価方法・限界・次アクションが含まれるか確認する

## Key Conventions

- タスク種別は `artifacts/eda/data_summary.json` の `task_type` フィールドで管理（`"regression"` or `"classification"`）
- 評価指標は `core/metrics.py` の関数を必ず使う（独自実装禁止）
- artifacts パスは必ず `core/config.py` の定数経由で参照する
- ML品質基準は `.claude/skills/tabular-ml-quality.md`、artifact契約は `.claude/skills/artifact-contracts.md`、資料品質は `.claude/skills/ml-reporting.md` を参照する
- Python ファイルを書き込むと ruff が自動実行される（PostToolUse hook）
