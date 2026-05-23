# Damour et al. (2010) Stomatal Conductance Review Summary

Source PDF:

```text
C:\Users\chris\OneDrive - Wageningen University & Research\datadriven\Plant Cell Environment - 2010 - DAMOUR - An overview of models of stomatal conductance at the leaf level.pdf
```

## Paper Information

**Title:** An overview of models of stomatal conductance at the leaf level  
**Authors:** Gaelle Damour, Thierry Simonneau, Herve Cochard, Laurent Urban  
**Journal:** Plant, Cell & Environment, 33, 1419-1438  
**Year:** 2010  
**DOI:** 10.1111/j.1365-3040.2010.02181.x

## Main Purpose

This review summarizes models of stomatal conductance (`gs`) at the leaf level, ranging from empirical models to more mechanistic models.

The main question is how stomata respond to multiple environmental and physiological drivers, especially under drought or limited water supply.

The paper emphasizes that stomata control both:

- water loss through transpiration, and
- CO2 uptake for photosynthesis.

Therefore, stomatal conductance models are important for predicting plant water use, photosynthesis, drought response, and crop performance under changing climate conditions.

## Why This Paper Is The Correct Main Reference

This paper is directly relevant to the assignment because the current project predicts `gsw` from LI-6800 leaf-level environmental variables.

The dataset contains variables such as:

```text
gsw, Qin, Ca, VPDleaf, Tleaf, Tair, RHcham, A
```

Damour et al. (2010) reviews the main families of models that explain or predict stomatal conductance from exactly these kinds of variables:

- light intensity,
- CO2 concentration,
- vapour pressure deficit,
- leaf temperature,
- photosynthesis,
- water stress and hydraulic status.

This paper supports the choice of a Leuning-type stomatal conductance model and explains why measured assimilation (`A`) should be treated carefully.

## Core Biological Ideas

Stomata regulate a trade-off:

```text
maximize CO2 uptake for photosynthesis
while limiting water loss by transpiration
```

The review highlights several important controls on stomatal conductance:

| Driver | Meaning for stomatal conductance |
|---|---|
| Light | Usually increases stomatal opening and photosynthesis |
| CO2 | Higher CO2 often reduces stomatal conductance |
| VPD / humidity | Higher atmospheric water demand usually reduces conductance |
| Leaf temperature | Affects both photosynthesis and transpiration demand |
| Photosynthesis | Many models link `gs` to `Anet` |
| Soil/leaf water status | Drought often reduces `gs` through hydraulic and chemical signals |
| ABA | A chemical drought signal involved in stomatal closure |

## Major Families Of Stomatal Conductance Models

### 1. Climatic Or Empirical Multiplicative Models

These models predict `gs` as a product of independent response functions.

A general Jarvis-type model is:

```math
g_s = f_1(Q) f_2(T_l) f_3(VPD) f_4(C_a) f_5(\Psi_l)
```

where:

| Symbol | Meaning |
|---|---|
| `Q` | light intensity |
| `T_l` | leaf temperature |
| `VPD` | vapour pressure deficit |
| `C_a` | ambient CO2 concentration |
| `Psi_l` | leaf water potential |

Strengths:

- practical and flexible,
- can represent multiple environmental effects,
- useful for prediction when enough calibration data are available.

Weaknesses:

- assumes each factor acts independently,
- requires many parameters,
- less mechanistic,
- response curves may not transfer well across conditions.

### 2. Simple Humidity / VPD Response Models

Some models use VPD as the main driver.

Lohammer-type response:

```math
g_s = \frac{g_0}{1 + VPD / D_0}
```

Monteith-type response:

```math
g_s = g_{smax} - a \cdot VPD
```

These are simple but incomplete because they ignore photosynthesis and CO2 effects.

### 3. Ball-Berry Model

Ball, Woodrow & Berry (1987) proposed a widely used empirical model linking stomatal conductance to photosynthesis, humidity, and CO2.

A common form is:

```math
g_s = g_0 + g_1 \frac{A_{net} H_r}{C_s}
```

where:

| Symbol | Meaning |
|---|---|
| `g_s` | stomatal conductance |
| `g_0` | residual/minimum stomatal conductance |
| `g_1` | empirical slope parameter |
| `A_net` | net CO2 assimilation rate |
| `H_r` | relative humidity |
| `C_s` | CO2 concentration at the leaf surface |

