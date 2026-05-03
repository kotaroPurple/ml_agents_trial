---
description: EDA から Marp スライドまでのパイプラインを一括実行する。/analyze → /engineer → /build → /evaluate → /report を順番に呼び出す。
---

`$ARGUMENTS` の形式: `[CSV_PATH] [TARGET_COLUMN]`
- CSV_PATH 未指定: `data/raw/house_prices.csv`
- TARGET_COLUMN 未指定: `MedHouseVal`

## 前提確認

`[CSV_PATH]` が存在するか確認してください。
存在しない場合は「先に `/setup` を実行してください」と伝えて終了。

## 実行順序

各ステップが完了したことを確認してから次へ進んでください。
いずれかのステップで失敗した場合はそこで停止し、エラー内容を報告してください。

### Step 1 — EDA
`/analyze [CSV_PATH] [TARGET_COLUMN]` スキルを呼び出してください。

### Step 2 — 特徴量エンジニアリング
`/engineer [TARGET_COLUMN]` スキルを呼び出してください。

### Step 3 — モデル学習
`/build [TARGET_COLUMN]` スキルを呼び出してください。

### Step 4 — 評価
`/evaluate [TARGET_COLUMN]` スキルを呼び出してください。

### Step 5 — レポート生成
`/report` スキルを呼び出してください。

## 完了報告

```bash
git log --oneline -6
```

を実行して各ステップのコミットを確認し、以下を報告してください:
- ベストモデル名と主要指標
- 生成されたスライド: `artifacts/presentation/slides.html`
