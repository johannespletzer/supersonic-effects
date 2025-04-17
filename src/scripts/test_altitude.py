import pytest
from response_model.taylor_model import calculate_delta_F_altitude


@pytest.mark.parametrize("mode", ["Ozone", "Radiative_Forcing"])
def test_calculate_delta_F_altitude(mode):
    region_map = {"TAC": "Transatlantic_Corridor", "SAS": "South_Arabian_Sea"}

    expected_delta = {"TAC162": 0.0, "TAC204": 0.0, "SAS162": 0.0, "SAS204": 0.0}

    for key, _ in expected_delta.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_altitude(
            altitude, mapped_region, mode=mode
        )
        print(key, altitude, mapped_region, calculated_value)


test_calculate_delta_F_altitude(mode="Ozone")
test_calculate_delta_F_altitude(mode="Radiative_Forcing")
