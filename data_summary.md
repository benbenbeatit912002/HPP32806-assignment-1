# Gas Exchange Data Summary

## Location

Data folder:

```text
C:\HPP32806\Files\assignment_1\Data
```

Notebook:

```text
C:\HPP32806\Files\assignment_1\Load_data.ipynb
```

## Overall Structure

This dataset contains LI-COR 6800 gas exchange data. The files are separated into training and validation sets.

| Dataset | Number of files | Rows | Columns per file |
|---|---:|---:|---:|
| Training | 6 | 33,923 | 279 |
| Validation | 5 | 28,303 | 279 |
| Total | 11 | 62,226 | 279 |

Each file records approximately 8 hours of gas exchange measurements.

## Files

### Training Files

| File | Rows | Time range |
|---|---:|---|
| 2023-08-25-1038_logdata_silvere2_flash | 5,688 | 2023-08-25 10:38:36 to 18:38:48 |
| 2023-08-30-1101_logdata_silvere2_flash | 5,671 | 2023-08-30 11:02:04 to 19:02:19 |
| 2023-09-06-1204_logdata_silvere2_flash | 5,685 | 2023-09-06 12:05:04 to 20:05:03 |
| 2023-09-22-1242_logdata_silvere2_flash | 5,642 | 2023-09-22 12:44:07 to 20:44:06 |
| 2023-10-24-1257_logdata_silvere2_flash | 5,669 | 2023-10-24 12:57:48 to 20:57:43 |
| 2023-10-24-1300_logdata2_silvere2_flash | 5,568 | 2023-10-24 13:00:45 to 21:00:48 |

### Validation Files

| File | Rows | Time range |
|---|---:|---|
| 2023-08-28-1128_logdata_silvere3_flash | 5,717 | 2023-08-28 11:29:00 to 19:29:10 |
| 2023-09-04-1143_logdata_silvere3_flash | 5,684 | 2023-09-04 11:44:32 to 19:44:33 |
| 2023-10-03-1126_logdata_silvere3_flash | 5,654 | 2023-10-02 11:27:12 to 19:27:09 |
| 2023-10-18-1319_logdata_silvere3_flash | 5,633 | 2023-10-18 13:19:56 to 21:20:21 |
| 2023-10-18-1323_logdata2_silvere3_flash | 5,615 | 2023-10-18 13:23:25 to 21:24:02 |

## Main Data Types

The 279 columns can be grouped into several major categories.

| Category | Example columns | Description |
|---|---|---|
| Time and index | `obs`, `time`, `elapsed`, `date`, `hhmmss` | Observation number, elapsed time, and timestamp |
| Sample information | `Plant_ID` | Plant identifier. This column is currently empty in the loaded data. |
| Gas exchange | `A`, `E`, `Emm`, `Ca`, `Ci`, `gsw`, `gbw` | Photosynthesis, transpiration, CO2, and stomatal conductance |
| Environmental conditions | `Tleaf`, `Tair`, `RHcham`, `VPDleaf`, `Qin`, `CO2_r`, `H2O_r` | Leaf temperature, air temperature, humidity, light, CO2, and water vapor |
| Fluorescence | `Fo`, `Fm`, `Fs`, `Fv/Fm`, `PhiPS2`, `ETR`, `NPQ` | Chlorophyll fluorescence and photosystem II related variables |
| Instrument status | `Flow_s`, `Flow_r`, `Fan`, `Pump`, `Tboard`, `DIAG`, `ADC_*`, `DAC_*` | LI-COR instrument flow, fan, pump, diagnostics, and sensor status |

## Important Columns

| Column | Meaning |
|---|---|
| `A` | Net photosynthetic assimilation rate |
| `E` | Transpiration rate |
| `Emm` | Transpiration rate in mmol units |
| `gsw` | Stomatal conductance to water vapor |
| `Ca` | Ambient/reference CO2 concentration |
| `Ci` | Intercellular CO2 concentration |
| `Qin` | Incoming light intensity |
| `Tleaf` | Leaf temperature |
| `Tair` | Air temperature |
| `RHcham` | Chamber relative humidity |
| `VPDleaf` | Leaf vapor pressure deficit |
| `PhiPS2` | Effective quantum yield of photosystem II |
| `Fo`, `Fm`, `Fs` | Fluorescence measurements |
| `Fv/Fm` | Maximum quantum efficiency of photosystem II |

## Summary Statistics

| Column | Meaning | Training mean | Validation mean |
|---|---|---:|---:|
| `A` | Photosynthesis rate | 11.03 | 11.26 |
| `E` | Transpiration rate | 0.0024 | 0.0024 |
| `Emm` | Transpiration in mmol | 2.44 | 2.37 |
| `gsw` | Stomatal conductance | 0.285 | 0.279 |
| `Ci` | Intercellular CO2 | 329.60 | 326.18 |
| `Ca` | Ambient CO2 | 395.32 | 395.13 |
| `Qin` | Incoming light | 594.49 | 618.23 |
| `CO2_r` | Reference CO2 | 400.12 | 400.00 |
| `H2O_r` | Reference water vapor | 17.26 | 17.20 |
| `Tleaf` | Leaf temperature | 22.44 | 22.45 |
| `Tair` | Air temperature | 23.00 | 23.00 |
| `RHcham` | Chamber relative humidity | 65.02 | 65.04 |
| `VPDleaf` | Leaf vapor pressure deficit | 0.89 | 0.89 |
| `PhiPS2` | PSII quantum yield | 0.0147 | 0.0144 |
| `Fo` | Minimum fluorescence | 11.31 | 11.20 |
| `Fm` | Maximum fluorescence | 43.10 | 42.12 |
| `Fs` | Steady-state fluorescence | 12.28 | 11.96 |
| `Fv/Fm` | PSII maximum efficiency | 0.0299 | 0.0297 |

## Data Quality Notes

Some columns contain extreme or unrealistic values and should be cleaned before analysis or modeling.

Examples:

| Column | Issue observed |
|---|---|
| `A` | Training data ranges from about -4145 to 4264, which is likely unrealistic. |
| `Tleaf` | Training data has a maximum value around 395, likely an invalid reading. |
| `CO2_r` | Training data has values up to about 3953, much higher than the normal reference CO2 level. |
| `Ci` | Contains negative values and very large values. |
| `Plant_ID` | Currently empty in the loaded data. |

These unusual values may come from instrument warm-up, transition periods, unstable measurements, or invalid records. They should be filtered before building a model.

## Short Interpretation

This dataset contains time-series measurements from LI-COR 6800 gas exchange experiments. Each row represents one measurement time point. The most useful variables for analysis are likely:

```text
A, gsw, E, Emm, Ci, Ca, Qin, Tleaf, Tair, RHcham, VPDleaf, PhiPS2
```

The training and validation folders can be used separately for model development and model evaluation.
