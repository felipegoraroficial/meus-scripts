import pandas as pd
import sqlite3

data = {
    'Coluna1': [1, 2, 3],
    'Coluna2': ['A', 'B', 'C']
}
df = pd.DataFrame(data)

conn = sqlite3.connect('caminho do banco de dados SQLite.db')

df.to_sql(name='nome da tabela', con=conn, if_exists='replace', index=False)

conn.commit()
conn.close()