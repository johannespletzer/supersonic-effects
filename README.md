# Ozone Sensitivity Modeling

A Python package to model ozone column changes (ΔF) in response to various aircraft emissions at different altitudes over specific regions. The model combines empirical emission sensitivities with a Taylor expansion in altitude to estimate total ozone impact.

---

## 📦 Project Structure

```text
supersonic-ozone/
├── src/
│   └── ozone_model/
│       ├── __init__.py
│       └── model.py
├── tests/
│   └── test_model.py
├── data/
│   ├── sensitivity_ozone.csv
│   └── taylor_param.csv
├── README.md
├── requirements.txt
├── pyproject.toml
```

---

## 🚀 Installation

Install the package:

```bash
pip install -e .
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Usage

### Load and calculate ozone change:

```python
import pandas as pd
from ozone_model.model import calculate_delta_F
from ozone_model.read_data import load_data

# Load data
sensitivity_df, taylor_df = load_data()

# Optional: clean column names
sensitivity_df.columns = sensitivity_df.columns.str.strip()
taylor_df.columns = taylor_df.columns.str.strip()

# Define inputs
altitude_km = 18.0
region = "Transatlantic_Corridor"
emissions = {
    'NOx': 100,
    'H2O': 500
}

# Calculate ozone change (ΔF)
delta_F = calculate_delta_F(altitude_km, emissions, region, sensitivity_df, taylor_df)
print(f"ΔF = {delta_F:.2f} DU")
```

---

## 🧪 Running Tests

Requires `pytest`

```bash
pip install pytest
```

Tests can be run simply with after installation

```bash
pytest
```

---

## 📈 Features

- Taylor expansion modeling of ozone change w.r.t. altitude
- Emission-specific sensitivity interpolation
- Supports multiple geographic regions
- Unit-tested with `pytest`

---

## 📚 Data Sources

The data underlying the software originates from [Van 't Hoff et al. 2024](https://doi.org/10.1029/2023JD040476)
- `data/sensitivity_ozone.csv`: Empirical sensitivities (mDU / unit / year)
- `data/taylor_param.csv`: 1st and 2nd order coefficients for altitude effect (DU / km, DU / km²)

---

## 📌 License

Apache2.0

---
