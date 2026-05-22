# GreenLight Literature Summary

Source PDF:

```text
C:\Users\chris\OneDrive - Wageningen University & Research\Thesis_Green Light\greenlight_an_open_source_model_for_greenhouses_w-wageningen_university_and_research_520969.pdf
```

## Paper Information

**Title:** GreenLight - An open source model for greenhouses with supplemental lighting: Evaluation of heat requirements under LED and HPS lamps  
**Authors:** David Katzin, Simon van Mourik, Frank Kempkes, Eldert J. van Henten  
**Journal:** Biosystems Engineering, 194, 61-81  
**Year:** 2020  
**DOI:** 10.1016/j.biosystemseng.2020.03.010  
**Code:** https://github.com/davkat1/GreenLight

## Main Purpose

This paper introduces **GreenLight**, an open-source greenhouse model designed for greenhouses with supplemental lighting.

The main goal is to model how different lighting systems, especially **HPS** and **LED** lamps, affect:

- greenhouse climate,
- crop energy balance,
- lamp heat distribution,
- heating demand,
- energy use.

The important point is that LED lamps and HPS lamps do not only differ in electrical efficiency. They also differ in how the supplied electrical energy becomes:

- photosynthetically active radiation, PAR,
- near-infrared radiation, NIR,
- far-infrared radiation, FIR,
- convective heat,
- removed heat through active cooling.

This matters because the heat emitted by lamps can reduce or increase the demand from the greenhouse heating system.

## Why This Paper Matters For This Project

This paper is useful as a main reference if the thesis or assignment is related to greenhouse climate, plant gas exchange, lighting, or energy balance.

It provides:

- a physical model structure for greenhouse climate,
- equations for heat, radiation, and lamp energy balance,
- a comparison between HPS and LED lighting,
- validation against real greenhouse data,
- useful evaluation metrics such as ME, RMSE, RRMSE, and heating relative error.

For gas exchange or photosynthesis data, the most relevant link is that variables such as light intensity, leaf temperature, air temperature, humidity, CO2, and VPD are all greenhouse climate drivers that influence photosynthesis and stomatal conductance.

## Core Model Idea

GreenLight is based on the Vanthoor greenhouse model and adds components for supplemental lighting.

The Vanthoor model already describes greenhouse climate and crop growth. GreenLight extends it by adding:

| Added state | Meaning |
|---|---|
| `T_Lamp` | top-light lamp temperature |
| `T_IntLamp` | inter-light lamp temperature |
| `T_GroPipe` | grow pipe temperature |
| `T_BlScr` | blackout screen temperature |

It also adds four control inputs:

| Control input | Meaning | Range |
|---|---|---|
| `U_Lamp` | top-lights on/off or intensity | 0 to 1 |
| `U_IntLamp` | inter-lights on/off or intensity | 0 to 1 |
| `U_BoilGro` | boiler valve opening to grow pipes | 0 to 1 |
| `U_BlScr` | blackout screen closure | 0 to 1 |

A value of `0` means no action, and `1` means full action.

## Important Experimental Setup

The model was evaluated using a tomato greenhouse experiment in Bleiswijk, the Netherlands.

| Item | Description |
|---|---|
| Crop | Tomato, *Solanum lycopersicum* cv. Sunstream |
| Period used | 20 October 2009 to 9 February 2010 |
| Time interval | 5 minutes |
| Compartments | one HPS compartment and one LED compartment |
| Floor area | 144 m2 per compartment |
| Lamp PPFD above crop | 170 umol m-2 s-1 in both compartments |
| CO2 setpoint | 1000 ppm |
| Average lamp operation | about 14 hours per day |

### Lighting Systems

| Parameter | HPS | LED |
|---|---:|---:|
| Electrical input, `q_LampMax` | 110 W m-2 | 116 W m-2 |
| Lamp surface area, `A_Lamp` | 0.03 m2 m-2 | 0.05 m2 m-2 |
| PAR fraction, `h_LampPAR` | 0.36 | 0.31 |
| NIR fraction, `h_LampNIR` | 0.22 | 0.02 |
| Top emissivity, `epsilon_TopLamp` | 0.10 | 0.88 |
| Bottom emissivity, `epsilon_BottomLamp` | 0.90 | 0.88 |
| Active cooling fraction, `h_LampCool` | 0 | 0.63 |
| Lamp heat capacity, `cap_Lamp` | 100 J K-1 m-2 | 10 J K-1 m-2 |
| Lamp-air heat exchange, `c_HEC_LampAir` | 0.09 W K-1 m-2 | 2.3 W K-1 m-2 |
| Photons per PAR joule, `z_LampPAR` | 5.0 umol J-1 | 5.2 umol J-1 |
| Efficacy | 1.8 umol J-1 | 1.6 umol J-1 |

