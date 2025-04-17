from response_model.taylor_model import calculate_delta_F


def test_valid_calculation():
    emissions = {"NO": 100, "H2O": 200}
    altitude = 18.0
    region = "Transatlantic_Corridor"

    delta_F = calculate_delta_F(altitude, emissions, region, mode="Ozone")

    # Just check it's a number and within plausible range
    assert isinstance(delta_F, float)
    assert -50 < delta_F < 50  # Based on rough sensitivity values


def test_edge_altitude_exact_match():
    emissions = {"SO": 50}
    altitude = 20.4  # Exact match in data
    region = "South_Arabian_Sea"

    result = calculate_delta_F(altitude, emissions, region, mode="Ozone")
    assert isinstance(result, float)
