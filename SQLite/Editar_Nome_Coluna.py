import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = 'ALTER TABLE Sua_Tabela RENAME COLUMN "coluna_1" TO "coluna_2";'

cursor.execute(sql_query)


conn.close()