## Main Results

### Model Accuracy

The model predicted heating requirements well.

| Quantity | Reported result |
|---|---|
| Heating prediction error | about 7 to 50 MJ m-2 |
| Air temperature RMSE | about 1.74 to 2.04 C |
| Relative humidity RMSE | about 5.52 to 8.5 percentage points |
| CO2 prediction | poorer than temperature and humidity |

The authors considered the heating prediction error small compared with the measured difference in heating demand between HPS and LED compartments.

### Heating Demand

| Compartment | Heating input |
|---|---:|
| HPS | 435 MJ m-2 |
| LED | 785 MJ m-2 |

The LED compartment needed much more heating because much of the LED heat was removed by active cooling.

### Total Energy Picture

| Energy component | HPS | LED |
|---|---:|---:|
| Heating input | 435 MJ m-2 | 785 MJ m-2 |
| Lighting input | 662 MJ m-2 | 676 MJ m-2 |
| Heat removed by LED cooling | 0 MJ m-2 | 426 MJ m-2 |
| Approximate net energy input | 1097 MJ m-2 | 1035 MJ m-2 |

Although the LED compartment required more heating, the net energy input became similar after considering the heat removed by the LED cooling system.

### Lamp Energy Output Distribution

| Output fraction | HPS | LED |
|---|---:|---:|
| PAR | 36% | 31% |
| NIR | 22% | 2% |
| FIR | 32.5% | 2.37% |
| Convective heat | 9.5% | 1.63% |
| Active cooling | 0% | 63% |

This is one of the most important findings: HPS releases much more radiative heat, while LED energy is largely removed by cooling in this experiment.

## Important Equations

The exact model has many state equations. Below are the most useful equations for understanding and reusing the paper.

### 1. General Energy Balance Form

Most temperature states follow this form:

```math
cap_x \frac{dT_x}{dt} = \sum \text{incoming fluxes} - \sum \text{outgoing fluxes}
```

where:

| Symbol | Meaning |
|---|---|
| `cap_x` | heat capacity of object or state `x` |
| `T_x` | temperature of object or state `x` |
| `H` | conductive or convective heat flux, W m-2 |
| `R` | radiative heat flux, W m-2 |
| `L` | latent heat flux, W m-2 |

### 2. Greenhouse Air Temperature Balance

A simplified form of the greenhouse air energy balance is:

```math
cap_{Air}\frac{dT_{Air}}{dt}
= H_{CanAir} + H_{PipeAir} + R_{GlobSunAir}
- H_{AirFlr} - H_{AirThScr} - H_{AirOut} - H_{AirTop} - H_{AirBlScr}
+ H_{LampAir} + R_{LampAir} + H_{IntLampAir} + H_{GroPipeAir}
```

Interpretation:

- air gains heat from canopy, heating pipes, sunlight, lamps, inter-lights, and grow pipes;
- air loses heat to floor, screens, outside air, top compartment, and blackout screen.

This equation is useful if your project connects greenhouse climate to gas exchange because `T_Air` influences leaf temperature, humidity, VPD, and photosynthesis.

### 3. Canopy Temperature Balance

A simplified canopy balance is:

```math
cap_{Can}\frac{dT_{Can}}{dt}
= R_{PAR,SunCan} + R_{NIR,SunCan} + R_{PipeCan}
- H_{CanAir} - L_{CanAir}
- R_{CanCov} - R_{CanFlr} - R_{CanSky} - R_{CanThScr} - R_{CanBlScr}
+ R_{PAR,LampCan} + R_{NIR,LampCan} + R_{FIR,LampCan}
+ R_{PAR,IntLampCan} + R_{NIR,IntLampCan} + R_{FIR,IntLampCan}
+ R_{GroPipeCan}
```

Interpretation:

- the canopy gains energy from sunlight, lamps, inter-lights, heating pipes, and grow pipes;
- it loses energy through convection, transpiration-related latent heat, and longwave radiation.

This is directly relevant to plant physiology because canopy temperature and radiation affect transpiration and photosynthesis.

### 4. Lamp Temperature Balance

For top-lights:

