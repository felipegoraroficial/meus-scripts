import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = 'DELETE FROM Sua_Tabela WHERE "COLUNA_1" = "sua condição";'

cursor.execute(sql_query)


conn.close()