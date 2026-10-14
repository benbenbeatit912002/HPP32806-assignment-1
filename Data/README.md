# LI-6800 gas exchange data

This directory contains the original measurement exports supplied with the HPP32806 assignment. The existing file split is preserved: six files in `Training/` and five in `Validation/`.

The files are tab-separated text without extensions. Each starts with instrument metadata and contains a `[Data]` section followed by group names, variable names, units, and observations. Keep these rows intact; the project parser handles them directly.

The complete dataset contains 62,226 raw observations and occupies approximately 136 MB. Model preparation excludes invalid observations; per-file retained counts are recorded in the [reference manifest](../reports/reference/run_manifest.json).

The validation filename beginning `2023-10-03` contains timestamps dated `2023-10-02`. The original file name and contents are retained. See the [dataset summary](../docs/data_summary.md) for the original inventory and variable descriptions.

These exports were already tracked by the original coursework repository. A separate dataset licence and original measurement-collection attribution are not recorded here; no new redistribution terms are assigned by this reorganisation.