```math
cap_{Lamp}\frac{dT_{Lamp}}{dt}
= Q_{LampIn}
- R_{LampSky} - R_{LampCov} - R_{LampThScr} - R_{LampBlScr}
- H_{LampAir}
- R_{PAR,LampCan} - R_{NIR,LampCan} - R_{FIR,LampCan}
- R_{LampPipe}
- R_{PAR,LampFlr} - R_{NIR,LampFlr} - R_{FIR,LampFlr}
- R_{LampAir}
- H_{LampCool}
```

Interpretation:

- electrical input heats the lamp;
- energy leaves as PAR, NIR, FIR, convective heat, and active cooling.

For inter-lights:

```math
cap_{IntLamp}\frac{dT_{IntLamp}}{dt}
= Q_{IntLampIn}
- H_{IntLampAir}
- R_{PAR,IntLampCan}
- R_{NIR,IntLampCan}
- R_{FIR,IntLampCan}
```

### 5. Lamp Electrical Input

Top-light input:

```math
Q_{LampIn} = U_{Lamp} q_{LampMax}
```

Inter-light input:

```math
Q_{IntLampIn} = U_{IntLamp} q_{IntLampMax}
```

where:

| Symbol | Meaning |
|---|---|
| `U_Lamp` | lamp control signal, 0 to 1 |
| `q_LampMax` | maximum electrical input of top-lights, W m-2 |
| `U_IntLamp` | inter-light control signal, 0 to 1 |
| `q_IntLampMax` | maximum electrical input of inter-lights, W m-2 |

### 6. Lamp PAR Output

```math
R_{PAR,GhLamp} = h_{LampPAR} Q_{LampIn}
```

where `h_LampPAR` is the fraction of lamp electrical input converted into PAR.

### 7. Lamp NIR Output

```math
R_{NIR,LampCan} = h_{LampNIR} Q_{LampIn}(1-r_{CanNIR})(1-e^{-K_{NIR}LAI})
```

where:

| Symbol | Meaning |
|---|---|
| `h_LampNIR` | fraction of lamp input converted to NIR |
| `r_CanNIR` | canopy reflectivity for NIR |
| `K_NIR` | extinction coefficient for NIR |
| `LAI` | leaf area index |

### 8. PAR Absorbed By Canopy From Top-Lights

Direct canopy absorption:

```math
R_{PAR,LampCanY}
= R_{PAR,GhLamp}(1-r_{CanPAR})(1-e^{-K_{1,PAR}LAI})
```

Floor-reflected component absorbed by canopy:

```math
R_{PAR,LampFlrCan}
= R_{PAR,GhLamp}e^{-K_{1,PAR}LAI}r_{FlrPAR}(1-r_{CanPAR})(1-e^{-K_{2,PAR}LAI})
```

Total PAR absorbed by canopy:

```math
R_{PAR,LampCan}
= R_{PAR,LampCanY} + R_{PAR,LampFlrCan}
```

This is useful if you need to connect lamp intensity to photosynthesis-related variables.

### 9. PAR And NIR Absorbed By Floor

```math
R_{PAR,LampFlr}
= R_{PAR,GhLamp}(1-r_{FlrPAR})e^{-K_{1,PAR}LAI}
```

```math
R_{NIR,LampFlr}
= h_{LampNIR}Q_{LampIn}(1-r_{FlrNIR})e^{-K_{NIR}LAI}
```

### 10. Lamp Radiation Not Absorbed By Canopy Or Floor

```math
R_{LampAir}
= (h_{LampPAR}+h_{LampNIR})Q_{LampIn}
- R_{PAR,LampCan} - R_{NIR,LampCan}
- R_{PAR,LampFlr} - R_{NIR,LampFlr}
```

The paper assumes this remaining shortwave radiation is absorbed by greenhouse structure and immediately transferred to greenhouse air.

### 11. Lamp Efficacy And PPFD

Lamp efficacy:

```math
\text{Efficacy} = h_{LampPAR} z_{LampPAR}
```

Maximum PPFD from the lamp:

```math
PPFD_{max} = h_{LampPAR} z_{LampPAR} q_{LampMax}
```

where:

| Symbol | Meaning |
|---|---|
| `h_LampPAR` | fraction of electrical input converted to PAR |
| `z_LampPAR` | photons per joule of PAR output |
| `q_LampMax` | electrical lamp capacity, W m-2 |

### 12. Convective Heat Transfer

The added convective heat transfers are expressed as:

