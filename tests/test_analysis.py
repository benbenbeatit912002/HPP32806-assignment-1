"""Scientific invariants and a small end-to-end run; no course data required."""

import json
import tempfile
import unittest
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from stomatal_conductance.cli import main, run_analysis
from stomatal_conductance.data import load_gas_exchange_file, load_model_data, prepare_model_data
from stomatal_conductance.fitting import PARAMETER_BOUNDS
from stomatal_conductance.metrics import calculate_metrics
from stomatal_conductance.models import predict_model


def example_frame():
    return pd.DataFrame({
        "_file": ["a"] * 4 + ["b"] * 4,
        "gsw": [0.2, 0.21, 0.19, 0.22, 0.4, 0.39, 0.41, 0.38],
        "Qin": [0, 800, 100, 1000] * 2, "Ca": [400.0] * 8,
        "VPDleaf": [1.0] * 8, "Tleaf": [22.0] * 8,
        "Tair": [23.0] * 8, "RHcham": [65.0] * 8,
        "A": [10.0] * 8, "elapsed": [0, 5, 10, 15] * 2,
    })


def write_export(path, frame):
    numeric = frame.drop(columns=["_file"], errors="ignore")
    numeric = numeric.assign(LeakPct=0.0)
    header = "[Header]\nInstrument\tLI-6800\n[Data]\n"
    header += "\t".join(["GasEx"] * len(numeric.columns)) + "\n"
    header += "\t".join(numeric.columns) + "\n"
    header += "\t".join(["unit"] * len(numeric.columns)) + "\n"
    path.write_text(header + numeric.to_csv(sep="\t", header=False, index=False), encoding="utf-8")


class ModelTests(unittest.TestCase):
    def test_dynamic_models_reset_at_each_file(self):
        frame = example_frame()
        for name in ("Model 2", "Model 3"):
            with self.subTest(model=name):
                params = PARAMETER_BOUNDS[name]["initial"]
                combined = predict_model(name, params, frame)
                separate = np.concatenate([predict_model(name, params, group) for _, group in frame.groupby("_file", sort=False)])
                np.testing.assert_allclose(combined, separate)
                np.testing.assert_allclose(combined[[0, 4]], frame["gsw"].iloc[[0, 4]])

    def test_predictions_ignore_later_observations_and_measured_assimilation(self):
        frame = example_frame()
        changed = frame.copy()
        changed.loc[[1, 2, 3, 5, 6, 7], "gsw"] = 0.59
        changed["A"] = 12345.0
        for name, spec in PARAMETER_BOUNDS.items():
            with self.subTest(model=name):
                np.testing.assert_allclose(predict_model(name, spec["initial"], frame), predict_model(name, spec["initial"], changed))

    def test_equal_opening_closing_rates_match_symmetric_model(self):
        frame = example_frame()
        params = PARAMETER_BOUNDS["Model 2"]["initial"]
        np.testing.assert_allclose(predict_model("Model 2", params, frame), predict_model("Model 3", [*params, params[-1]], frame))

    def test_unit_lag_reaches_static_target_after_initialization(self):
        frame = example_frame()
        static = PARAMETER_BOUNDS["Model 1"]["initial"]
        expected = predict_model("Model 1", static, frame)
        actual = predict_model("Model 2", [*static, 1.0], frame)
        mask = ~frame.groupby("_file").cumcount().eq(0)
        np.testing.assert_allclose(actual[mask], expected[mask])


class MetricTests(unittest.TestCase):
    def test_bias_sign_and_nonfinite_pairs(self):
        metrics = calculate_metrics([1, 2, np.nan, 4], [2, 3, 5, np.inf])
        self.assertEqual(metrics["RMSE"], 1.0)
        self.assertEqual(metrics["Bias"], 1.0)
        self.assertEqual(metrics["R2"], -3.0)

    def test_constant_target_has_undefined_r_squared(self):
        self.assertTrue(np.isnan(calculate_metrics([1, 1], [1, 1])["R2"]))

    def test_unusable_or_mismatched_arrays_fail(self):
        for observed, predicted in [([], []), ([np.nan], [1]), ([1], [1, 2]), ([[1]], [[1]])]:
            with self.subTest(observed=observed), self.assertRaises(ValueError):
                calculate_metrics(observed, predicted)


class DataTests(unittest.TestCase):
    def test_parser_skips_metadata_and_units_and_deduplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "export"
            path.write_text("[Header]\nmetadata\n[Data]\nGroup\tGroup\tGroup\t\nTIME\tTIME\tTIME_1\t\ns\ts\ts\t\n1\t2\t3\t\n", encoding="utf-8")
            frame = load_gas_exchange_file(path)
            self.assertEqual(list(frame.columns), ["TIME", "TIME_2", "TIME_1"])
            self.assertEqual(frame.iloc[0].tolist(), [1, 2, 3])

    def test_missing_or_truncated_data_header_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "export"
            for text in ("not an instrument export", "[Data]\nGroup\n"):
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_gas_exchange_file(path)

    def test_cleaning_does_not_mutate_input_and_removes_invalid_rows(self):
        frame = example_frame()
        frame.loc[0, "Tleaf"] = 395
        frame.loc[1, "gsw"] = -1
        frame.loc[2, "A"] = 1000
        original = frame.copy(deep=True)
        cleaned = prepare_model_data(frame)
        self.assertEqual(len(cleaned), 5)
        pd.testing.assert_frame_equal(frame, original)

    def test_missing_columns_and_folders_give_actionable_errors(self):
        with self.assertRaisesRegex(ValueError, "Missing model columns"):
            prepare_model_data(pd.DataFrame({"gsw": [0.2]}))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "Training"):
                load_model_data(directory)

    def test_empty_after_filtering_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            training = Path(directory) / "Training"
            training.mkdir()
            frame = example_frame().assign(gsw=5.0)
            write_export(training / "empty", frame)
            with self.assertRaisesRegex(ValueError, "No usable rows"):
                load_model_data(directory)


class PipelineTests(unittest.TestCase):
    def test_pipeline_exports_metrics_figures_and_optimizer_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for split in ("Training", "Validation"):
                folder = root / "Data" / split
                folder.mkdir(parents=True)
                for name, frame in example_frame().groupby("_file"):
                    write_export(folder / name, frame)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                comparison, diagnostics = run_analysis(root / "Data", root / "results", max_nfev=2)
            self.assertEqual(len(comparison), 8)
            self.assertTrue(np.isfinite(comparison[["RMSE", "R2", "Bias"]]).all().all())
            for filename in ("model_comparison.csv", "parameters.json", "run_manifest.json", "model_comparison.png", "validation_timeseries.png"):
                self.assertGreater((root / "results" / filename).stat().st_size, 0)
            manifest = json.loads((root / "results" / "run_manifest.json").read_text())
            self.assertEqual(len(manifest["data"]), 4)
            self.assertEqual(manifest["max_nfev_override"], 2)
            self.assertTrue(all(len(item["sha256"]) == 64 for item in manifest["data"]))
            self.assertFalse(all(item["success"] for item in diagnostics.values()))

    def test_cli_rejects_invalid_optimizer_limit(self):
        with self.assertRaises(SystemExit) as error:
            main(["--max-nfev", "0"])
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
