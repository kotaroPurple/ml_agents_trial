import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

from ml_agents_trial.core.config import ARTIFACTS_EDA, ARTIFACTS_MODELS, ARTIFACTS_PRESENTATION


def collect_slide_data() -> dict:
    """全 artifacts を1つの dict に集約して返す"""
    data: dict = {}

    # --- EDA summary ---
    eda_summary_path = ARTIFACTS_EDA / "data_summary.json"
    if eda_summary_path.exists():
        with eda_summary_path.open() as f:
            eda = json.load(f)
    else:
        eda = {}
    data["eda"] = eda

    # --- models comparison ---
    comparison_path = ARTIFACTS_MODELS / "comparison.json"
    if comparison_path.exists():
        with comparison_path.open() as f:
            comparison = json.load(f)
    else:
        comparison = []
    data["comparison"] = comparison

    # --- report summary (optional) ---
    report_summary_path = ARTIFACTS_MODELS / "report_summary.json"
    if report_summary_path.exists():
        with report_summary_path.open() as f:
            report_summary = json.load(f)
    else:
        report_summary = {}
    data["report_summary"] = report_summary

    # --- derive best model ---
    best_model_name: str = ""
    if report_summary.get("best_model"):
        best_model_name = report_summary["best_model"]
    elif comparison:
        # comparison は list[dict]。r2 最大のものをベストとする
        best_entry = max(comparison, key=lambda m: m.get("r2", float("-inf")))
        best_model_name = best_entry.get("model_name", "")
    data["best_model_name"] = best_model_name

    # --- copy plot images to artifacts/presentation/images/ ---
    images_dir = ARTIFACTS_PRESENTATION / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    copied_images: dict = {}  # logical_key -> filename (relative to images/)

    # EDA plots
    for eda_plot in (ARTIFACTS_EDA / "plots").glob("*.png"):
        dest = images_dir / eda_plot.name
        shutil.copy2(eda_plot, dest)
        copied_images[f"eda_{eda_plot.stem}"] = eda_plot.name

    # Model-level plots
    for model_dir in ARTIFACTS_MODELS.iterdir():
        if not model_dir.is_dir():
            continue
        plots_dir = model_dir / "plots"
        if not plots_dir.exists():
            continue
        for plot_file in plots_dir.glob("*.png"):
            dest_name = f"{model_dir.name}__{plot_file.name}"
            dest = images_dir / dest_name
            shutil.copy2(plot_file, dest)
            copied_images[f"{model_dir.name}_{plot_file.stem}"] = dest_name

    # Aggregate model comparison plot
    agg_plots_dir = ARTIFACTS_MODELS / "plots"
    if agg_plots_dir.exists():
        for plot_file in agg_plots_dir.glob("*.png"):
            dest = images_dir / plot_file.name
            shutil.copy2(plot_file, dest)
            copied_images[f"models_{plot_file.stem}"] = plot_file.name

    data["copied_images"] = copied_images

    return data


def _build_dataset_overview(eda: dict) -> str:
    shape = eda.get("shape", {})
    rows = shape.get("rows", "N/A")
    cols = shape.get("cols", "N/A")
    task_type = eda.get("task_type", "N/A")
    missing = eda.get("missing", {})
    missing_count = len(missing)
    lines = [
        f"- 行数: **{rows:,}** / 列数: **{cols}**",
        f"- タスク種別: **{task_type}**",
        f"- 欠損のある列: **{missing_count}**",
    ]
    return "\n".join(lines)


def _build_target_stats(eda: dict) -> str:
    stats = eda.get("target_stats", {})
    if not stats:
        return ""
    lines = [
        "| 統計量 | 値 |",
        "|--------|-----|",
        f"| 平均 | {stats.get('mean', 'N/A'):.4f} |",
        f"| 標準偏差 | {stats.get('std', 'N/A'):.4f} |",
        f"| 最小 | {stats.get('min', 'N/A'):.4f} |",
        f"| 中央値 | {stats.get('50%', 'N/A'):.4f} |",
        f"| 最大 | {stats.get('max', 'N/A'):.4f} |",
    ]
    return "\n".join(lines)


def _build_eda_findings(eda: dict, copied_images: dict) -> str:
    lines = []
    task_type = eda.get("task_type", "regression")
    top_features = eda.get("top_features", [])

    if task_type == "regression":
        lines.append("- ターゲットは連続値 (回帰タスク)")
    else:
        lines.append("- ターゲットはカテゴリ値 (分類タスク)")

    missing = eda.get("missing", {})
    if missing:
        lines.append(f"- 欠損値あり: {', '.join(missing.keys())}")
    else:
        lines.append("- 欠損値なし")

    if top_features:
        lines.append(f"- 主要特徴量: {', '.join(top_features[:5])}")

    # 分布プロットを挿入
    if "eda_distributions" in copied_images:
        lines.append("")
        lines.append(f"![distributions](images/{copied_images['eda_distributions']})")

    return "\n".join(lines)


def _build_top_features(eda: dict, copied_images: dict) -> str:
    top_features = eda.get("top_features", [])
    lines = []
    if top_features:
        lines.append("| 順位 | 特徴量名 |")
        lines.append("|------|----------|")
        for i, feat in enumerate(top_features[:10], 1):
            lines.append(f"| {i} | `{feat}` |")

    # 相関ヒートマップ
    if "eda_correlation_heatmap" in copied_images:
        lines.append("")
        lines.append(f"![correlation heatmap](images/{copied_images['eda_correlation_heatmap']})")

    return "\n".join(lines)


