---
name: artifact-contracts
description: Claude Code ML Pipeline の各段階が読み書きする artifacts JSON の期待キー、意味、互換性ルールを定義するSkill。
---

# artifact-contracts

このSkillは `model-architect`, `evaluator`, `reporter`, `ml-reviewer` が参照する。目的は、前段のAI生成物に後段が暗黙依存して壊れることを防ぐこと。

## General Rules

- JSONは `ml_agents_trial.core.io.save_json()` / `load_json()` を使って読み書きする。
- 既存キーの意味を変えない。新しい情報は追加キーとして足す。
- 後段が参照するキーが欠けている場合は、例外で落とすか、明示的なfallback値を資料に出す。
- モデル名、ターゲット列、タスク種別、主要指標はartifact間で同じ表記にする。

## `artifacts/eda/data_summary.json`

期待キー:

- `shape`: `[rows, columns]` または同等の行列情報。
- `dtypes`: 列名から型名へのマッピング。
- `missing_values`: 列名から欠損数へのマッピング。
- `target`: ターゲット列名。既存実装にない場合も追加を推奨する。
- `target_stats`: ターゲットの要約統計またはクラス分布。
- `task_type`: `"regression"` または `"classification"`。
- `top_features`: ターゲットとの関連が高い特徴量名リスト。

## `artifacts/models/<model_name>/metrics.json`

期待キー:

- `model`: モデル名。
- `task_type`: `"regression"` または `"classification"`。
- `metrics`: 指標名から値へのマッピング。既存互換のため、トップレベルに `rmse`, `mae`, `r2`, `accuracy`, `f1` などを併記してもよい。
- `train_time_sec`: 学習時間。
- `n_train`: 学習行数。
- `n_test`: テスト行数。

## `artifacts/models/comparison.json`

期待形式:

- モデル比較行のlistを基本形にする。
- 各行は `model`, `task_type`, `train_time_sec` と主要指標を持つ。
- 回帰行は `rmse`, `mae`, `r2` を持つ。
- 分類行は `accuracy`, `f1` を持つ。
- best modelは回帰なら `rmse` 最小、分類なら `f1` 最大、なければ `accuracy` 最大で判定できること。

## `artifacts/evaluation/report_summary.json`

期待キー:

- `target`: ターゲット列名。
- `task_type`: `"regression"` または `"classification"`。
- `best_model`: best model名。
- `best_metric`: best model選定に使った指標名。
- `model_count`: 比較したモデル数。
- `evaluation_method`: 分割方法や評価方法の説明。
- `limitations`: 評価上の限界のlist。
- `next_steps`: 次に検証すべき改善案のlist。

## Reviewer Pass Criteria

`ml-reviewer` は以下を満たせばPASSにする。

- 後続commandが必要とするartifactが存在する、または生成コードが作成する。
- 主要キーの欠落がない。
- best model選定に必要な指標が `comparison.json` から読める。
- reporterが必要な前提、限界、次アクションをartifactから取得できる。
