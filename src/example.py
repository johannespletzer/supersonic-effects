from ozone_model.model import calculate_delta_F
from ozone_model.read_data import load_data

df, df_t = load_data(prepare=False)

emissions = {'NOx': 10, 'H2O': 20}
region = "Transatlantic_Corridor"
altitude = 18.0 

delta_F = calculate_delta_F(altitude, emissions, region, df, df_t)

print(f"ΔF = {delta_F:.2f} DU")
