"""Original model equations; lag rates are per retained observation, not per second."""

import numpy as np
import pandas as pd


def photosynthesis_light_response(Qin, Amax, K, Rd):
    """Simulate assimilation from light only. Measured A is not used here."""
    Qin = np.asarray(Qin, dtype=float)
    return (Amax * Qin) / (K + Qin + 1e-9) - Rd


def empirical_light_vpd_model(Qin, VPDleaf, params):
    """Model 0: empirical light and VPD response."""
    g0, a, Kq, D0 = params
    Qin = np.asarray(Qin, dtype=float)
    VPDleaf = np.asarray(VPDleaf, dtype=float)
    return g0 + a * Qin / (Kq + Qin + 1e-9) * 1 / (1 + VPDleaf / D0)


def leuning_1995_model(Qin, Ca, VPDleaf, params):
    """Model 1: Leuning-style model using simulated photosynthesis."""
    Amax, K, Rd, g0, gL, Gamma, D0 = params
    A_model = photosynthesis_light_response(Qin, Amax, K, Rd)
    denominator = (1 + np.asarray(VPDleaf, dtype=float) / D0) * (np.asarray(Ca, dtype=float) - Gamma)
    return g0 + gL * A_model / (denominator + 1e-9)


def dynamic_leuning_model(df, params):
    """Model 2: Leuning target with a first-order stomatal time lag, reset by file."""
    Amax, K, Rd, g0, gL, Gamma, D0, k_lag = params
    target_params = [Amax, K, Rd, g0, gL, Gamma, D0]

    output = pd.Series(index=df.index, dtype=float)
    groups = df.groupby("_file", sort=False) if "_file" in df.columns else [(None, df)]

    for _, group in groups:
        target = leuning_1995_model(group["Qin"], group["Ca"], group["VPDleaf"], target_params)
        target = np.asarray(target, dtype=float)

        dynamic = np.empty_like(target)
        if len(target) == 0:
            continue

        dynamic[0] = np.clip(group["gsw"].iloc[0], 0, 0.6)
        for i in range(1, len(target)):
            dynamic[i] = dynamic[i - 1] + k_lag * (target[i] - dynamic[i - 1])

        output.loc[group.index] = dynamic

    return output.to_numpy()


def predict_model(model_name, params, df):
    if model_name == "Model 0":
        return empirical_light_vpd_model(df["Qin"], df["VPDleaf"], params)
    if model_name == "Model 1":
        return leuning_1995_model(df["Qin"], df["Ca"], df["VPDleaf"], params)
    if model_name == "Model 2":
        return dynamic_leuning_model(df, params)
    if model_name == "Model 3":
        return asymmetric_dynamic_leuning_model(df, params)
    raise ValueError(f"Unknown model: {model_name}")


def asymmetric_dynamic_leuning_model(df, params):
    """Model 3: Leuning target with separate opening and closing lag parameters."""
    Amax, K, Rd, g0, gL, Gamma, D0, k_open, k_close = params
    target_params = [Amax, K, Rd, g0, gL, Gamma, D0]

    output = pd.Series(index=df.index, dtype=float)
    groups = df.groupby("_file", sort=False) if "_file" in df.columns else [(None, df)]

    for _, group in groups:
        target = leuning_1995_model(group["Qin"], group["Ca"], group["VPDleaf"], target_params)
        target = np.asarray(target, dtype=float)

        dynamic = np.empty_like(target)
        if len(target) == 0:
            continue

        dynamic[0] = np.clip(group["gsw"].iloc[0], 0, 0.6)
        for i in range(1, len(target)):
            if target[i] > dynamic[i - 1]:
                k = k_open
            else:
                k = k_close
            dynamic[i] = dynamic[i - 1] + k * (target[i] - dynamic[i - 1])

        output.loc[group.index] = dynamic

    return output.to_numpy()
