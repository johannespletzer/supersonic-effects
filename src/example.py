from ozone_model.taylor_model import calculate_delta_F, calculate_delta_F_altitude, calculate_delta_F_emissions
from ozone_model.read_data import load_data

# Load data
sensitivity_df, taylor_df = load_data(prepare=True)

# Define inputs
#altitude_km = 19.
altitude_km = 16.2
#altitude_km = 20.4
reference_km = 18.3 
region = "Transatlantic_Corridor" # Options: Transatlantic corridor, South_Arabian_Sea, Mean
#region = "South_Arabian_Sea" # Options: Transatlantic corridor, South_Arabian_Sea, Mean
emissions = {
# Values from Zhang et al. 2023 for 17-21 km altitude: ΔF(emis) ~ - 2 DU
#    'NO': 1780.0, # GgNO2/yr
#    'SO': 73.39/44.01*12.01, # GgSO2 from Zhang et al. 2023 to GgS/yr
#    'H2O': 151.31 # TgH2O/yr
# Values from Jurrian for 16.2 and 20.4 km altitude
#    'NO': 144., # GgNO2/yr
#    'NO': 187.2, # GgNO2/yr
    'NO': 43.2, # GgNO2/yr
#    'NO': 0., # GgNO2/yr
#    'SO': 9.408, # GgS
#    'SO': 12.2304, # GgS
#    'SO': 2.8224, # GgS
#    'SO': 0., # GgS
#    'H2O': 10.08 # TgH2O/yr
#    'H2O': 13.44 # TgH2O/yr
#    'H2O': 3.36 # TgH2O/yr
#    'H2O': 0. # TgH2O/yr
}

# Calculate ozone change (ΔF), first and second term
delta_F = calculate_delta_F(altitude_km, emissions, region, sensitivity_df, taylor_df, reference_km)
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, taylor_df, reference_km)
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region, sensitivity_df)

print(f"ΔF = {delta_F:.3f} DU,",f"ΔF(alt) = {delta_F_alt:.3f} DU,",f"ΔF(emis) = {delta_F_emis:.3f} DU")
#print(f"ΔF(emis) = {delta_F_emis:.3f} DU")
