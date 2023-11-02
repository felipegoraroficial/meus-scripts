import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = "DROP TABLE Sua_Tabela;"

cursor.execute(sql_query)


conn.close()