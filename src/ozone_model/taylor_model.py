import numpy as np

def calculate_delta_F_altitude(altitude_km, region, taylor_df, ref_km=18.3, mode="Ozone"):
    """
    Compute first term of ΔF(𝐗,Z) for a given region and altitude.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        taylor_df (pd.DataFrame): Loaded from taylor_param.csv.
        ref_km (float): Emission altitude of Taylor expansion reference.
        mode (str): "Ozone" or "Radiative_Forcing".

    Returns:
        float: ΔF value in DU.
    """

    if mode not in ["Ozone","Radiative_Forcing"]:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")

    # Convert pure altitude to relative altitude change from the reference
    altitude_change = altitude_km - ref_km
    # The taylor curve is calculated around an altitude of 18.3 km, so a relative altitude needs to be calculated
    relative_altitude_183 = ref_km - 18.3
    # Relative altitude change w.r.t. 18.3 km
    delta_altitude_183 = altitude_change + relative_altitude_183

    # Altitude-based term using Taylor expansion
    first_order = float(taylor_df.loc[taylor_df['Parameter'].str.contains(f"1st order Altitude {mode}"), region].iloc[0])
    second_order = float(taylor_df.loc[taylor_df['Parameter'].str.contains(f"2nd order Altitude {mode}"), region].iloc[0])
    delta_F_altitude = delta_altitude_183 * (first_order) + ((delta_altitude_183**2) / 2) * second_order

    # If the reference altitude is not exactly 18.3 km, correct or the bias introduced to the curve
    delta_F_altitude -= relative_altitude_183 * (first_order) + ((relative_altitude_183**2) / 2) * second_order

    return delta_F_altitude

def calculate_delta_F_emissions(altitude_km, emissions_dict, region, sensitivity_df, mode="Ozone"):
    """
    Compute second term of ΔF(𝐗,Z) for a given region, altitude and emissions.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        emissions_dict (dict): Emission magnitudes, e.g., {'NOx': 10, 'H2O': 5}.
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        sensitivity_df (pd.DataFrame): Loaded from sensitivity_ozone.csv.
        mode (str): "Ozone" or "Radiative_Forcing".

    Returns:
        float: ΔF value in DU.
    """

    if mode not in ["Ozone","Radiative_Forcing"]:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")

    # Emission-based term with interpolation
    delta_F_emissions = 0.0
    for emission_type, x_i in emissions_dict.items():
        # Get all rows matching this emission type
        rows = sensitivity_df[sensitivity_df['Emission'] == emission_type]

        if emission_type not in sensitivity_df['Emission'].unique():
            raise ValueError(f"Emission type '{emission_type}' not found in data.")

        # Sort by altitude to ensure interpolation works
        rows = rows.sort_values("Altitude_km")

        # Get values to interpolate
        altitudes = rows["Altitude_km"].values
        sensitivities = rows[region].values

        # Interpolate
        sensitivity_interp = np.interp(altitude_km, altitudes, sensitivities)
        # In Ozone mode convert the value from mDU to DU.
        delta_F_emissions += x_i * sensitivity_interp / 1000.0 if mode == "Ozone" else x_i * sensitivity_interp

    return delta_F_emissions

def calculate_delta_F(altitude_km, emissions_dict, region, sensitivity_df, taylor_df, ref_km=18.3, mode="Ozone"):
    """
    Combine first and second order term of ΔF(𝐗,Z) for a given region, altitude and emissions.

    Parameters:
        altitude_km (float): Emission altitude (e.g., 18.0).
        emissions_dict (dict): Emission magnitudes, e.g., {'NOx': 10, 'H2O': 5}.
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        sensitivity_df (pd.DataFrame): Loaded from sensitivity_ozone.csv.
        taylor_df (pd.DataFrame): Loaded from taylor_param.csv.
        ref_km (float): Emission altitude of Taylor expansion reference.

    Returns:
        float: ΔF value in DU.
    """
    from ozone_model.taylor_model import calculate_delta_F_altitude, calculate_delta_F_emissions

    if mode not in ["Ozone","Radiative_Forcing"]:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")

    # Get valid altitude bounds from the sensitivity data
    valid_altitudes = sensitivity_df["Altitude_km"].unique()
    z_min, z_max = valid_altitudes.min(), valid_altitudes.max()

    if not (z_min <= altitude_km <= z_max):
        raise Warning(f"Altitude {altitude_km} km is outside the supported range: {z_min}–{z_max} km, the estimate will have higher uncertainty!")

    # 1. Altitude-based term using Taylor expansion
    delta_F_altitude = calculate_delta_F_altitude(altitude_km, region, taylor_df, ref_km,mode)

    from ozone_model.read_data import load_data
    sensitivity_df_o3, sensitivity_df_rf, taylor_df = load_data(prepare=True)

    # 2. Emission-based term with interpolation
    if mode == "Ozone":
        delta_F_emissions = calculate_delta_F_emissions(altitude_km, emissions_dict, region, sensitivity_df_o3, mode)
    elif mode == "Radiative_Forcing":
        delta_F_emissions = calculate_delta_F_emissions(altitude_km, emissions_dict, region, sensitivity_df_rf, mode)
    else:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")

    # 3. Total
    delta_F_total = delta_F_altitude + delta_F_emissions

    return delta_F_total

