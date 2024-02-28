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

    url = 'https://lista.mercadolivre.com.br/nintendo-sitwitch'
    resposta = requests.get(url, headers=headers)
    sopa_bonita = BeautifulSoup(resposta.text, 'html.parser')

    link_tags = sopa_bonita.find_all('a')
    filtered_links = [link for link in link_tags if 'nintendo switch' in link.get('title', '').lower() and not re.search(r'lista', link.get('href', '').lower())]

    # Iterar sobre os links filtrados
    for link_tag in filtered_links:
        # Obter o valor do atributo 'href' de cada link
        link = link_tag.get('href')

        resposta_produto = requests.get(link)
        sopa_produto = BeautifulSoup(resposta_produto.text, 'html.parser')

        list_titulo = sopa_produto.find_all('h1', {'class': 'ui-pdp-title'})
        list_moeda = sopa_produto.find_all('span', {'class': 'andes-money-amount__currency-symbol'})
        list_preco_promo = sopa_produto.find_all('span', {'class': 'andes-money-amount__fraction'})
        list_condition_promo = sopa_produto.find_all('span', {'class': 'andes-money-amount__discount'})
        img_tags = sopa_produto.find_all('img', class_='ui-pdp-image ui-pdp-gallery__figure__image')
        img_srcs = [img.get('src') for img in img_tags]
        list_parcela_green = sopa_produto.find_all('p', {'class': 'ui-pdp-color--GREEN ui-pdp-size--MEDIUM ui-pdp-family--REGULAR'})
        list_parcela_black = sopa_produto.find_all('p', {'class': 'ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--REGULAR'})
        list_parcelado = list_parcela_green + list_parcela_black


        for titulo, moeda, preco_promo,condition_promo, img, parcelado in zip(list_titulo, list_moeda, list_preco_promo,list_condition_promo, img_srcs,list_parcelado):
            # Extraia o texto de cada elemento e faça algumas limpezas
            titulo_text = titulo.text
            moeda = moeda.text
            preco_promo_text = preco_promo.text.replace('\xa0','').replace('.','').replace(',','.')
            condition_promo_text = condition_promo.text
            imagem = str(img).replace('[', '').replace(']', '')
            parcelado_text = parcelado.text    


            # Adicione os atributos à lista 'list_todos' como um dicionário
            list_todos.append({
                'titulo': titulo_text,
                'moeda': moeda,
                'preco_promo': preco_promo_text,
                'condition_promo': condition_promo_text,
                'parcelado': parcelado_text,
                'imagem': imagem 


            })

    # Salvar o arquivo JSON no Google Cloud Storage
    bucket_name = "lakehouse_13"
    folder_name = "raw/"
    file_name = "ml-nintendo.json"
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