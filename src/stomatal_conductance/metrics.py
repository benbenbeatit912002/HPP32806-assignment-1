"""RMSE, R squared, and bias (prediction minus observation)."""

import numpy as np


def calculate_metrics(y_obs, y_pred):
    y_obs = np.asarray(y_obs, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_obs.shape != y_pred.shape or y_obs.ndim != 1:
        raise ValueError("Observed and predicted values must be matching one-dimensional arrays.")
    mask = np.isfinite(y_obs) & np.isfinite(y_pred)
    y_obs = y_obs[mask]
    y_pred = y_pred[mask]

    if not len(y_obs):
        raise ValueError("No finite observation/prediction pairs available for evaluation.")

    residual = y_obs - y_pred
    rmse = np.sqrt(np.mean(residual ** 2))
    bias = np.mean(y_pred - y_obs)
    ss_res = np.sum(residual ** 2)
    ss_tot = np.sum((y_obs - np.mean(y_obs)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    return {"RMSE": rmse, "R2": r2, "Bias": bias}
