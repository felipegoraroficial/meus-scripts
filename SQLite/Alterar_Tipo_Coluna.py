import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = "ALTER TABLE Sua_Tabela ALTER COLUMN Coluna_2 VARCHAR(15);"

cursor.execute(sql_query)


conn.close()