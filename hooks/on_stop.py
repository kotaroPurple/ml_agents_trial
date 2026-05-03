import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).parent.parent
artifacts = root / "artifacts"
log_path = artifacts / ".session_log.json"

entries: list = []
if log_path.exists():
    try:
        entries = json.loads(log_path.read_text())
    except json.JSONDecodeError:
        entries = []

new_files = [
    str(p.relative_to(root))
    for p in artifacts.rglob("*")
    if p.is_file() and p.name != ".session_log.json"
]

entries.append({"ts": datetime.now(timezone.utc).isoformat(), "files": new_files})
artifacts.mkdir(exist_ok=True)
log_path.write_text(json.dumps(entries, indent=2))

comparison = artifacts / "models" / "comparison.json"
if comparison.exists():
    try:
        data = json.loads(comparison.read_text())
        print("\n=== Model Leaderboard ===")
        sort_key = "rmse" if "rmse" in (data[0] if data else {}) else "accuracy"
        reverse = sort_key == "accuracy"
        for m in sorted(data, key=lambda x: x.get(sort_key, 9999), reverse=reverse):
            if sort_key == "rmse":
                print(f"  {m['model']:20s}  RMSE={m.get('rmse', '?'):.4f}  R²={m.get('r2', '?'):.4f}")
            else:
                print(f"  {m['model']:20s}  Acc={m.get('accuracy', '?'):.4f}  F1={m.get('f1', '?'):.4f}")
        print()
    except Exception:
        pass
