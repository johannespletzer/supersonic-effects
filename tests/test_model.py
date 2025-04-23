import pytest
from response_model.taylor_model import (
    calculate_delta_F,
    calculate_delta_F_altitude,
    calculate_delta_F_emissions,
)

# Mock input for tests
emissions_dict = {"NO": 10, "H2O": 5, "SO": 1}
region = "Transatlantic_Corridor"
altitude_km = 18.0


def test_altitude_term_runs_without_error():
    val = calculate_delta_F_altitude(
        altitude_km=altitude_km,
        region=region,
        initial_emis_alt=18.3,
        mode="Ozone"
    )
    assert isinstance(val, float)


def test_emission_term_runs_without_error():
    val = calculate_delta_F_emissions(
        altitude_km=altitude_km,
        emissions_dict=emissions_dict,
        region=region,
        mode="Ozone"
    )
    assert isinstance(val, float)


def test_full_deltaF_combines_terms():
    val = calculate_delta_F(
        altitude_km=altitude_km,
        emissions_dict=emissions_dict,
        region=region,
        initial_emis_alt=18.3,
        mode="Ozone"
    )
    assert isinstance(val, float)


def test_invalid_region_raises():
    with pytest.raises(KeyError):
        calculate_delta_F(
            altitude_km=altitude_km,
            emissions_dict=emissions_dict,
            region="InvalidRegion",
            mode="Ozone"
        )


def test_invalid_emission_type_raises():
    with pytest.raises(ValueError):
        calculate_delta_F_emissions(
            altitude_km=altitude_km,
            emissions_dict={"UNKNOWN": 1.0},
            region=region,
            mode="Ozone"
        )


def test_warning_for_out_of_range_altitude():
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = calculate_delta_F_emissions(
            altitude_km=50.0,  # clearly outside normal range
            emissions_dict=emissions_dict,
            region=region,
            mode="Ozone"
        )
        assert any("outside the supported range" in str(warn.message) for warn in w)
