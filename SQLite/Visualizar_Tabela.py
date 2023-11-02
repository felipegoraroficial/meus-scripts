import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = """ SELECT name FROM sqlite_master
WHERE type='table;'"""

cursor.execute(sql_query)
print(cursor.fetchall())

conn.close()