from google.cloud import bigquery

# Inicialize o cliente BigQuery
client = bigquery.Client.from_service_account_json('caminho da sua credencial')

# Substitua 'seu-projeto' pelo ID do seu projeto no Google Cloud
projeto = 'scrapy-project-415116'
conjunto_de_dados = 'Nintendo'
tabela = 'Kabum'

# Construa uma referência à tabela
tabela_ref = client.dataset(conjunto_de_dados).table(tabela)

# Busque os dados da tabela
dados_da_tabela = client.get_table(tabela_ref)

# Visualize os primeiros 5 registros
for row in client.list_rows(dados_da_tabela, max_results=5):
    print(row)
