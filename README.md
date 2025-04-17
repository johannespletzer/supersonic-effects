# Ozone and Radiation Sensitivity Modeling

A Python package to model ozone column changes and radiative effects in response to various aircraft emissions at different altitudes over specific regions. The model combines empirical emission sensitivities with a Taylor expansion in altitude to estimate effects of supersonic transport on ozone and radiation.

---

## 📦 Project Structure

```text
supersonic-effects/
├── src/
│   └── example.py 
│   └── response_model/
│       ├── __init__.py
│       └── taylor_model.py
│       └── load_data.py
├── tests/
│   └── test_model.py
│   └── test_validation*.py
├── data/
│   ├── sensitivity_*.csv
│   └── taylor_param_*.csv
├── README.md
├── requirements.txt
├── pyproject.toml
...
```

---

## 📈 Features

- Taylor expansion modeling of ozone change w.r.t. altitude
- Emission-specific sensitivity interpolation
- Supports multiple geographic regions

---

## 🚀 Installation

Install the package:

```bash
pip install -e .
```

---

## 🧠 Usage

### Calculate ozone change:

Either execute the example with `python3 src/example.py` or use the following code

```python
from response_model.taylor_model import calculate_delta_F

# Define inputs
# Regions: Transatlantic_Corridor, South_Arabian_Sea or Mean (latter requires prepare=True)
region = "Transatlantic_Corridor" 
altitude_km = 18.0
emissions = {
    'NO': 100, # GgNO2/yr
    'SO': 50,  # GgS/yr
    'H2O': 500, # TgH2O/yr
}

# Calculate ozone change (ΔF)
delta_F = calculate_delta_F(altitude_km, emissions, region, mode='Ozone')
print(f"ΔF = {delta_F:.2f} DU")
```

---

## 📚 Data Source

The data underlying the software originates from [Van 't Hoff et al. 2024](https://doi.org/10.1029/2023JD040476)
- `data/sensitivity_ozone.csv`: Empirical sensitivities (mDU / unit / year)
- `data/sensitivity_radiative_forcing.csv`: Empirical sensitivities (mW/m2 / unit / year)
- `data/taylor_param_ozone.csv`: 1st and 2nd order coefficients for altitude effect (DU / km, DU / km²)
- `data/taylor_param_radiative_forcing.csv`: 1st and 2nd order coefficients for altitude effect (mW/m2 / km, mW/m2 / km²)

---