def _build_model_comparison_rows(comparison: list) -> str:
    if not comparison:
        return "| (データなし) | - | - | - | - |"
    rows = []
    for m in comparison:
        name = m.get("model_name", "N/A")
        rmse = m.get("rmse", "N/A")
        mae = m.get("mae", "N/A")
        r2 = m.get("r2", "N/A")
        train_time = m.get("train_time_sec", "N/A")
        rows.append(f"| {name} | {rmse} | {mae} | {r2} | {train_time} |")
    return "\n".join(rows)


def _build_best_model_plots(best_model_name: str, copied_images: dict) -> str:
    lines = []
    pred_key = f"{best_model_name}_predictions"
    resid_key = f"{best_model_name}_residuals"
    if pred_key in copied_images:
        lines.append(f"![predictions](images/{copied_images[pred_key]})")
    if resid_key in copied_images:
        lines.append(f"![residuals](images/{copied_images[resid_key]})")
    if not lines:
        lines.append("(プロットなし)")
    return "\n".join(lines)


def _build_best_feature_importance_plot(best_model_name: str, copied_images: dict) -> str:
    key = f"{best_model_name}_feature_importance"
    if key in copied_images:
        return f"![feature importance](images/{copied_images[key]})"
    return "(特徴量重要度プロットなし)"


def _build_conclusions(eda: dict, comparison: list, best_model_name: str) -> str:
    lines = []
    task_type = eda.get("task_type", "regression")
    top_features = eda.get("top_features", [])

    if best_model_name and comparison:
        best = next((m for m in comparison if m.get("model_name") == best_model_name), None)
        if best:
            r2 = best.get("r2", "N/A")
            rmse = best.get("rmse", "N/A")
            lines.append(f"- **{best_model_name}** が最高性能 (R²={r2}, RMSE={rmse})")

    if task_type == "regression":
        lines.append("- 回帰タスクとして適切なモデル群を評価")
    else:
        lines.append("- 分類タスクとして適切なモデル群を評価")

    if top_features:
        lines.append(f"- 最重要特徴量: **{top_features[0]}**")

    lines.append("- すべてのモデルは `core/metrics.py` の標準指標で評価")
    return "\n".join(lines)


def _build_next_steps(eda: dict, best_model_name: str) -> str:
    lines = [
        f"1. **{best_model_name}** のハイパーパラメータをさらにチューニング",
        "2. 特徴量エンジニアリングの追加検討 (交互作用項、変換など)",
        "3. より多くのデータで再学習",
        "4. 本番環境へのデプロイ計画",
    ]
    return "\n".join(lines)


def build_slides(slide_data: dict) -> Path:
    """
    src/ml_agents_trial/presentation/templates/base.marp.md を読んで
    artifacts/presentation/slides.md を生成して返す
    """
    template_path = Path(__file__).parent / "templates" / "base.marp.md"
    template = template_path.read_text(encoding="utf-8")

    eda = slide_data.get("eda", {})
    comparison = slide_data.get("comparison", [])
    best_model_name = slide_data.get("best_model_name", "")
    copied_images = slide_data.get("copied_images", {})
    task_type = eda.get("task_type", "regression")

    # ターゲット列名の推定: dtypes の最後のキーをターゲットとみなす
    dtypes = eda.get("dtypes", {})
    target_column = list(dtypes.keys())[-1] if dtypes else "target"

    now_str = datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M UTC")

    placeholder_map: dict[str, str] = {
        "{{TITLE}}": "ML パイプライン 実験レポート",
        "{{SUBTITLE}}": f"データセット: California Housing | タスク: {task_type}",
        "{{GENERATION_TIMESTAMP}}": now_str,
        "{{DATASET_OVERVIEW}}": _build_dataset_overview(eda),
        "{{TARGET_COLUMN}}": target_column,
        "{{TARGET_STATS}}": _build_target_stats(eda),
        "{{EDA_FINDINGS}}": _build_eda_findings(eda, copied_images),
        "{{TOP_FEATURES}}": _build_top_features(eda, copied_images),
        "{{MODEL_COMPARISON_ROWS}}": _build_model_comparison_rows(comparison),
        "{{BEST_MODEL_NAME}}": best_model_name,
        "{{BEST_MODEL_PLOTS}}": _build_best_model_plots(best_model_name, copied_images),
        "{{BEST_FEATURE_IMPORTANCE_PLOT}}": _build_best_feature_importance_plot(
            best_model_name, copied_images
        ),
        "{{CONCLUSIONS}}": _build_conclusions(eda, comparison, best_model_name),
        "{{NEXT_STEPS}}": _build_next_steps(eda, best_model_name),
    }

    content = template
    for placeholder, value in placeholder_map.items():
        content = content.replace(placeholder, value)

    ARTIFACTS_PRESENTATION.mkdir(parents=True, exist_ok=True)
    out_path = ARTIFACTS_PRESENTATION / "slides.md"
    out_path.write_text(content, encoding="utf-8")

    return out_path


if __name__ == "__main__":
    data = collect_slide_data()
    out = build_slides(data)
    print(f"DONE: {out}")
