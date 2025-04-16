import pandas as pd

def prepare_data(filepath):
    '''Calculate mean, min, max columns'''

    # Read data
    df = pd.read_csv(filepath, sep=', ', engine='python')

    # Average and range
    df['Mean']    = df[['Transatlantic_Corridor','South_Arabian_Sea']].mean(axis=1)
    df['Range']   = (df['South_Arabian_Sea'] - df['Transatlantic_Corridor']).abs()
    df['Max_val'] = df['Mean'] + df['Range']
    df['Min_val'] = df['Mean'] - df['Range']

    return df

def load_data(prepare=False):
    '''Load sensitivity and taylor data from file as a pandas DataFrame'''

    if prepare:
        df_o3 = prepare_data('./data/sensitivity_ozone.csv')
        df_rf = prepare_data('./data/sensitivity_radiative_forcing.csv')
        df_t = prepare_data('./data/taylor_param.csv')
    else:
        df_o3 = pd.read_csv('./data/sensitivity_ozone.csv', sep=', ', engine='python')
        df_rf = pd.read_csv('./data/sensitivity_radiative_forcing.csv', sep=', ', engine='python')
        df_t = pd.read_csv('./data/taylor_param.csv', sep=', ', engine='python')

    return df_o3, df_rf, df_t
