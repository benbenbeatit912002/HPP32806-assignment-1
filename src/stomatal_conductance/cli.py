"""Command-line entry point for the four-model reference experiment."""

import argparse
import hashlib
import json
import platform
import warnings
from importlib.metadata import version
from pathlib import Path

import pandas as pd

from .data import load_model_data, raw_files
from .fitting import PARAMETER_BOUNDS, evaluate_model, fit_model, params_to_array
from .models import predict_model


def run_analysis(data_dir, output_dir, *, max_nfev=None):
    """Fit on Training, evaluate on both splits, and write inspectable artifacts."""
    data_dir, output_dir = Path(data_dir), Path(output_dir)
    train, validation = load_model_data(data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tables, parameters, diagnostics, predictions = [], {}, {}, {}
    for model in PARAMETER_BOUNDS:
        print(f"Fitting {model} on {len(train):,} training rows...", flush=True)
        params, result = fit_model(model, train, max_nfev=max_nfev)
        parameters[model] = params
        diagnostics[model] = {
            "success": bool(result.success), "status": int(result.status),
            "message": result.message, "nfev": int(result.nfev),
            "cost": float(result.cost), "optimality": float(result.optimality),
        }
        if not result.success:
            warnings.warn(f"{model} did not converge: {result.message}", stacklevel=2)
        tables.append(evaluate_model(model, params, train, validation))
        predictions[model] = predict_model(model, params_to_array(model, params), validation)
    comparison = pd.concat(tables, ignore_index=True)
    comparison.to_csv(output_dir / "model_comparison.csv", index=False)
    (output_dir / "parameters.json").write_text(json.dumps(parameters, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "python": platform.python_version(),
        "packages": {name: version(name) for name in ("numpy", "pandas", "scipy", "matplotlib")},
        "max_nfev_override": max_nfev,
        "model_specs": PARAMETER_BOUNDS,
        "optimizer": diagnostics,
        "data": [],
    }
    for split, frame in [("Training", train), ("Validation", validation)]:
        for path in raw_files(data_dir / split):
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            manifest["data"].append({
                "file": f"{split}/{path.name}", "sha256": digest,
                "model_rows": int((frame["_file"] == path.name).sum()),
            })
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    from .reporting import save_figures
    save_figures(comparison, validation, predictions, output_dir)
    print(comparison.round(4).to_string(index=False))
    print(f"Artifacts saved to {output_dir.resolve()}")
    return comparison, diagnostics


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("Data"), help="Folder containing Training/ and Validation/ (default: Data)")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Destination for CSV, JSON, and figures (default: outputs)")
    parser.add_argument("--max-nfev", type=int, help="Optional optimizer evaluation cap for a smoke run; not a reference fit")
    args = parser.parse_args(argv)
    if args.max_nfev is not None and args.max_nfev < 1:
        parser.error("--max-nfev must be positive")
    try:
        _, diagnostics = run_analysis(args.data_dir, args.output_dir, max_nfev=args.max_nfev)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    return 0 if all(item["success"] for item in diagnostics.values()) else 1
