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
