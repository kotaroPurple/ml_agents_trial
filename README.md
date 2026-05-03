# ml-agents-trial

Claude Code と Codex のエージェント運用を活用した、テーブルデータ向け機械学習パイプライン。

EDA → 特徴量エンジニアリング → モデル学習 → Marp プレゼン資料生成まで、スラッシュコマンド一つで進められる。

---

## コンセプト

このプロジェクトは「コードを手書きしない」ことを前提にしている。

| 役割 | 担当 |
|---|---|
| パイプラインの進行・コードレビュー | メインエージェント（Claude Code または Codex） |
| 各フェーズのコード生成・実行 | Subagents（専門エージェント） |
| フェーズ間の引き渡し | Commands / Skills |
| 品質保証 | 構造レビュー・ML品質レビュー・ruff |

Subagents はデータの特性に合わせた Python コードを `src/ml_agents_trial/` に書き込む。生成されたコードは通常の Python モジュールとして扱え、`pytest` でテストでき、`ruff` で Lint できる。

---

## 前提条件

- Claude Code または Codex が利用可能
- [uv](https://docs.astral.sh/uv/) がインストール済み（`uv --version` で確認）
- Node.js 18 以上（Marp による HTML 変換に使用）

---

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone https://github.com/kotaroPurple/ml_agents_trial.git
cd ml_agents_trial
```

### 2. Claude Code または Codex を起動

```bash
claude
```

Codexで使う場合は、このリポジトリをCodexで開き、`AGENTS.md` の指示に従う。

### 3. セットアップ

Claude Code:

```
/setup
```

Codex:

```
codex command: setup
```

Python 3.12 の仮想環境作成・依存インストール・デモデータ（California Housing）の取得が自動で行われる。

---

## Claude Codeで使う場合

6つのコマンドを順番に実行することで、データ読み込みからプレゼン資料まで完成する。

```
/setup
/analyze data/raw/house_prices.csv MedHouseVal
/engineer MedHouseVal
/build MedHouseVal
/evaluate MedHouseVal
/report
```

Claude Code用の定義は `.claude/` にある。

---

## Codexで使う場合

Codex用の入口は `AGENTS.md`、実行手順は `.codex/commands/`、役割定義は `.codex/agents/`、品質基準は `.codex/skills/` にある。`.claude/` は維持し、Codex作業では `.codex/` を参照する。

Codexでは以下のように依頼する。

```
codex command: setup
codex command: analyze data/raw/house_prices.csv MedHouseVal
codex command: engineer MedHouseVal
codex command: build MedHouseVal
codex command: evaluate MedHouseVal
codex command: report
```

一括実行する場合:

```
codex command: run-pipeline data/raw/house_prices.csv MedHouseVal
```

Codex版はClaude Codeのrepo-local slash commandやnamed subagentに依存しない。Codexは `AGENTS.md` から該当command、agent、skill文書を読み、`apply_patch` と `exec_command` で実行する。

### 各ステップで起きること

```
/analyze
  data-analyst (subagent)
    └─ data/raw/house_prices.csv を読む
    └─ src/ml_agents_trial/eda/analysis.py を書く
    └─ src/ml_agents_trial/eda/plots.py を書く
    └─ 実行して動作確認
  メインがコードをレビュー
  artifacts/eda/ にサマリー JSON・プロットを保存

/engineer
  feature-engineer (subagent)
    └─ artifacts/eda/data_summary.json を読む
    └─ src/ml_agents_trial/features/engineer.py を書く
    └─ 実行して data/processed/features.csv を生成
  メインがコードをレビュー

/build
  model-architect (subagent)
    └─ タスク種別（回帰/分類）を自動判定
    └─ src/ml_agents_trial/models/configs.py を書く
    └─ src/ml_agents_trial/models/trainer.py を書く
    └─ 全モデルを学習して artifacts/models/ に保存
  メインがコードをレビュー
  comparison.json にモデル比較結果を保存

/evaluate
  evaluator (subagent)
    └─ src/ml_agents_trial/evaluation/plots.py を書く
    └─ src/ml_agents_trial/evaluation/report.py を書く
    └─ 予測 vs 実績・残差・特徴量重要度プロットを生成

/report
  reporter (subagent)
    └─ src/ml_agents_trial/presentation/builder.py を書く
    └─ artifacts/ の結果を Marp スライドに変換
  npx @marp-team/marp-cli で HTML 出力
```

---

## 自分のデータで使う

`data/raw/` に CSV を置いて、ターゲット列名を指定するだけで動く。

```
/analyze data/raw/your_data.csv target_column_name
/engineer target_column_name
/build target_column_name
/evaluate target_column_name
/report
```

タスク種別（回帰 / 分類）は `detect_task_type()` が自動判定する。  
判定が間違っていた場合は `/analyze` の後にメインエージェントに伝えれば修正できる。

---

## ディレクトリ構成

```
ml_agents_trial/
├── src/ml_agents_trial/
│   ├── core/                ← 固定インフラ（手を加えない）
│   │   ├── config.py        — パス定数
│   │   ├── io.py            — CSV/JSON 読み書き・split
│   │   └── metrics.py       — 回帰/分類メトリクス
│   ├── data/datasets/
│   │   └── house_prices.py  — California Housing 取得
│   ├── eda/                 ← /analyze で生成
│   ├── features/            ← /engineer で生成
│   ├── models/              ← /build で生成
│   ├── evaluation/          ← /evaluate で生成
│   └── presentation/
│       └── templates/
│           └── base.marp.md ← Marp テンプレート（固定）
│
├── tests/
│   ├── conftest.py          — サンプル DataFrame フィクスチャ
│   └── test_core.py         — core/ のユニットテスト
│
├── data/
│   ├── raw/                 — 元データ CSV（git 管理対象外）
│   └── processed/           — 特徴量変換済み CSV（git 管理対象外）
│
├── artifacts/               — 実行結果（git 管理対象外）
│   ├── eda/                 — data_summary.json・プロット
│   ├── models/              — model.pkl・metrics.json・プロット
│   └── presentation/        — slides.md・slides.html
│
├── hooks/
│   └── on_stop.py           — セッション終了時にリーダーボード表示
│
├── .claude/
│   ├── agents/              — Claude Code Subagent 定義
│   ├── commands/            — Claude Code command 定義
│   └── skills/              — Claude Code 品質基準
│
├── AGENTS.md                — Codex 用入口
└── .codex/
    ├── agents/              — Codex 用役割定義
    ├── commands/            — Codex 用 command 手順
    └── skills/              — Codex Skill 形式の品質基準
```

---

## 生成されたコードの扱い方

Subagents が書いたコードは `src/` に残るため、通常の Python プロジェクトとして扱える。

### テスト

```bash
# core のテスト（常に通る）
pytest tests/test_core.py -q

# 生成されたモジュールのテスト（生成後に追記する）
pytest tests/ -q
```

### Lint・フォーマット

Python ファイルの書き込みごとに ruff が自動実行される（PostToolUse Hook）。手動で実行する場合:

```bash
ruff format src/ tests/
ruff check src/ tests/
```

### 単独実行

各生成モジュールは `if __name__ == "__main__":` で単独実行できる。

```bash
# EDA の再実行
.venv/bin/python src/ml_agents_trial/eda/analysis.py data/raw/house_prices.csv MedHouseVal

# 特徴量エンジニアリングの再実行
.venv/bin/python src/ml_agents_trial/features/engineer.py data/raw/house_prices.csv MedHouseVal

# 学習の再実行
.venv/bin/python src/ml_agents_trial/models/trainer.py MedHouseVal
```

### 手動修正

生成されたコードに問題があれば、通常の Python ファイルとして直接編集できる。  
Claude に修正を依頼する場合は「`src/ml_agents_trial/features/engineer.py` の〇〇を変更してください」と伝えればよい。

---

## 繰り返し実験のワークフロー

### 特徴量を変えて再実験

```
/engineer MedHouseVal
（特徴量を修正したい場合は Claude に直接頼む）
/build MedHouseVal
```

### モデルを追加・変更

`src/ml_agents_trial/models/configs.py` の `MODEL_CONFIGS` に追記する、または Claude に依頼する。

```
src/ml_agents_trial/models/configs.py の MODEL_CONFIGS に XGBoost を追加してください
```

その後:
```
/build MedHouseVal
```

### 別データセットで同じパイプラインを試す

```
/analyze data/raw/new_data.csv label
/engineer label
/build label
/evaluate label
/report
```

`src/` の各モジュールは新しいデータ・ターゲット列に合わせて上書き生成される。

---

## セッション終了時の動作

Claude Code のセッションが終了すると Stop Hook が起動し、`artifacts/` の更新ファイル一覧と最新のモデルリーダーボードが表示される。

```
=== Model Leaderboard ===
  lgbm                  RMSE=0.4523  R²=0.8712
  hgb                   RMSE=0.4801  R²=0.8604
  rf                    RMSE=0.5134  R²=0.8401
  ridge                 RMSE=0.7289  R²=0.7102
```

---

## 技術スタック

| 用途 | ライブラリ |
|---|---|
| データ処理 | pandas, numpy |
| 機械学習 | scikit-learn, lightgbm |
| 可視化 | matplotlib, seaborn, japanize-matplotlib |
| CLI | typer, rich |
| プレゼン | Marp CLI |
| パッケージ管理 | uv |
| Lint/Format | ruff |
| テスト | pytest |