def calculate_delta_F_single(reference_altitude_km, change_altitude_km, change_in_emissions, region, mode="Ozone"):
    """
    Combine first and second order term of ΔF(𝐗,Z) for a given region, altitude and emissions.

    Parameters:
        reference_altitude_km (float): Emission altitude of the initial scenario (e.g., 18.0).
        change_altitude_km (float): Change in altitude relative to the initial scenario (e.g., -2.0).
        change_in_emissions (dict): Changes in annual emissions, in Gigagrams. e.g., {'NOx': 10, 'H2O': 5}.
        region (str): 'Transatlantic_Corridor' or 'South_Arabian_Sea'.
        mode (str): "Ozone" or "Radiative Forcing".

    Returns:
        dict: dictionary with components of the ΔF value in DU (Ozone mode) or mW/m2 (Radiative_Forcing mode).
    """
    # Load the underlying data from the csv files
    from ozone_model.read_data import load_data
    sensitivity_df_o3, sensitivity_df_rf, taylor_df = load_data(prepare=True)

    # Check whether the input arguments are as expected
    if mode not in ["Ozone","Radiative_Forcing"]:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")
    if region not in ["Transatlantic_Corridor", "South_Arabian_Sea"]:
        raise ValueError("region keyword should be either Transatlantic_Corridor or South_Arabian_Sea")

    # Get valid altitude bounds from the sensitivity data
    valid_altitudes = sensitivity_df_o3["Altitude_km"].unique()
    z_min, z_max = valid_altitudes.min(), valid_altitudes.max()
    # Check whether the new altitude is within these bounds, if not raise a warning.
    if not (z_min <= reference_altitude_km + change_altitude_km <= z_max):
        raise Warning(f"Altitude {reference_altitude_km + change_altitude_km} km is outside the supported range: {z_min}–{z_max} km, the estimate will have higher uncertainty!")

    # Calculate relative altitudes
    relative_altitude_183 = reference_altitude_km - 18.3 # The taylor curve is calculated around an altitude of 18.3 km
    relative_altitude_162 = reference_altitude_km - 16.2 # The sensitivities are interpolated from an altitude of 16.2 km
    delta_altitude_183 = change_altitude_km + relative_altitude_183 # New altitude relative to 18.3 km
    delta_altitude_162 = change_altitude_km + relative_altitude_162 # New altitude relative to 16.2 km

    ### 1. Altitude-based term using Taylor expansion
    first_order = float(taylor_df.loc[taylor_df['Parameter'].str.contains(f"1st order Altitude {mode}"), region].iloc[0])
    second_order = float(taylor_df.loc[taylor_df['Parameter'].str.contains(f"2nd order Altitude {mode}"), region].iloc[0])
    delta_F_altitude = delta_altitude_183 * (first_order) + (delta_altitude_183**2)/2 * second_order

    # If the initial reference altitude is not exactly 18.3 km, compensate by subtracting the bias
    delta_F_altitude -= (relative_altitude_183 * (first_order) + (relative_altitude_183**2)/2 * second_order)

    ### 2. Emission-based term with interpolation
    # Select the right sensitivity dataframe
    df_sensitivities = sensitivity_df_o3 if mode == "Ozone" else sensitivity_df_rf

    # Interpolate sensitivities to the requested (new) emission altitude
    sensitivities = {
        'NO': df_sensitivities.loc[1][region] + (
                df_sensitivities.loc[0][region] - df_sensitivities.loc[1][region]) / 4.2 * delta_altitude_162,
        'SO': df_sensitivities.loc[3][region] + (df_sensitivities.loc[2][region] - df_sensitivities.loc[3][
                         region]) / 4.2 * delta_altitude_162,
        'H2O': df_sensitivities.loc[5][region] + (
                    df_sensitivities.loc[4][region] - df_sensitivities.loc[5][region]) / 4.2 * delta_altitude_162}

    # Loop over the emissions in the change_in_emissions dictionary, and calculate their respective effect on the F metric
    delta_F_emissions = {}
    delta_F_emissions_total = 0
    for emission_type, x_i in change_in_emissions.items():
        if emission_type not in df_sensitivities['Emission'].unique():
            raise ValueError(f"Emission type '{emission_type}' not found in data.")

        # Calculate effect of changes in emissions
        delta_F_emissions[emission_type] = x_i * sensitivities[emission_type]
        delta_F_emissions_total += x_i * sensitivities[emission_type]

    # optionally scale all ozone metrics to DU
    if mode == "Ozone":
        delta_F_emissions_total /= 1000
        for k in delta_F_emissions.keys():
            delta_F_emissions[k] /= 1000


    # 3. Total
    delta_F_total = delta_F_altitude + delta_F_emissions_total

    # Prepare output dictionary (To allow outputting separate terms as well)
    output_dict = {"Total": delta_F_total, "Altitude_term": delta_F_altitude, "Emissions_term": delta_F_emissions_total,
                   "Speciated_emissions": delta_F_emissions}

    return output_dict
