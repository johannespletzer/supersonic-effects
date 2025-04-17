import pytest
from response_model.taylor_model import calculate_delta_F_emissions

def test_calculate_delta_F_emissions_o3():
    emissions = {'NO':43.2, 'SO':2.8224, 'H2O':3.36}
    region_map = {'TAC':'Transatlantic_Corridor', 'SAS':'South_Arabian_Sea'}

    expected_delta_O3 = {
        'TAC162_NO':  0.0904, 'TAC162_SO': -0.0620, 'TAC162_H2O': -0.0047,
        'TAC204_NO': -0.1015, 'TAC204_SO': -0.0975, 'TAC204_H2O': -0.0264,
        'SAS162_NO':  0.0854, 'SAS162_SO': -0.0473, 'SAS162_H2O':  7.201152e-05,
        'SAS204_NO': -0.1854, 'SAS204_SO': -0.1118, 'SAS204_H2O': -0.0376
    }

    for key, expected_value in expected_delta_O3.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        species = altitude_species.split('_')[1]
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_emissions(altitude, {species: emissions[species]}, mapped_region, mode='Ozone')
        assert pytest.approx(calculated_value, abs=1e-3) == expected_value

def test_calculate_delta_F_emissions():
    emissions = {'NO':43.2, 'SO':2.8224, 'H2O':3.36}
    region_map = {'TAC':'Transatlantic_Corridor', 'SAS':'South_Arabian_Sea'}

    expected_delta = {
        'TAC162_NO':  1.6552, 'TAC162_SO': -1.6836, 'TAC162_H2O':  0.2732,
        'TAC204_NO':  2.0602, 'TAC204_SO': -2.8830, 'TAC204_H2O':  1.1131,
        'SAS162_NO':  1.7487, 'SAS162_SO': -1.2414, 'SAS162_H2O':  0.0085,
        'SAS204_NO':  2.9161, 'SAS204_SO': -3.5205, 'SAS204_H2O':  1.6684
    }

    for key, expected_value in expected_delta.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        species = altitude_species.split('_')[1]
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_emissions(altitude, {species: emissions[species]}, mapped_region, mode='Radiative_Forcing')
        assert pytest.approx(calculated_value, abs=1e-3) == expected_value
