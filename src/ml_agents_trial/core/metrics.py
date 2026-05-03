import numpy as np
import pandas as pd


def compute_regression_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))) * 100)
    return {"rmse": round(rmse, 4), "mae": round(mae, 4), "r2": round(r2, 4), "mape": round(mape, 2)}


def compute_classification_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

    acc = float(accuracy_score(y_true, y_pred))
    f1 = float(f1_score(y_true, y_pred, average="weighted"))
    result = {"accuracy": round(acc, 4), "f1": round(f1, 4)}
    try:
        auc = float(roc_auc_score(y_true, y_pred))
        result["auc"] = round(auc, 4)
    except Exception:
        pass
    return result
