"""Cleaning rules preserved from the original analysis notebook."""

import pandas as pd


MODEL_COLUMNS = ["gsw", "Qin", "Ca", "VPDleaf", "Tleaf", "Tair", "RHcham", "A", "elapsed"]


OUTLIER_FILTERS = {
    "gsw": (0, 0.6),
    "Qin": (0, 2000),
    "Ca": (300, 500),
    "VPDleaf": (0, 2),
    "Tleaf": (15, 35),
    "Tair": (15, 35),
    "RHcham": (30, 90),
}


def remove_gsw_spikes(df, gsw_col="gsw", window=21, threshold=0.08):
    """Remove isolated gsw spikes using a centered rolling median filter."""
    if gsw_col not in df.columns:
        return df.copy()

    filtered_df = df.copy()
    gsw = pd.to_numeric(filtered_df[gsw_col], errors="coerce")
    rolling_median = gsw.rolling(window=window, center=True, min_periods=5).median()
    deviation = (gsw - rolling_median).abs()
    keep = rolling_median.isna() | (deviation <= threshold)
    return filtered_df[keep].copy()


def prepare_model_data(df):
    """Create a modelling copy with numeric variables and modelling-specific outlier filters."""
    model_df = df.copy()
    initial_rows = len(model_df)

    for col in MODEL_COLUMNS:
        if col in model_df.columns:
            model_df[col] = pd.to_numeric(model_df[col], errors="coerce")

    # Required model variables. Measured A is kept for evaluation only and is not
    # used as an input for predicting gsw.
    required = ["gsw", "Qin", "Ca", "VPDleaf", "Tleaf", "Tair", "RHcham", "A"]
    missing = sorted(set(required) - set(model_df.columns))
    if missing:
        raise ValueError(f"Missing model columns: {missing}")
    model_df = model_df.dropna(subset=required)
    after_missing = len(model_df)

    for col, (lower, upper) in OUTLIER_FILTERS.items():
        if col in model_df.columns:
            model_df = model_df[model_df[col].between(lower, upper)].copy()

    # A is not used as a predictor. This optional filter removes clearly
    # unrealistic assimilation values so the A_model vs measured A diagnostic
    # plot is not dominated by instrument artefacts.
    if "A" in model_df.columns:
        model_df = model_df[model_df["A"].between(-10, 50)].copy()

    print(
        "Model data cleaning: "
        f"{initial_rows:,} rows -> {after_missing:,} after missing-value removal -> "
        f"{len(model_df):,} after outlier filters"
    )

    return model_df.reset_index(drop=True)


def combine_data_dict(data_dict):
    """Combine a dictionary of dataframes and preserve the source file name."""
    frames = []
    for filename, df in data_dict.items():
        temp = df.copy()
        temp["_file"] = filename
        frames.append(temp)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)
