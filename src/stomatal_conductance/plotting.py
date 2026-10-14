"""Exploratory notebook plots."""

import numpy as np
import matplotlib.pyplot as plt

from .metrics import calculate_metrics


def plot_observed_vs_predicted(y_obs, y_pred, title):
    metrics = calculate_metrics(y_obs, y_pred)

    plt.figure(figsize=(6, 6))
    plt.scatter(y_obs, y_pred, s=8, alpha=0.25)
    lim_min = min(np.nanmin(y_obs), np.nanmin(y_pred))
    lim_max = max(np.nanmax(y_obs), np.nanmax(y_pred))
    plt.plot([lim_min, lim_max], [lim_min, lim_max], color="black", linestyle="--", linewidth=1)
    plt.xlabel("Observed gsw")
    plt.ylabel("Predicted gsw")
    plt.title(f"{title}\nRMSE={metrics['RMSE']:.3f}, R2={metrics['R2']:.3f}, Bias={metrics['Bias']:.3f}")
    plt.tight_layout()
    plt.show()


def plot_timeseries(df, y_pred, title):
    plot_df = df.copy()
    plot_df["gsw_pred"] = y_pred

    if "_file" in plot_df.columns:
        first_file = plot_df["_file"].iloc[0]
        plot_df = plot_df[plot_df["_file"] == first_file].copy()

    if "elapsed" in plot_df.columns:
        x = plot_df["elapsed"] / 3600
        xlabel = "Elapsed time (h)"
    else:
        x = np.arange(len(plot_df))
        xlabel = "Observation index"

    plt.figure(figsize=(10, 4))
    plt.plot(x, plot_df["gsw"], label="Observed gsw", linewidth=1.5)
    plt.plot(x, plot_df["gsw_pred"], label="Predicted gsw", linewidth=1.5)
    plt.xlabel(xlabel)
    plt.ylabel("gsw")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()
