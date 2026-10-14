"""Bounded robust least squares and evaluation on separate files."""

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

from .metrics import calculate_metrics
from .models import predict_model


PARAMETER_BOUNDS = {
    "Model 0": {
        "names": ["g0", "a", "Kq", "D0"],
        "lower": [0, 0, 1, 0.01],
        "upper": [0.1, 5, 3000, 10],
        "initial": [0.02, 1.0, 300, 1.5],
    },
    "Model 1": {
        "names": ["Amax", "K", "Rd", "g0", "gL", "Gamma", "D0"],
        "lower": [0, 1, 0, 0, 0, 0, 0.01],
        "upper": [50, 3000, 10, 0.1, 50, 100, 10],
        "initial": [30, 500, 2, 0.02, 10, 40, 1.5],
    },
    "Model 2": {
        "names": ["Amax", "K", "Rd", "g0", "gL", "Gamma", "D0", "k_lag"],
        "lower": [0, 1, 0, 0, 0, 0, 0.01, 0.001],
        "upper": [50, 3000, 10, 0.1, 50, 100, 10, 1],
        "initial": [30, 500, 2, 0.02, 10, 40, 1.5, 0.15],
    },
}


def fit_model(model_name, train_df, *, max_nfev=None):
    if train_df.empty:
        raise ValueError("Training data are empty after cleaning.")
    spec = PARAMETER_BOUNDS[model_name]
    y_obs = train_df["gsw"].to_numpy(dtype=float)

    def residuals(params):
        y_pred = predict_model(model_name, params, train_df)
        residual = y_pred - y_obs
        return np.nan_to_num(residual, nan=1e3, posinf=1e3, neginf=-1e3)

    result = least_squares(
        residuals,
        x0=np.asarray(spec["initial"], dtype=float),
        bounds=(np.asarray(spec["lower"], dtype=float), np.asarray(spec["upper"], dtype=float)),
        max_nfev=max_nfev if max_nfev is not None else (700 if model_name == "Model 3" else 500),
        loss="soft_l1",
    )

    params = dict(zip(spec["names"], result.x))
    return params, result


def params_to_array(model_name, params):
    return np.asarray([params[name] for name in PARAMETER_BOUNDS[model_name]["names"]], dtype=float)


def evaluate_model(model_name, params, train_df, validation_df):
    param_array = params_to_array(model_name, params)
    rows = []

    for dataset_name, df in [("Training", train_df), ("Validation", validation_df)]:
        y_pred = predict_model(model_name, param_array, df)
        metrics = calculate_metrics(df["gsw"], y_pred)
        rows.append({"Model": model_name, "Dataset": dataset_name, **metrics})

    return pd.DataFrame(rows)


MODEL_3_SPEC = {
    "names": ["Amax", "K", "Rd", "g0", "gL", "Gamma", "D0", "k_open", "k_close"],
    "lower": [0, 1, 0, 0, 0, 0, 0.01, 0.001, 0.001],
    "upper": [35, 3000, 10, 0.1, 50, 100, 10, 1, 1],
    "initial": [25, 500, 2, 0.02, 10, 40, 1.5, 0.75, 0.5],
}

PARAMETER_BOUNDS["Model 3"] = MODEL_3_SPEC


def fit_model_3_asymmetric_dynamic(train_df):
    """Notebook compatibility wrapper; fit only the supplied training frame."""
    return fit_model("Model 3", train_df)


def model_3_params_to_array(params):
    return params_to_array("Model 3", params)


def evaluate_model_3(params, train_df, validation_df):
    return evaluate_model("Model 3", params, train_df, validation_df)
