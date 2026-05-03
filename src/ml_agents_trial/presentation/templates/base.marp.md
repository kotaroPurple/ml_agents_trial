---
marp: true
theme: default
paginate: true
backgroundColor: "#ffffff"
style: |
  section {
    font-family: 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
    font-size: 26px;
  }
  section.lead h1 {
    font-size: 2em;
    color: #2d6a9f;
  }
  section.lead p {
    color: #555;
  }
  table {
    font-size: 0.75em;
    width: 100%;
  }
  code {
    background: #f4f4f4;
    font-size: 0.85em;
  }
  h2 {
    color: #2d6a9f;
    border-bottom: 2px solid #2d6a9f;
    padding-bottom: 4px;
  }
---

<!-- _class: lead -->

# {{TITLE}}

{{SUBTITLE}}

`Generated: {{GENERATION_TIMESTAMP}}`

---

## データセット概要

{{DATASET_OVERVIEW}}

**ターゲット変数**: `{{TARGET_COLUMN}}`

{{TARGET_STATS}}

---

## EDA: 主要な発見

{{EDA_FINDINGS}}

---

## 特徴量の重要度 (Top 10)

{{TOP_FEATURES}}

---

## モデル比較結果

| モデル | RMSE | MAE | R² | 学習時間(秒) |
|--------|------|-----|-----|------------|
{{MODEL_COMPARISON_ROWS}}

---

## ベストモデル: {{BEST_MODEL_NAME}}

{{BEST_MODEL_PLOTS}}

---

## 特徴量重要度 ({{BEST_MODEL_NAME}})

{{BEST_FEATURE_IMPORTANCE_PLOT}}

---

## 結論

{{CONCLUSIONS}}

---

## 次のステップ

{{NEXT_STEPS}}

---

<!-- _class: lead -->

# ありがとうございました

Claude Code ML Pipeline で自動生成
