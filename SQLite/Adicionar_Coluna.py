import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = 'ALTER TABLE Sua_Tabela ADD "Nome_Coluna" VARCHAR(20);'

cursor.execute(sql_query)


conn.close()