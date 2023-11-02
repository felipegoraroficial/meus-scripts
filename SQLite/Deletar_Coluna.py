import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = 'ALTER TABLE Sua_Tabela DROP COLUMN "SUA_COLUNA";'

cursor.execute(sql_query)


conn.close()