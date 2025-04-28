import pytest
from response_model.taylor_model import calculate_delta_F_emissions


@pytest.mark.parametrize("mode", ["Ozone", "Radiative_Forcing"])
def test_calculate_delta_F_emissions(mode):
    emissions = {"NO": 43.2, "SO": 2.8224, "H2O": 3.36}
    region_map = {"TAC": "Transatlantic_Corridor", "SAS": "South_Arabian_Sea"}

    expected_delta_O3 = {
        "TAC162_NO": 0.0904,
        "TAC162_SO": -0.0620,
        "TAC162_H2O": -0.0047,
        "TAC204_NO": -0.1015,
        "TAC204_SO": -0.0975,
        "TAC204_H2O": -0.0264,
        "SAS162_NO": 0.0854,
        "SAS162_SO": -0.0473,
        "SAS162_H2O": 7.201152e-05,
        "SAS204_NO": -0.1854,
        "SAS204_SO": -0.1118,
        "SAS204_H2O": -0.0376,
    }

    for key, _ in expected_delta_O3.items():
        region, altitude_species = key[:3], key[3:]
        altitude = float(altitude_species[:3]) / 10
        species = altitude_species.split("_")[1]
        mapped_region = region_map[region]

        calculated_value = calculate_delta_F_emissions(
            altitude, {species: emissions[species]}, mapped_region, mode=mode
        )
        print(key, altitude, species, mapped_region, calculated_value)


test_calculate_delta_F_emissions(mode="Ozone")
test_calculate_delta_F_emissions(mode="Radiative_Forcing")