Strengths:

- practical,
- widely used,
- captures the strong relation between `gs` and photosynthesis.

Weaknesses:

- uses relative humidity instead of VPD,
- does not fully handle the CO2 compensation point,
- does not directly represent drought or soil water limitation.

### 4. Leuning Models

Leuning modified the Ball-Berry model to better represent CO2 and VPD responses.

Leuning 1990 includes the CO2 compensation point:

```math
g_s = g_0 + g_L \frac{A_{net}}{C_s - \Gamma}
```

Leuning 1995 adds a VPD response:

```math
g_s = g_0 + \frac{g_L A_{net}}{(1 + VPD / D_0)(C_s - \Gamma)}
```

In the current assignment prototype, this is adapted as:

```math
gsw_{pred} = g_0 + \frac{g_L A_{model}}{(1 + VPDleaf / D_0)(C_a - \Gamma)}
```

where `A_model` is simulated from light rather than using measured `A` directly.

Parameter meanings:

| Parameter | Meaning |
|---|---|
| `g0` | residual/minimum stomatal conductance |
| `gL` | Leuning slope or stomatal sensitivity parameter |
| `A_model` | simulated net assimilation |
| `D0` | VPD sensitivity parameter |
| `Gamma` | CO2 compensation-point-like parameter |
| `Ca` or `Cs` | ambient or leaf-surface CO2 concentration |

Why this model is useful here:

- it directly uses `Qin`, `Ca`, and `VPDleaf`,
- it is biologically interpretable,
- it is one of the major literature-supported stomatal conductance models,
- it avoids using measured `A` as a direct predictor if `A_model` is simulated.

### 5. Coupled Photosynthesis-Stomatal Models

Damour et al. note that Ball-Berry and Leuning models are often coupled with a photosynthesis submodel because `A_net`, `g_s`, and internal CO2 concentration (`C_i`) are interdependent.

The CO2 supply relationship can be written conceptually as:

```math
A_{net} = g_s (C_s - C_i)
```

or equivalently:

```math
g_s = \frac{A_{net}}{C_s - C_i}
```

A full coupled model can solve for:

```text
gs, Anet, Ci
```

using:

1. a stomatal conductance equation,
2. a CO2 diffusion/supply equation,
3. a biochemical photosynthesis equation, such as Farquhar-type photosynthesis.

The assignment prototype uses a simpler light-response equation for `A_model`:

```math
A_{model} = \frac{A_{max} Q_{in}}{K + Q_{in}} - R_d
```

This is simpler than a full Farquhar model but keeps the key rule: measured `A` is not used as an input to predict `gsw`.

### 6. Drought, Hydraulic, And ABA-Based Models

A major message of Damour et al. is that many common `gs` models work well under well-watered conditions but perform poorly under drought.

Water stress can be represented through:

- predawn water potential,
- leaf water potential,
- soil water potential,
- whole-plant hydraulic conductance,
- ABA concentration,
- embolism risk.

#### Hydraulic Model Concept

Some models assume stomata close to prevent xylem water potential from dropping below a cavitation threshold.

A simple hydraulic idea is:

```math
E_{crit} = K_{tot}(\Psi_s - \Psi_{cav})
```

where:

| Symbol | Meaning |
|---|---|
| `Ecrit` | critical transpiration threshold |
| `Ktot` | total soil-to-leaf hydraulic conductance |
| `Psi_s` | soil water potential |
| `Psi_cav` | cavitation threshold water potential |

If transpiration approaches the threshold, stomata close to avoid hydraulic failure.

#### Tuzet-Type Model

Tuzet et al. (2003) combines a Leuning-type model with a water-potential stress function.

Conceptually:

```math
g_s = g_0 + f(\Psi_l) \cdot \frac{g_L A_{net}}{C_i - \Gamma}
```

where `f(Psi_l)` reduces stomatal conductance under water stress.

The stress function is often sigmoidal, meaning conductance remains high under mild stress but drops strongly after a threshold.

#### ABA-Based Models

ABA models represent chemical signalling from roots or leaves during drought.

General idea:

```text
higher ABA concentration -> stronger stomatal closure -> lower gs
```

