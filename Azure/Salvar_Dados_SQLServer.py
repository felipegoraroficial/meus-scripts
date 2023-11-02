import pandas as pd
import pyodbc


server = 'seu server'
database = 'sua database'
username = 'seu username'
password = 'seu password'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD' + password)
cur = cnxn.cursor()


data = {
    'Coluna1': [1, 2, 3],
    'Coluna2': ['A', 'B', 'C']
}
df = pd.DataFrame(data)

quer_delete = 'DELETE FROM nome-da-tabela WHERE COLUNA_1 = "uma variavel"'
cur.execute(quer_delete)

tabela = 'nome-da-tabela'
df.to_sql(name=tabela, con=cur, if_exists='append', index=False)


cnxn.close()