```math
H_{LampAir} = c_{HEC,LampAir}(T_{Lamp}-T_{Air})
```

```math
H_{IntLampAir} = c_{HEC,IntLampAir}(T_{IntLamp}-T_{Air})
```

```math
H_{GroPipeAir} = c_{HEC,GroPipeAir}(T_{GroPipe}-T_{Air})
```

For the blackout screen:

```math
H_{AirBlScr} = c_{HEC,BlScrAir}(T_{Air}-T_{BlScr})
```

### 13. Active Lamp Cooling

```math
H_{LampCool} = h_{LampCool}Q_{LampIn}
```

This equation is very important for the LED case in this paper because `h_LampCool = 0.63`, meaning 63% of lamp input was removed through active cooling.

### 14. Error Metrics For Model Evaluation

Mean error:

```math
ME = \frac{1}{n}\sum_{i=1}^{n}(y_i^{mes}-y_i^{sim})
```

Root mean squared error:

```math
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i^{mes}-y_i^{sim})^2}
```

Relative root mean squared error:

```math
RRMSE = \frac{100}{\bar{y}^{mes}}\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i^{mes}-y_i^{sim})^2}
```

Relative error for heating:

```math
RE_{heating} = 100\frac{heat^{sim}-heat^{mes}}{heat^{mes}}
```

These are useful if your own model needs to compare predictions against measured greenhouse or gas exchange data.

## How This Can Connect To The Current Dataset

Your current dataset contains gas exchange variables such as:

```text
A, E, Emm, gsw, Ca, Ci, Qin, Tleaf, Tair, RHcham, VPDleaf, PhiPS2
```

GreenLight is not directly a gas exchange data cleaning paper, but it provides the physical greenhouse context behind these variables.

Possible links:

| Current data column | GreenLight-related concept |
|---|---|
| `Qin` | incoming radiation / PAR driver |
| `Tleaf` | canopy or leaf temperature |
| `Tair` | greenhouse air temperature |
| `RHcham` | humidity / vapour pressure environment |
| `VPDleaf` | vapour pressure deficit affecting transpiration |
| `A` | photosynthetic assimilation response |
| `E`, `Emm` | transpiration response |
| `gsw` | stomatal conductance response |
| `Ca`, `Ci` | CO2 environment and leaf internal CO2 |
| `PhiPS2` | photosystem II efficiency / fluorescence response |

A practical modeling direction could be:

```text
Use Qin, Tleaf, Tair, RHcham, VPDleaf, Ca, and possibly time variables
as predictors for A, gsw, E, or PhiPS2.
```

## Possible Thesis/Assignment Takeaways

1. LED lighting may reduce electrical lighting energy per unit PAR, but it can increase greenhouse heating demand.
2. The energy advantage of LED depends on whether removed cooling heat can be recovered.
3. HPS lamps provide substantial radiative heat, especially FIR and NIR, which affects canopy and greenhouse temperature.
4. LED lamps emit much less radiative heat and may require additional heating to maintain climate targets.
5. For greenhouse modeling, lamp energy should not be treated as a single heat input to air. It should be separated into PAR, NIR, FIR, convection, and cooling.
6. For data-driven modeling, climate variables such as light, temperature, humidity, CO2, and VPD should be considered together because they jointly affect photosynthesis and transpiration.

## Limitations Mentioned In The Paper

- The model was evaluated using one experiment.
- Several parameters had to be estimated rather than directly measured.
- CO2 prediction was less accurate, partly because actual CO2 injection rate was not fully measured.
- Relative humidity was systematically overestimated.
- The model did not explicitly include light spectrum effects on stomatal aperture.
- The canopy was treated as one layer, while real canopies have vertical gradients.

## Most Useful Equations To Keep For Later

If only a few equations are needed, keep these:

```math
Q_{LampIn} = U_{Lamp}q_{LampMax}
```

```math
R_{PAR,GhLamp} = h_{LampPAR}Q_{LampIn}
```

```math
PPFD_{max} = h_{LampPAR}z_{LampPAR}q_{LampMax}
```

```math
H_{LampCool} = h_{LampCool}Q_{LampIn}
```

```math
H_{LampAir} = c_{HEC,LampAir}(T_{Lamp}-T_{Air})
```

```math
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i^{mes}-y_i^{sim})^2}
```

```math
RE_{heating} = 100\frac{heat^{sim}-heat^{mes}}{heat^{mes}}
```

These cover lamp input, PAR output, PPFD, cooling, convective heat, and model evaluation.
