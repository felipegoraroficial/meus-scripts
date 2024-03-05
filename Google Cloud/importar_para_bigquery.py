from google.cloud import storage
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

google_credencial = storage.Client.from_service_account_json('sua credencial')
bucket_name = "seu bucket"
arquivo = "nome do arquivo"
pasta= "nome da pasta/"

def read_file_bucket(bucket_name, pasta, arquivo, google_credencial):
    storage_client = google_credencial

    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(pasta + arquivo)

    # Baixar o arquivo como um fluxo de bytes
    content = blob.download_as_bytes()

    # Carregar o arquivo Parquet usando pyarrow
    df = pq.read_table(BytesIO(content)).to_pandas()

    return df

df = read_file_bucket(bucket_name, pasta, arquivo, google_credencial)


# Substitua 'seu-projeto' pelo ID do seu projeto no Google Cloud
projeto = 'codigo do projeto'
conjunto_de_dados = 'nome conjunto de dados'
tabela = 'nome da tabela'

# Especifique o nome completo da tabela no formato 'projeto.conjunto_de_dados.nome_tabela'
nome_tabela_completo = f'{projeto}.{conjunto_de_dados}.{tabela}'

# Carregue o DataFrame para o BigQuery
df.to_gbq(destination_table=nome_tabela_completo, project_id=projeto, if_exists='replace')



