import pandas as pd
from pandas import ExcelFile
import os

path = 'seu caminho dbfs'

def ler_um_Arquivo(path):

    df = pd.ExcelFile(path,engine='openpyxl')
    df = df.parse("sua sheet",header=0)

    return df

def ler_um_Arquivo(path):

    dataframes = []

    for filename in os.listdir(path):

        df = pd.ExcelFile(path,engine='openpyxl')
        df = df.parse("sua sheet",header=0)
        df['file_name'] = filename

        dataframes.append(df)

    return dataframes