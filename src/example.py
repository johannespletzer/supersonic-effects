from response_model.taylor_model import calculate_delta_F, calculate_delta_F_altitude, calculate_delta_F_emissions
from response_model.read_data import load_data

# Load data
sensitivity_df_o3, sensitivity_df_rf, taylor_df = load_data(prepare=True)

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
delta_F = calculate_delta_F(altitude_km, emissions, region, sensitivity_df_o3, taylor_df, reference_km)
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, taylor_df, reference_km)
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region, sensitivity_df_o3)
print(f"ΔF = {delta_F:.3f} DU,",f"ΔF(alt) = {delta_F_alt:.3f} DU,",f"ΔF(emis) = {delta_F_emis:.3f} DU")
#print(f"ΔF(emis) = {delta_F_emis:.3f} DU")

# Calculate RF change (ΔF), first and second term
delta_F = calculate_delta_F(altitude_km, emissions, region, sensitivity_df_rf, taylor_df, reference_km,mode="Radiative_Forcing")
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, taylor_df, reference_km,mode="Radiative_Forcing")
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region, sensitivity_df_rf,mode="Radiative_Forcing")
print(f"ΔF = {delta_F:.3f} mW/m2,",f"ΔF(alt) = {delta_F_alt:.3f} mW/m2,",f"ΔF(emis) = {delta_F_emis:.3f} mW/m2")
#print(f"ΔF(emis) = {delta_F_emis:.3f} DU")



# Two test cases with the singlemodel to check my implementation:
altitude_change = altitude_km - reference_km
print(f"Example calculation: {altitude_change:.3f} km altitude change from a reference altitude of {reference_km:.3f} km, NOx increase, Transatlantic")
delta_output_singlemodel = calculate_delta_F_single(reference_km,altitude_change,emissions,region)
print(f"Single model: ΔF = {delta_output_singlemodel['Total']:.3f} DU,",f"ΔF(alt) = {delta_output_singlemodel['Altitude_term']:.3f} DU,",f"ΔF(emis) = {delta_output_singlemodel['Emissions_term']:.3f} DU")
delta_output_singlemodel = calculate_delta_F_single(reference_km,altitude_change,emissions,region,mode="Radiative_Forcing")
print(f"Single model: ΔF = {delta_output_singlemodel['Total']:.3f} mW/m2,",f"ΔF(alt) = {delta_output_singlemodel['Altitude_term']:.3f} mW/m2,",f"ΔF(emis) = {delta_output_singlemodel['Emissions_term']:.3f} mW/m2")
print("Should output around 0.26 DU (0.170 alt, 0.090 emis) and 0.41 mW/m2 (-1.24 alt ,1.65 emis) for Transatlantic_Corridor")

reference_km = 16.2
altitude_km = 20.4
region = "South_Arabian_Sea"
altitude_change = altitude_km - reference_km
print(f"Example calculation: {altitude_change:.3f} km altitude change from a reference altitude of {reference_km:.3f} km, NOx increase, South Arabian Sea")
delta_output_singlemodel = calculate_delta_F_single(reference_km,altitude_change,emissions,region)
print(f"Single model: ΔF = {delta_output_singlemodel['Total']:.3f} DU,",f"ΔF(alt) = {delta_output_singlemodel['Altitude_term']:.3f} DU,",f"ΔF(emis) = {delta_output_singlemodel['Emissions_term']:.3f} DU")
delta_output_singlemodel = calculate_delta_F_single(reference_km,altitude_change,emissions,region,mode="Radiative_Forcing")
print(f"Single model: ΔF = {delta_output_singlemodel['Total']:.3f} mW/m2,",f"ΔF(alt) = {delta_output_singlemodel['Altitude_term']:.3f} mW/m2,",f"ΔF(emis) = {delta_output_singlemodel['Emissions_term']:.3f} mW/m2")
print("Should output around -1.18 DU (-0.99 alt, -0.19 emis) and 7.09 mW/m2 (4.17 alt ,2.92 emis) for Transatlantic_Corridor")

