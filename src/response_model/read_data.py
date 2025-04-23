import pandas as pd
import importlib.resources as pkg_resources
from response_model import data


def prepare_data(filepath):
    """Calculate mean, min, max columns"""

    # Read data
    df = pd.read_csv(filepath, sep=", ", engine="python")

    # Average and range
    df["Mean"] = df[["Transatlantic_Corridor", "South_Arabian_Sea"]].mean(axis=1)
    df["Range"] = (df["South_Arabian_Sea"] - df["Transatlantic_Corridor"]).abs()
    df["Max_val"] = df["Mean"] + df["Range"]
    df["Min_val"] = df["Mean"] - df["Range"]

    return df


def load_data(prepare=False, mode="Ozone"):
    """Load sensitivity and taylor data from file as a pandas DataFrame"""

    if mode not in ["Ozone", "Radiative_Forcing"]:
        raise ValueError("mode must be 'Ozone' or 'Radiative_Forcing'")

    if mode == "Ozone":
        sens_file = "sensitivity_ozone.csv"
        taylor_file = "taylor_param_ozone.csv"
    else:
        sens_file = "sensitivity_radiative_forcing.csv"
        taylor_file = "taylor_param_radiative_forcing.csv"

    with pkg_resources.files(data).joinpath(sens_file).open("r") as f1, \
         pkg_resources.files(data).joinpath(taylor_file).open("r") as f2:

        if prepare:
            df = prepare_data(f1)
            df_t = prepare_data(f2)
        else:
            df = pd.read_csv(f1, sep=", ", engine="python")
            df_t = pd.read_csv(f2, sep=", ", engine="python")

    return df, df_t
