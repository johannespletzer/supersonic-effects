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

def load_data(prepare=False, mode='Ozone'):
    '''Load sensitivity and taylor data from file as a pandas DataFrame'''

    if mode not in ["Ozone","Radiative_Forcing"]:
        raise ValueError("mode keyword should be either Ozone or Radiative_Forcing!")

    if prepare:
        if mode=='Ozone':
            df = prepare_data('./data/sensitivity_ozone.csv')
            df_t = prepare_data('./data/taylor_param_ozone.csv')
        elif mode=='Radiative_Forcing':
            df = prepare_data('./data/sensitivity_radiative_forcing.csv')
            df_t = prepare_data('./data/taylor_param_radiative_forcing.csv')
    else:
        if mode=='Ozone':
            df = pd.read_csv('./data/sensitivity_ozone.csv', sep=', ', engine='python')
            df_t = pd.read_csv('./data/taylor_param_ozone.csv', sep=', ', engine='python')
        elif mode=='Radiative_Forcing':
            df = pd.read_csv('./data/sensitivity_radiative_forcing.csv', sep=', ', engine='python')
            df_t = pd.read_csv('./data/taylor_param_radiative_forcing.csv', sep=', ', engine='python')

    return df, df_t
