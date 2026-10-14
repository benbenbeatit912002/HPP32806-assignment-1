# Methods and limitations

## Experimental split and quality control

The six `Data/Training` files are used for fitting; the five `Data/Validation` files are used for evaluation. Files are loaded in filename order, and the row order inside each file is preserved. Source names are retained in `_file` so dynamic states reset at experimental boundaries.

The original notebook cleaning rules are retained:

1. If present, require `LeakPct <= 1`.
2. Keep `gsw` between 0 and 0.6 mol m⁻² s⁻¹.
3. Within each file, remove conductance points more than 0.08 from a centred 21-row rolling median, with a minimum of five observations.
4. Require numeric, nonmissing `gsw`, `Qin`, `Ca`, `VPDleaf`, `Tleaf`, `Tair`, `RHcham`, and `A`.
5. Apply the ranges below and reset the combined row index.

| Variable | Retained range |
|---|---|
| `gsw` | 0 to 0.6 |
| `Qin` | 0 to 2000 |
| `Ca` | 300 to 500 |
| `VPDleaf` | 0 to 2 |
| `Tleaf`, `Tair` | 15 to 35 |
| `RHcham` | 30 to 90 |
| `A` | −10 to 50 |

These are experiment-specific filters. Filtering uses the observed target and measured assimilation, so the reported metrics describe a selected subset of measurements. A centred rolling median also uses future neighbouring measurements; this is an offline analysis, not a real-time quality-control system.

## Model progression

Model 0 uses a saturating light response and VPD attenuation:

```math
g_{sw} = g_0 + a\frac{Q}{K_q + Q}\frac{1}{1 + D/D_0}
```

Model 1 simulates assimilation, then computes a Leuning-style target:

```math
A_{model} = \frac{A_{max}Q}{K + Q} - R_d
```

```math
g_{target} = g_0 + \frac{g_L A_{model}}{(1 + D/D_0)(C_a - \Gamma)}
```

Model 2 adds a first-order lag:

```math
g_t = g_{t-1} + k_{lag}(g_{target,t} - g_{t-1})
```

Model 3 selects `k_open` when the target exceeds the previous dynamic value and `k_close` otherwise. Both dynamic models initialise each file using its first observed `gsw`, clipped to the 0–0.6 range. Subsequent predictions do not use observed `gsw` or measured `A` as predictors.

The first point is included in the metrics. Predictions are therefore conditional on an observed initial state. Lag coefficients operate per retained row, with no elapsed-time adjustment. Filtering creates gaps, so these coefficients should not be interpreted directly as rates per second.

## Parameter estimation and evaluation

`scipy.optimize.least_squares` fits all parameters jointly against training `gsw`, with `loss="soft_l1"` and fixed bounds. Models 0–2 allow up to 500 function evaluations; Model 3 allows 700. Initial guesses and bounds are preserved from the original notebook in `fitting.py`.

RMSE is the square root of mean squared error. R² compares residual sum of squares with the observed variation; it is undefined for a constant target. Bias is mean prediction minus observation. Nonfinite pairs are excluded, and an empty evaluation raises an error.

Each retained row contributes equally, so longer files receive more weight. Validation metrics compare candidate models, rather than constitute a final untouched test. Several parameters lie at bounds, and assimilation-scale parameters can trade off against stomatal sensitivity. Good prediction does not establish unique or physiologically identifiable parameter estimates.

## Exploratory notebook extensions

Ridge and LSTM predict residuals of Model 3. Feature scaling is fitted on Training. LSTM windows stay within source-file boundaries. The original residual feature construction uses fixed photosynthesis parameters as a fallback; these differ from the jointly fitted Model 3 parameters.

Ridge uses leave-one-file-out scoring to choose its regularisation value. Its mechanistic base model was fitted on all Training files before this scoring, so those scores are not a fully nested evaluation of the entire hybrid pipeline. A stronger follow-up would refit the mechanistic model inside each fold.

Model 3 sensitivity analysis perturbs one fitted parameter at a time by ±10%, clipping to its bounds. Monte Carlo analysis approximates parameter covariance from the optimizer Jacobian, rejecting draws outside bounds and falling back to independent normal perturbations if necessary. Under robust fitting and active parameter bounds, these bands are exploratory parameter uncertainty ranges, not calibrated predictive intervals. They omit measurement noise and structural model error.

## Reproducing the reference artifacts

Install the exact core versions from `requirements.txt` and run:

```bash
python -m stomatal_conductance --data-dir Data --output-dir outputs
```

Compare the generated CSV with `reports/reference/model_comparison.csv`. The manifest records input hashes, retained counts, Python and core package versions, parameter bounds, and convergence information. Small floating-point differences can occur across numerical libraries and operating systems.
