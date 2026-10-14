"""Create compact, reproducible figures for the project README."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def save_figures(comparison, validation_df, predictions, output_dir):
    """Plot all model metrics and the first validation file (chosen by filename)."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    colors = ["#94a3b8", "#64748b", "#0f766e", "#d97706"]
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False}):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout="constrained")
        validation = comparison.loc[comparison["Dataset"] == "Validation"]
        for ax, metric, title in zip(axes, ["RMSE", "R2"], ["Validation error · lower is better", "Explained variance · higher is better"]):
            bars = ax.bar(validation["Model"], validation[metric], color=colors)
            ax.bar_label(bars, fmt="%.4f", padding=5, fontsize=10)
            ax.set_title(title, loc="left", fontsize=12, pad=16)
            ax.set_ylabel("RMSE (mol m$^{-2}$ s$^{-1}$)" if metric == "RMSE" else "$R^2$")
            ax.margins(y=0.23)
            ax.set_axisbelow(True)
            ax.grid(axis="y", alpha=0.18)
        fig.suptitle("Stomatal conductance · validation comparison", fontsize=16, weight="bold")
        fig.savefig(output_dir / "model_comparison.png", dpi=180, facecolor="white")
        plt.close(fig)

        filename = sorted(validation_df["_file"].unique())[0]
        mask = (validation_df["_file"] == filename).to_numpy()
        subset = validation_df.loc[mask]
        x = subset["elapsed"].to_numpy() / 3600 if "elapsed" in subset else np.arange(len(subset))
        fig, ax = plt.subplots(figsize=(11, 4.5), layout="constrained")
        ax.plot(x, subset["gsw"], color="#334155", alpha=0.65, lw=1, label="Observed")
        for name, color in [("Model 2", "#0f766e"), ("Model 3", "#d97706")]:
            if name in predictions:
                ax.plot(x, np.asarray(predictions[name])[mask], color=color, lw=1.6, label=name)
        ax.set(xlabel="Elapsed time (h)" if "elapsed" in subset else "Observation index", ylabel="$g_{sw}$ (mol m$^{-2}$ s$^{-1}$)")
        ax.set_title(f"Dynamic response on an unseen measurement file\n{filename}", loc="left", fontsize=13, pad=14)
        ax.grid(alpha=0.18)
        ax.legend(frameon=False, ncol=3)
        fig.savefig(output_dir / "validation_timeseries.png", dpi=180, facecolor="white")
        plt.close(fig)
