import pytest
import pandas as pd
from response_model.taylor_model import calculate_delta_F_emissions

@pytest.fixture
def sensitivity_df():
    return pd.read_csv('./data/sensitivity_ozone.csv', sep=', ', engine='python')

def test_calculate_delta_F_emissions(sensitivity_df):
    emissions = {'NO':43.2, 'SO':2.8224, 'H2O':3.36}
    region_map = {'TAC':'Transatlantic_Corridor', 'SAS':'South_Arabian_Sea'}

    expected_delta_O3 = {
        'TAC162_NO': 0.4009-0.3105, 'TAC162_SO': 0.2788-0.3105, 'TAC162_H2O': 0.3062-0.3105,
        'TAC204_NO': -0.4136+0.3121, 'TAC204_SO': -0.3619+0.3121, 'TAC204_H2O': -0.3359+0.3121,
        'SAS162_NO': 0.3724-0.2870, 'SAS162_SO': 0.2628-0.2870, 'SAS162_H2O': 0.2871-0.2870,
        'SAS204_NO': -0.9014+0.7160, 'SAS204_SO': -0.7731+0.7160, 'SAS204_H2O': -0.7499+0.7160
    }
    expected_delta_O3 = {
        'TAC162_NO':  0.0904, 'TAC162_SO': -0.0317*1.956, 'TAC162_H2O': -0.0043,
        'TAC204_NO': -0.1015, 'TAC204_SO': -0.0498*1.956, 'TAC204_H2O': -0.0238,
        'SAS162_NO':  0.0854, 'SAS162_SO': -0.0242*1.956, 'SAS162_H2O':  0.0001,
        'SAS204_NO': -0.1854, 'SAS204_SO': -0.0571*1.956, 'SAS204_H2O': -0.0339
    }

    for key, expected_value in expected_delta_O3.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        species = altitude_species.split('_')[1]
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_emissions(altitude, {species: emissions[species]}, mapped_region, sensitivity_df)
        assert pytest.approx(calculated_value, abs=1e-3) == expected_value
