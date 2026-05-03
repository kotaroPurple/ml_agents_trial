from pathlib import Path

# Repo root (src/ml_agents_trial/core/config.py → 4 levels up)
ROOT = Path(__file__).parent.parent.parent.parent

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS_EDA = ARTIFACTS / "eda"
ARTIFACTS_MODELS = ARTIFACTS / "models"
ARTIFACTS_PRESENTATION = ARTIFACTS / "presentation"

for _d in [DATA_RAW, DATA_PROCESSED, ARTIFACTS_EDA, ARTIFACTS_MODELS, ARTIFACTS_PRESENTATION]:
    _d.mkdir(parents=True, exist_ok=True)
