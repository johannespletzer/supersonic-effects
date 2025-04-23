from typing import Tuple
import pandas as pd


def prepare_data(filepath: str) -> pd.DataFrame:
    """
    Calculate mean, min, max columns from sensitivity data

    Args:
        filepath (str): Path to ozone or radiation sensitivity data file

    Returns:
        pd.DataFrame: Extended with mean, min and max values as columns
    """

    # Read data
    df = pd.read_csv(filepath, sep=", ", engine="python")

    # Average and range
    df["Mean"] = df[["Transatlantic_Corridor", "South_Arabian_Sea"]].mean(axis=1)
    df["Range"] = (df["South_Arabian_Sea"] - df["Transatlantic_Corridor"]).abs()
    df["Max_val"] = df["Mean"] + df["Range"]
    df["Min_val"] = df["Mean"] - df["Range"]

    return df


<<<<<<< src/response_model/read_data.py
def load_data(prepare=False, mode="Ozone"):
    """
    Loads and optionally prepares data for a given mode.
=======
def load_data(prepare: bool=False, mode: str="Ozone") -> Tuple[pd.DataFrame]:
    """Load sensitivity and taylor data from file as a pandas DataFrame"""
>>>>>>> src/response_model/read_data.py

    Parameters:
        prepare (bool): Whether to preprocess the data. Default is False.
        mode (str): The type of data to load. Default is "Ozone", alternative is "Radiative_Forcing".

    Returns:
        Tuple[pd.DataFrame, ...]: A tuple of two pandas DataFrames.
    """
    
    if mode not in ["Ozone", "Radiative_Forcing"]:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")

    if prepare:
        if mode == "Ozone":
            df = prepare_data("./data/sensitivity_ozone.csv")
            df_t = prepare_data("./data/taylor_param_ozone.csv")
        elif mode == "Radiative_Forcing":
            df = prepare_data("./data/sensitivity_radiative_forcing.csv")
            df_t = prepare_data("./data/taylor_param_radiative_forcing.csv")
    else:
        if mode == "Ozone":
            df = pd.read_csv("./data/sensitivity_ozone.csv", sep=", ", engine="python")
            df_t = pd.read_csv(
                "./data/taylor_param_ozone.csv", sep=", ", engine="python"
            )
        elif mode == "Radiative_Forcing":
            df = pd.read_csv(
                "./data/sensitivity_radiative_forcing.csv", sep=", ", engine="python"
            )
            df_t = pd.read_csv(
                "./data/taylor_param_radiative_forcing.csv", sep=", ", engine="python"
            )

    return df, df_t
