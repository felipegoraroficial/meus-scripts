import pandas as pd
import pyodbc


server = 'seu server'
database = 'sua database'
username = 'seu username'
password = 'seu password'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD' + password)
cur = cnxn.cursor()

query_azure = 'SELECT * FROM SUA_TABELA WHERE COLUNA_1 = "Male" AND COLUNA_2 >= 20;'
df = pd.read_sql(query_azure,cnxn)
