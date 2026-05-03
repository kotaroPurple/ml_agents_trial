from ml_agents_trial.core.config import ARTIFACTS_EDA
from ml_agents_trial.core.io import load_json

# Regression model configurations
REGRESSION_CONFIGS: dict[str, dict] = {
    "Ridge": {
        "class": "sklearn.linear_model.Ridge",
        "params": {"alpha": 1.0},
    },
    "RandomForestRegressor": {
        "class": "sklearn.ensemble.RandomForestRegressor",
        "params": {"n_estimators": 200, "max_depth": None, "random_state": 42, "n_jobs": -1},
    },
    "HistGradientBoostingRegressor": {
        "class": "sklearn.ensemble.HistGradientBoostingRegressor",
        "params": {"max_iter": 300, "learning_rate": 0.05, "max_depth": 6, "random_state": 42},
    },
    "LGBMRegressor": {
        "class": "lightgbm.LGBMRegressor",
        "params": {
            "n_estimators": 300,
            "learning_rate": 0.05,
            "max_depth": 6,
            "num_leaves": 63,
            "random_state": 42,
            "n_jobs": -1,
            "verbose": -1,
        },
    },
}

# Classification model configurations
CLASSIFICATION_CONFIGS: dict[str, dict] = {
    "LogisticRegression": {
        "class": "sklearn.linear_model.LogisticRegression",
        "params": {"max_iter": 1000, "random_state": 42, "n_jobs": -1},
    },
    "RandomForestClassifier": {
        "class": "sklearn.ensemble.RandomForestClassifier",
        "params": {"n_estimators": 200, "max_depth": None, "random_state": 42, "n_jobs": -1},
    },
    "HistGradientBoostingClassifier": {
        "class": "sklearn.ensemble.HistGradientBoostingClassifier",
        "params": {"max_iter": 300, "learning_rate": 0.05, "max_depth": 6, "random_state": 42},
    },
    "LGBMClassifier": {
        "class": "lightgbm.LGBMClassifier",
        "params": {
            "n_estimators": 300,
            "learning_rate": 0.05,
            "max_depth": 6,
            "num_leaves": 63,
            "random_state": 42,
            "n_jobs": -1,
            "verbose": -1,
        },
    },
}


def get_model_configs() -> dict[str, dict]:
    """Return model configs appropriate for the task type in data_summary.json."""
    summary_path = ARTIFACTS_EDA / "data_summary.json"
    task_type = "regression"
    if summary_path.exists():
        summary = load_json(summary_path)
        task_type = summary.get("task_type", "regression")

    if task_type == "classification":
        return CLASSIFICATION_CONFIGS
    return REGRESSION_CONFIGS


MODEL_CONFIGS: dict[str, dict] = get_model_configs()
