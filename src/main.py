import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def prepare_data():
    '''Load sensitivity data from file and calculate required columns as a pandas DataFrame'''
    
    # Read data
    df = pd.read_csv('../data/sensitivity_ozone.csv')
    
    # Average and range
    df['Mean']    = df[['Transatlantic_Corridor','South_Arabian_Sea']].mean(axis=1)
    df['Range']   = (df['South_Arabian_Sea'] - df['Transatlantic_Corridor']).abs()
    df['Max_val'] = df['Mean'] + df['Range']
    df['Min_val'] = df['Mean'] - df['Range']

    return df

def interpolate_sensitivity(emission_type, altitude_km, corridor='Transatlantic_Corridor'):
    data = df[df['Emission'] == emission_type]
    valid_data = data[data['Altitude_km'] != '-']
    altitudes = valid_data['Altitude_km'].astype(float)
    sensitivities = valid_data[corridor].astype(float)
    interpolator = interp1d(altitudes, sensitivities, fill_value='extrapolate')
    return interpolator(altitude_km)

def calculate_ozone_change(altitude_km, emission_magnitude, case='combined', corridor='Transatlantic_Corridor'):
    altitude_km = np.array(altitude_km, dtype=float)
    emission_magnitude = np.array(emission_magnitude, dtype=float)

    if altitude_km.shape != emission_magnitude.shape:
        raise ValueError('altitude_km and emission_magnitude arrays must have the same shape.')

    ozone_change = np.zeros_like(altitude_km)

    if case.lower() == 'combined':
        sensitivity = interpolate_sensitivity('Generalized Fuel', altitude_km, corridor)
        ozone_change = sensitivity * emission_magnitude
    elif case.lower() == 'individual':
        for emission in ['NOx', 'SOx', 'H2O']:
            sensitivity = interpolate_sensitivity(emission, altitude_km, corridor)
            ozone_change += sensitivity * emission_magnitude
    else:
        raise ValueError("Invalid case specified. Choose 'combined' or 'individual'.")

    return ozone_change

df = prepare_data()

# Example usage:
altitudes = [17, 18, 19]
emissions = [100, 150, 120]  # Emission magnitudes in corresponding units

# Combined effect example
combined_ozone_change = calculate_ozone_change(altitudes, emissions, case='combined')
print('Combined ozone change (mDU):', combined_ozone_change)

# Individual effect example
individual_ozone_change = calculate_ozone_change(altitudes, emissions, case='individual')
print('Individual ozone change (mDU):', individual_ozone_change)