These models can simulate drought responses better, but they require ABA measurements or submodels, which are usually not available in LI-6800 gas exchange datasets.

## Important Equations For This Assignment

### Simple Light And VPD Baseline

This corresponds to Model 0 in the notebook:

```math
gsw_{pred} = g_0 + a \frac{Q_{in}}{K_q + Q_{in}} \frac{1}{1 + VPDleaf / D_0}
```

This is inspired by the idea that stomata open with light and close with increasing VPD.

### Simulated Photosynthesis Light Response

```math
A_{model} = \frac{A_{max} Q_{in}}{K + Q_{in}} - R_d
```

This is not a full photosynthesis model, but it provides a simple way to avoid using measured `A` as a predictor.

### Leuning 1995 Prototype

```math
gsw_{pred} = g_0 + \frac{g_L A_{model}}{(1 + VPDleaf / D_0)(C_a - \Gamma)}
```

This is the main literature-based model used in the notebook.

### Dynamic Stomatal Lag

Damour et al. mention that stomatal response under fluctuating conditions may deviate from steady state, although most reviewed models assume steady states.

A simple dynamic extension is:

```math
gsw_t = gsw_{t-1} + k_{lag}(gsw_{target,t} - gsw_{t-1})
```

This allows stomatal conductance to respond gradually instead of instantly.

## Relation To The Current LI-6800 Dataset

| Dataset column | Role in modelling |
|---|---|
| `gsw` | target variable |
| `Qin` | light response driver |
| `Ca` | CO2 driver in Leuning model |
| `VPDleaf` | water-demand / stomatal closure driver |
| `Tleaf` | modelling filter and possible future predictor |
| `Tair` | modelling filter and possible future predictor |
| `RHcham` | humidity-related predictor or diagnostic variable |
| `A` | evaluation only; not used directly as input |

## Why Measured A Should Not Be Used Directly

Many stomatal models use assimilation as a driver, but in this assignment the goal is to predict `gsw` from environmental variables.

Using measured `A` directly would cause information leakage because measured assimilation is already a plant response measured at the same time as `gsw`.

Therefore, the notebook uses:

```text
Qin -> A_model -> gsw_pred
```

instead of:

```text
measured A -> gsw_pred
```

Measured `A` can still be used to evaluate whether the simulated `A_model` is physiologically reasonable.

## Model Choice Recommendation

For this assignment, the best interpretation is:

1. Use Model 0 as a simple empirical baseline.
2. Use Model 1, Leuning 1995 with simulated photosynthesis, as the main literature-based steady-state model.
3. Use Model 2 as an improved prototype for fluctuating-light or time-series conditions.

This is consistent with Damour et al. because:

- the review identifies Ball-Berry and Leuning models as widely used and practical,
- Leuning improves Ball-Berry by using VPD and a CO2 compensation term,
- the review notes the importance of dynamic response under fluctuating environments,
- drought and hydraulic models are important but require variables not available in the current dataset.

## Limitations

The current prototype still has limitations relative to the full review:

- It does not include soil water status or leaf water potential.
- It does not include ABA signalling.
- It does not solve a fully coupled `gs-Anet-Ci` system.
- It uses a simple light-response equation instead of a full Farquhar photosynthesis model.
- It assumes the same parameters across all files.
- It does not include long-term acclimation, drought morphology effects, or hydraulic conductance.

## Future Improvements

Possible next steps:

- Replace the simple `A_model` with a Farquhar photosynthesis model.
- Add mesophyll conductance if CO2 diffusion limitations become important.
- Add hydraulic or water stress variables if leaf water potential, soil water potential, or substrate moisture data become available.
- Add ABA or drought signalling components if chemical or proxy measurements are available.
- Fit separate parameters for different treatments, species, or environmental regimes.
- Use dynamic opening and closing rates instead of one shared `k_lag`.

## Short Takeaway

Damour et al. (2010) supports using Leuning-type stomatal conductance models for this project because they connect stomatal conductance with photosynthesis, CO2, and VPD.

For the current dataset, the most appropriate practical prototype is:

```text
Qin -> simulated A_model -> Leuning gsw prediction using Ca and VPDleaf
```

Measured `A` should remain an evaluation variable, not a direct model input.
