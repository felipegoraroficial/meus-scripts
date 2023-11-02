import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')


sql_query = "SELECT Coluna_1, Coluna_2 FROM Sua_Tabela;"

df = pd.read_sql(sql_query, conn)


conn.close()