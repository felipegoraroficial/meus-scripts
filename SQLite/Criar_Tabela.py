import pandas as pd
import sqlite3

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

cursor = conn.cursor()

sql_query = """CREATE TABLE Sua_Tabela
(
    Coluna_1 CHAR(3),
    Coluna_2 VARCHAR(30),
    Coluna_3 TEXT,
    Coluna_4 FLOAT,
    Coluna_5 INT,
    Coluna_6 DATE
        );"""

cursor.execute(sql_query)


conn.close()