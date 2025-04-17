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

