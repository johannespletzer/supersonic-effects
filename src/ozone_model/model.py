import pandas as pd
import numpy as np

def calculate_delta_F(altitude_km, emissions_dict, region, sensitivity_df, taylor_df):
    """
    Compute ΔF(𝐗,Z) for a given region, altitude (with interpolation), and emissions.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        emissions_dict (dict): Emission magnitudes, e.g., {'NOx': 10, 'H2O': 5}.
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        sensitivity_df (pd.DataFrame): Loaded from sensitivity_ozone.csv.
        taylor_df (pd.DataFrame): Loaded from taylor_param.csv.

    Returns:
        float: ΔF value in DU.
    """

    # Get valid altitude bounds from the sensitivity data
    valid_altitudes = sensitivity_df["Altitude_km"].unique()
    z_min, z_max = valid_altitudes.min(), valid_altitudes.max()

    if not (z_min <= altitude_km <= z_max):
        raise ValueError(f"Altitude {altitude_km} km is outside the supported range: {z_min}–{z_max} km")

    # 1. Altitude-based term using Taylor expansion
    first_order = float(taylor_df.loc[taylor_df['Parameter'].str.contains("1st"), region])
    second_order = float(taylor_df.loc[taylor_df['Parameter'].str.contains("2nd"), region])
    delta_F_altitude = altitude_km * (first_order + (altitude_km / 2) * second_order)

    # 2. Emission-based term with interpolation
    delta_F_emissions = 0.0
    for emission_type, x_i in emissions_dict.items():
        # Get all rows matching this emission type
        rows = sensitivity_df[sensitivity_df['Emission'] == emission_type]

        if len(rows) < 2:
            raise ValueError(f"Not enough data to interpolate for emission type: {emission_type}")

        if emission_type not in sensitivity_df['Emission'].unique():
            raise ValueError(f"Emission type '{emission_type}' not found in data.")

        # Sort by altitude to ensure interpolation works
        rows = rows.sort_values("Altitude_km")

        # Get values to interpolate
        altitudes = rows["Altitude_km"].values
        sensitivities = rows[region].values

        # Interpolate
        sensitivity_interp = np.interp(altitude_km, altitudes, sensitivities)
        delta_F_emissions += x_i * sensitivity_interp / 1000.0  # Convert mDU to DU

    # 3. Total
    delta_F_total = delta_F_altitude + delta_F_emissions

    return delta_F_total
