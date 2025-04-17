import pytest
from response_model.taylor_model import calculate_delta_F_altitude

def test_calculate_delta_F_altitude_O3():
    region_map = {'TAC':'Transatlantic_Corridor', 'SAS':'South_Arabian_Sea'}

    expected_delta_O3 = {
        'TAC162_NO':  0.1754,
        'TAC204_NO': -0.4470,
        'SAS162_NO':  0.1926,
        'SAS204_NO': -0.8104
    }

    for key, expected_value in expected_delta_O3.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_altitude(altitude, mapped_region, mode='Ozone')
        assert pytest.approx(calculated_value, abs=1e-3) == expected_value

def test_calculate_delta_F_altitude():
    region_map = {'TAC':'Transatlantic_Corridor', 'SAS':'South_Arabian_Sea'}

    expected_delta = {
        'TAC162_NO': -1.2415,
        'TAC204_NO':  0.2440,
        'SAS162_NO': -0.5217,
        'SAS204_NO':  3.657
    }

    for key, expected_value in expected_delta.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_altitude(altitude, mapped_region, mode='Radiative_Forcing')
        assert pytest.approx(calculated_value, abs=1e-3) == expected_value
