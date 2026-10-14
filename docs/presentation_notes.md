# Presentation planning notes

Notes retained from the original coursework notebook.

## Slide Plan for a 10-Minute Presentation

| Slide | Title | Key points | Figure/table to use | Speaker notes |
|---:|---|---|---|---|
| 1 | Title | Research question; predicting stomatal conductance under fluctuating light | Title slide with model schematic | State the biological problem and modelling goal clearly. |
| 2 | Introduction & Context | `gsw` controls CO2 uptake and water loss; photosynthesis-transpiration trade-off | Simple stomata / gas exchange diagram | Explain why stomatal conductance matters for plant performance. |
| 3 | Dataset Description | LI-COR 6800 data; 6 Training files; 5 Validation files; target and predictors | Dataset summary table | Mention that measured `A` is not used directly for `gsw` prediction. |
| 4 | Conceptual / Forrester Diagram | Inputs, photosynthesis sub-model, stomatal model, dynamic state, output | Forrester / conceptual model diagram | Use this slide to orient the audience before equations. |
| 5 | Model Progression | Model 0 to Model 3; increasing physiological structure and dynamics | Model progression flowchart | Explain why each model was added. |
| 6 | Model Equations | `A_model`; Leuning target; dynamic lag; asymmetric lag | Equation slide | Keep equations short and explain terms verbally. |
| 7 | One-Stage Parameter Fitting | Training `gsw` used to fit model parameters; Validation kept separate | Parameter fitting workflow diagram | Emphasize that fitted parameters are fixed during validation simulation. |
| 8 | Model Comparison | RMSE, R2, Bias for Models 0-3 | Clean comparison table and validation RMSE bar plot | Highlight Model 2 as best validation model and Model 3 as the asymmetric extension. |
| 9 | Model 3 Time-Series | Dynamic prediction; validation shape; remaining mismatch | Model 3 validation time-series | Discuss peaks, lags, and leaf/file variation. |
| 10 | Sensitivity Analysis | Parameters perturbed +/-10%; validation RMSE response | Model 3 sensitivity bar plot | Identify which parameters most influence prediction. |
| 11 | Residual Models / Future Extension | LSTM overfitting risk; Ridge as simpler correction | LSTM/Ridge validation comparison plot | Present residual models as exploratory extensions. |
| 12 | Conclusions | Main findings; limitations; future work | Final conclusion bullets | End with Model 2 validation performance, Model 3 interpretation, and future improvements. |

## Figure Recommendations for the Final Presentation

Recommended figures and tables to keep:

- Forrester / conceptual model diagram showing environmental inputs, photosynthesis sub-model, stomatal model, dynamic state, and predicted `gsw`.
- One-stage parameter fitting workflow diagram.
- Clean Model 0-3 model comparison table.
- Model 0 Validation time-series as a simple baseline.
- Model 2 and Model 3 Validation time-series to compare best validation performance with asymmetric dynamics.
- Model 3 sensitivity analysis bar plot.
- LSTM residual Training vs Validation plot as an exploratory overfitting example.
- Optional: Ridge residual Validation plot if presenting hybrid models as future predictive extensions.
