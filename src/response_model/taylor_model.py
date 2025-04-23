import warnings
import numpy as np
from response_model.read_data import load_data


def calculate_delta_F_altitude(
    altitude_km, region, initial_emis_alt=18.3, mode="Ozone"
):
    """
    Compute first term of ΔF(𝐗,Z) for a given region and altitude.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        initial_emis_alt (float): Emission altitude of reference.
        mode (str): "Ozone" or "Radiative_Forcing".

    Returns:
        float: ΔF value in DU or mW/m2.
    """

    _, taylor_df = load_data(prepare=True, mode=mode)

    # Convert pure altitude to relative altitude change from the reference
    altitude_change = altitude_km - initial_emis_alt
    # The Taylor curve is calculated around an altitude of 18.3 km, so a relative altitude needs to be calculated
    relative_altitude_183 = initial_emis_alt - 18.3
    # Relative altitude change w.r.t. 18.3 km
    delta_altitude_183 = altitude_change + relative_altitude_183

    # Altitude-based term using Taylor expansion
    first_order = float(
        taylor_df.loc[
            taylor_df["Parameter"].str.contains(f"1st order Altitude {mode}"), region
        ].iloc[0]
    )
    second_order = float(
        taylor_df.loc[
            taylor_df["Parameter"].str.contains(f"2nd order Altitude {mode}"), region
        ].iloc[0]
    )
    delta_F_altitude = (
        delta_altitude_183 * (first_order)
        + ((delta_altitude_183**2) / 2) * second_order
    )

    # If the reference altitude is not exactly 18.3 km, correct or the bias introduced to the curve
    delta_F_altitude -= (
        relative_altitude_183 * (first_order)
        + ((relative_altitude_183**2) / 2) * second_order
    )

    return delta_F_altitude


def calculate_delta_F_emissions(altitude_km, emissions_dict, region, mode="Ozone"):
    """
    Compute second term of ΔF(𝐗,Z) for a given region, altitude and emissions.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        emissions_dict (dict): Emission magnitudes, e.g., {'NOx': 10, 'H2O': 5}.
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        mode (str): "Ozone" or "Radiative_Forcing".

    Returns:
        float: ΔF value in DU or mW/m2.
    """

    sensitivity_df, _ = load_data(prepare=True, mode=mode)

    # Get valid altitude bounds from the sensitivity data
    valid_altitudes = sensitivity_df["Altitude_km"].unique()
    z_min, z_max = valid_altitudes.min(), valid_altitudes.max()

    if not (z_min <= altitude_km <= z_max):
        warnings.warn(
            f"Altitude {altitude_km} km is outside the supported range: {z_min}–{z_max} km. The estimate will have higher uncertainty!",
            category=UserWarning
        )

    # Emission-based term with interpolation
    delta_F_emissions = 0.0
    for emission_type, x_i in emissions_dict.items():
        # Get all rows matching this emission type
        rows = sensitivity_df[sensitivity_df["Emission"] == emission_type]

        if emission_type not in sensitivity_df["Emission"].unique():
            raise ValueError(f"Emission type '{emission_type}' not found in data.")

        # Sort by altitude to ensure interpolation works
        rows = rows.sort_values("Altitude_km")

        # Get values to interpolate
        altitudes = rows["Altitude_km"].values
        sensitivities = rows[region].values

        # Interpolate
        sensitivity_interp = np.interp(altitude_km, altitudes, sensitivities)
        # In Ozone mode convert the value from mDU to DU.
        delta_F_emissions += (
            x_i * sensitivity_interp / 1000.0
            if mode == "Ozone"
            else x_i * sensitivity_interp
        )

    return delta_F_emissions


def calculate_delta_F(
    altitude_km, emissions_dict, region, initial_emis_alt=18.3, mode="Ozone"
):
    """
    Combine first and second order term of ΔF(𝐗,Z) for a given region, altitude and emissions.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        emissions_dict (dict): Emission magnitudes, e.g., {'NOx': 10, 'H2O': 5}.
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        initial_emis_alt (float): Emission altitude of Taylor expansion reference.

    Returns:
        float: ΔF value in DU or mW/m2.
    """

    # 1. Altitude-based term using Taylor expansion
    delta_F_altitude = calculate_delta_F_altitude(
        altitude_km, region, initial_emis_alt, mode
    )

    # 2. Emission-based term with interpolation
    delta_F_emissions = calculate_delta_F_emissions(
        altitude_km, emissions_dict, region, mode
    )

    # 3. Total
    delta_F_total = delta_F_altitude + delta_F_emissions

    return delta_F_total
