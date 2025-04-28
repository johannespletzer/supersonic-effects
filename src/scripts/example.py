from response_model.taylor_model import (
    calculate_delta_F,
    calculate_delta_F_altitude,
    calculate_delta_F_emissions,
)

altitude_km = 16.2
reference_km = 18.3
region = (
    "Transatlantic_Corridor"  # Options: Transatlantic corridor, South_Arabian_Sea, Mean
)
emissions = {
    "NO": 43.2,  # GgNO2/yr
    #    'SO': 2.8224, # GgS
    #    'H2O': 3.36 # TgH2O/yr
}

print(
    "Should result in around 0.26 DU (0.170 alt, 0.090 emis) and 0.41 mW/m2 (-1.24 alt, 1.65 emis) for Transatlantic_Corridor"
)

# Calculate ozone change (ΔF), first and second term
delta_F = calculate_delta_F(altitude_km, emissions, region, reference_km)
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, reference_km)
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region)

print(
    f"ΔF = {delta_F:.3f} DU,",
    f"ΔF(alt) = {delta_F_alt:.3f} DU,",
    f"ΔF(emis) = {delta_F_emis:.3f} DU",
)

# Calculate RF change (ΔF), first and second term
delta_F = calculate_delta_F(
    altitude_km, emissions, region, reference_km, mode="Radiative_Forcing"
)
delta_F_alt = calculate_delta_F_altitude(
    altitude_km, region, reference_km, mode="Radiative_Forcing"
)
delta_F_emis = calculate_delta_F_emissions(
    altitude_km, emissions, region, mode="Radiative_Forcing"
)

print(
    f"ΔF = {delta_F:.3f} mW/m2,",
    f"ΔF(alt) = {delta_F_alt:.3f} mW/m2,",
    f"ΔF(emis) = {delta_F_emis:.3f} mW/m2",
)

reference_km = 16.2
altitude_km = 20.4
region = "South_Arabian_Sea"

print(
    "\nShould result in around -1.18 DU (-0.99 alt, -0.19 emis) and 7.09 mW/m2 (4.17 alt, 2.92 emis) for South_Arabian_Sea"
)

# Calculate ozone change (ΔF), first and second term
delta_F = calculate_delta_F(altitude_km, emissions, region, reference_km)
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, reference_km)
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region)

print(
    f"ΔF = {delta_F:.3f} DU,",
    f"ΔF(alt) = {delta_F_alt:.3f} DU,",
    f"ΔF(emis) = {delta_F_emis:.3f} DU",
)
