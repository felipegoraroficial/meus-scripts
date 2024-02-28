import requests
from bs4 import BeautifulSoup
from google.cloud import storage
import json
import pandas as pd
import numpy as np
import re
import pytest


headers = {'user-agent': 'Mozilla/5.0'}

#lista unificada para cada atributo html
list_todos = []

"""
Esta função faz uma requisição GET para cada página de resultados da busca por "nintendo switch" no site da Magazine Luiza,
extrai várias informações sobre cada produto listado e as salva em um arquivo JSON.
"""
def get_data():

    for page_number in range(1,17):
        # Faça uma requisição GET para cada página de resultados
        resposta = requests.get(f"https://www.magazineluiza.com.br/busca/nintendo+switch/?page={page_number}")
        sopa = resposta.text
        sopa_bonita = BeautifulSoup(sopa,'html.parser')

        # Encontre todos os elementos relevantes na página
        list_titulo = sopa_bonita.find_all('h2',{'data-testid':'product-title'})
        list_preco_promo = sopa_bonita.find_all('p',{'data-testid':'price-value'})
        list_condition_promo = sopa_bonita.find_all('span',{'data-testid':'in-cash'})
        list_parcelamento = sopa_bonita.find_all('p',{'data-testid':'installment'})
        img_tags = sopa_bonita.find_all('img')
        img_srcs = [img['src'] for img in img_tags]

        for titulo, preco_promo, condition_promo, parcelado, img in zip(list_titulo, list_preco_promo, list_condition_promo, list_parcelamento, img_srcs):
            # Extraia o texto de cada elemento e faça algumas limpezas
            titulo = titulo.text
            moeda = preco_promo.text
            moeda = moeda[0] + moeda[1]
            preco_promo = preco_promo.text.replace('R$','').replace('\xa0','').replace('.','').replace(',','.')
            condition_promo = condition_promo.text
            parcelado = parcelado.text.replace('R$','').replace('\xa0','').replace('.','').replace(',','.')
            imagem = str(img).replace('[', '').replace(']', '')

            # Adicione os atributos à lista 'list_todos' como um dicionário
            list_todos.append({
                'titulo': titulo,
                'moeda': moeda,
                'preco_promo': preco_promo,
                'condition_promo': condition_promo,
                'parcelado': parcelado,
                'imagem': imagem
            })

    # Salvar o arquivo JSON no Google Cloud Storage
    bucket_name = "lakehouse_13"
    folder_name = "raw/"
    file_name = "magalu-nintendo.json"
    json_data = json.dumps(list_todos)

    # Credenciais de autenticação do Google Cloud Storage
    client = storage.Client.from_service_account_json('/home/fececa/scrapy-project-415116-fd70d3d10223.json')
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(folder_name + file_name)  # Aqui é onde especificamos o caminho do arquivo dentro da pasta
    blob.upload_from_string(json_data)

    return resposta.status_code, list_todos

# Chame a função get_data() e obtenha o status do request e a lista 'list_todos'
status_code, list_todos = get_data()

# Verifique se o status do request é 200
assert status_code == 200, "O status do request não é 200"
# Verifique se a lista 'list_todos' não está vazia
assert list_todos, "A lista 'list_todos' está vazia"