import pytest
import pandas as pd
from ozone_model.taylor_model import calculate_delta_F

@pytest.fixture
def sensitivity_df():
    return pd.read_csv("data/sensitivity_ozone.csv", sep=', ', engine='python')

@pytest.fixture
def taylor_df():
    return pd.read_csv("data/taylor_param.csv", sep=', ', engine='python')

def test_valid_calculation(sensitivity_df, taylor_df):
    emissions = {'NOx': 100, 'H2O': 200}
    altitude = 18.0
    region = "Transatlantic_Corridor"

    delta_F = calculate_delta_F(altitude, emissions, region, sensitivity_df, taylor_df)
    
    # Just check it's a number and within plausible range
    assert isinstance(delta_F, float)
    assert -500 < delta_F < 500  # Based on rough sensitivity values

def test_altitude_below_bounds(sensitivity_df, taylor_df):
    emissions = {'NOx': 100}
    region = "South_Arabian_Sea"
    
    with pytest.raises(ValueError, match="Altitude.*outside the supported range"):
        calculate_delta_F(15.0, emissions, region, sensitivity_df, taylor_df)

def test_edge_altitude_exact_match(sensitivity_df, taylor_df):
    emissions = {'SOx': 50}
    altitude = 20.4  # Exact match in data
    region = "South_Arabian_Sea"

    result = calculate_delta_F(altitude, emissions, region, sensitivity_df, taylor_df)
    assert isinstance(result, float)
