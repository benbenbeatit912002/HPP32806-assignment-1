"""Read LI-6800 exports and prepare independent training/validation files."""

from pathlib import Path

import pandas as pd

from ._preprocessing import (
    MODEL_COLUMNS,
    OUTLIER_FILTERS,
    combine_data_dict,
    prepare_model_data,
    remove_gsw_spikes,
)


def load_gas_exchange_file(filepath):
    """Read the [Data] section, preserving duplicate instrument column names.

    LI-6800 exports have a group row, column-name row, and units row after
    the section marker. Blank header columns are excluded from the result.
    Malformed files raise an error instead of silently disappearing.
    """
    filepath = Path(filepath)
    with filepath.open(encoding="utf-8-sig") as handle:
        for index, line in enumerate(handle):
            if line.strip() == "[Data]":
                groups = handle.readline()
                header = handle.readline()
                units = handle.readline()
                break
        else:
            raise ValueError(f"{filepath}: missing [Data] section.")
    if not groups.strip() or not header.strip() or not units.strip():
        raise ValueError(f"{filepath}: incomplete [Data] header.")

    raw_names = header.rstrip("\r\n").split("\t")
    reserved = {name for name in raw_names if name.strip()}
    names, used, keep = [], set(), []
    for raw in raw_names:
        name = raw if raw.strip() else "Unnamed"
        candidate, suffix = name, 0
        while candidate in used or (suffix > 0 and candidate in reserved):
            suffix += 1
            candidate = f"{name}_{suffix}"
        names.append(candidate)
        used.add(candidate)
        if raw.strip():
            keep.append(candidate)
    frame = pd.read_csv(
        filepath, sep="\t", skiprows=index + 4, names=names,
        index_col=False, engine="python", encoding="utf-8-sig",
    )
    return frame[keep]


def raw_files(directory):
    """Return extensionless LI-6800 exports in a deterministic order."""
    directory = Path(directory)
    if not directory.is_dir():
        raise FileNotFoundError(f"Data directory not found: {directory}")
    files = sorted(path for path in directory.iterdir() if path.is_file() and "." not in path.name)
    if not files:
        raise ValueError(f"No extensionless LI-6800 files found in {directory}.")
    return files


def load_clean_folder_for_model(directory, *, leak_threshold=1.0, gs_min=0.0, gs_max=0.6):
    """Apply leak, conductance, and rolling-median QC within each source file."""
    frames = {}
    for path in raw_files(directory):
        frame = load_gas_exchange_file(path)
        if "gsw" not in frame:
            raise ValueError(f"{path.name}: missing required gsw column.")
        if "LeakPct" in frame:
            frame["Leak"] = pd.to_numeric(frame["LeakPct"], errors="coerce")
            frame = frame.loc[frame["Leak"] <= leak_threshold].copy()
        frame["gsw"] = pd.to_numeric(frame["gsw"], errors="coerce")
        frame = frame.loc[frame["gsw"].between(gs_min, gs_max)].copy()
        frame = remove_gsw_spikes(frame)
        if not frame.empty:
            frames[path.name] = frame
    if not frames:
        raise ValueError(f"No usable rows remain after quality control in {directory}.")
    return frames


def load_model_data(data_dir):
    """Load the fixed Training/Validation split without shuffling time-series rows."""
    data_dir = Path(data_dir)
    datasets = []
    for split in ("Training", "Validation"):
        frames = load_clean_folder_for_model(data_dir / split)
        frame = prepare_model_data(combine_data_dict(frames))
        if frame.empty:
            raise ValueError(f"{split}: no rows remain after model filters.")
        datasets.append(frame)
    return tuple(datasets)
