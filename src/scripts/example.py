from response_model.taylor_model import (
    calculate_delta_F,
    calculate_delta_F_altitude,
    calculate_delta_F_emissions,
)


# Calculate ozone changes

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

# Calculate ozone change (ΔF), first and second term
delta_F = calculate_delta_F(altitude_km, emissions, region, reference_km)
delta_F_alt = calculate_delta_F_altitude(altitude_km, region, reference_km)
delta_F_emis = calculate_delta_F_emissions(altitude_km, emissions, region)


print('\nRegion: "Transatlantic_Corridor", mode: "Ozone"')
print(f'Cruise altitude: {altitude_km} km, cruise of reference aircraft: {reference_km} km')
print("Should result in around 0.3 DU (0.2 DU for altitude term, 0.1 DU for emission term) with default settings\n")
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

print('\n\nRegion: "Transatlantic_Corridor", mode: "Radiative_Forcing"')
print(f'Cruise altitude: {altitude_km} km, cruise of reference aircraft: {reference_km} km')
print("Should result in around 0.4 mW/m2 (-1.2 mW/m2 altitude term, 1.7 mW/m2 for emission term) with default settings\n")
print(
    f"ΔF = {delta_F:.3f} mW/m2,",
    f"ΔF(alt) = {delta_F_alt:.3f} mW/m2,",
    f"ΔF(emis) = {delta_F_emis:.3f} mW/m2",
)


# Calculate radiative forcing

reference_km = 16.2
altitude_km = 20.4
region = "South_Arabian_Sea"

print('\n\nRegion: "South_Arabian_Sea", mode: "Ozone"')
print(f'Cruise altitude: {altitude_km} km, cruise of reference aircraft: {reference_km} km')
print("Should result in around -1.2 (-1.0 DU for altitude term, -0.2 DU for emission term) with default settings\n")

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

print('\n\nRegion: "South_Arabian_Sea", mode: "Radiative_Forcing"')
print(f'Cruise altitude: {altitude_km} km, cruise of reference aircraft: {reference_km} km')
print("Should result in around 7.1 mW/m2 (4.2 mW/m2 altitude term, 2.9 mW/m2 for emission term) with default settings\n")
print(
    f"ΔF = {delta_F:.3f} mW/m2,",
    f"ΔF(alt) = {delta_F_alt:.3f} mW/m2,",
    f"ΔF(emis) = {delta_F_emis:.3f} mW/m2\n",
)
