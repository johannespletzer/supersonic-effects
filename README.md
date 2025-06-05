[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15552405.svg)](https://doi.org/10.5281/zenodo.15552405)

# Ozone and Radiation Sensitivity Modeling

A Python package to model ozone column changes and radiative effects in response to various aircraft emissions at different altitudes over specific regions. The model combines empirical emission sensitivities with a Taylor expansion in altitude to estimate effects of supersonic transport on ozone and radiation.

---

## Project Structure

```text
supersonic-effects/
├── src/
│   └── response_model/
│       ├── __init__.py
│       ├── taylor_model.py
│       ├── load_data.py
│       ├── scripts/ 
│ 	    ├── example.py 
│   	    └── test*.py 
├── resources/
│   ├── sensitivity_*.csv
│   └── taylor_param_*.csv
├── tests/
│   ├── test_model.py
│   └── test_validation*.py
├── README.md
├── requirements.txt
├── pyproject.toml
...
```

---

## Features

- Modeling of ozone change and radiative forcing 
- Supports multiple geographic regions
- Emission-specific sensitivity interpolation to altitude of emission
- Optional Taylor expansion w.r.t. cruise altitude to compare to reference aircraft

---

## Use the software

### Installation
Install the package:

```bash
pip install -e .
```

### Run calculation

### Calculate ozone change:

An example on how to use the code is shown here

```python
from response_model.taylor_model import calculate_delta_F_emissions

# Define inputs
mode = 'Radiative_Forcing'  # or 'Ozone'
region = "Transatlantic_Corridor"
altitude_km = 18.0
emissions = {
    'NO': (100, "GgNO2"),  # Gigagrams of NO2 per year
    'SO': (5, "GgS"),      # Gigagrams of sulfur per year
    'H2O': (50, "TgH2O"),  # Teragrams of water vapor per year
}

# Calculate ozone change or radiative forcing
emission_values = {key: val[0] for key, val in emissions.items()}
delta_F = calculate_delta_F_emissions(altitude_km, emission_values, region, mode=mode)

# Format emissions into a readable string with units
emission_str = ', '.join([f"{key} = {value} {unit}" for key, (value, unit) in emissions.items()])
unit_str = "DU" if mode == "Ozone" else "mW/m²"

print(
    f"The {mode} effect of a supersonic aircraft flying across the {region} "
    f"at {altitude_km:.1f} km, emitting {emission_str}, is estimated to be ΔF = {delta_F:.2f} {unit_str}"
)
```

### Example output

The **radiative forcing** effect of a supersonic aircraft flying across the `Transatlantic_Corridor` at **18.0 km**, emitting:

- **NO** = 100 GgNO₂  
- **SO** = 5 GgS  
- **H₂O** = 50 TgH₂O  

is estimated to be:

**ΔF = 9.76 mW/m²**

More extensive examples including reference aircraft for comparison are shown in src/scripts/example.py You can execute this via

```python
python3 src/scripts/example.py
```

---

## Resources

The data underlying the software originates from [Van 't Hoff et al. 2024](https://doi.org/10.1029/2023JD040476)
- `resources/sensitivity_ozone.csv`: Empirical sensitivities (mDU / unit / year)
- `resources/sensitivity_radiative_forcing.csv`: Empirical sensitivities (mW/m2 / unit / year)
- `resources/taylor_param_ozone.csv`: 1st and 2nd order coefficients for altitude effect (DU / km, DU / km²)
- `resources/taylor_param_radiative_forcing.csv`: 1st and 2nd order coefficients for altitude effect (mW/m2 / km, mW/m2 / km²)

---
