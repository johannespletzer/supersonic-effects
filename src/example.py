from ozone_model.taylor_model import calculate_delta_F, calculate_delta_F_altitude, calculate_delta_F_emissions
from ozone_model.read_data import load_data

# Load data
sensitivity_df, taylor_df = load_data()

# Define inputs
altitude_km = 19.0
region = "Transatlantic_Corridor"
emissions = {
    'NOx': 1780.0, # GgNO2/yr
    'SOx': 73.39/44.01*12.01, # GgSO2 from Zhang et al. 2023 to GgS/yr
    'H2O': 151.31 # TgH2O/yr
#    'Fuel': 122320.0 # Gg/yr
}

# Calculate ozone change (ΔF), first and second term
delta_F = calculate_delta_F(altitude_km, emissions, region, sensitivity_df, taylor_df)
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, taylor_df)
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region, sensitivity_df)

print(f"ΔF = {delta_F:.2f} DU,",f"ΔF(alt) = {delta_F_alt:.2f} DU,",f"ΔF(alt) = {delta_F_emis:.2f} DU")
