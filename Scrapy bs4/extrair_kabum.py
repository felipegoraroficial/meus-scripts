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

    # Loop para iterar sobre as páginas
    for page_number in range(1, 3):  # Neste exemplo, apenas uma página será verificada (de 1 a 2)
        # Faça uma requisição GET para cada página de resultados
        resposta = requests.get(f"https://www.kabum.com.br/gamer/nintendo/consoles-nintendo?page_number={page_number}&page_size=20&facet_filters=&sort=most_searched")
        sopa_bonita = BeautifulSoup(resposta.text, 'html.parser')

        img_tags = sopa_bonita.find_all('img', class_='imageCard')
        img_srcs = [img.get('src') for img in img_tags]

        elements = sopa_bonita.find_all('a', {'data-smarthintproductid': True})

        for element in elements:
            codigo = element['data-smarthintproductid']
            url_produto = f"https://www.kabum.com.br/produto/{codigo}"
            
            resposta_produto = requests.get(url_produto)
            sopa_produto = BeautifulSoup(resposta_produto.text, 'html.parser')
            
            # Encontre todos os elementos relevantes na página
            list_titulo = sopa_produto.find_all('h1', {'class': 'sc-fdfabab6-6 jNQQeD'})
            list_preco_promo = sopa_produto.find_all('h4', {'class': 'sc-5492faee-2 ipHrwP finalPrice'})
            list_condition_promo = sopa_produto.find_all('span', {'class': 'sc-5492faee-3 igKOYC'})
            list_parcelamento = sopa_produto.find_all('span', {'class': 'cardParcels'})

            for titulo, preco_promo, condition_promo, parcelado, img in zip(list_titulo, list_preco_promo, list_condition_promo, list_parcelamento, img_srcs):  # Modificação aqui
                # Extraia o texto de cada elemento e faça algumas limpezas
                titulo_text = titulo.text if titulo else ""
                moeda = preco_promo.text
                moeda = moeda[0] + moeda[1]
                preco_promo_text = preco_promo.text.replace('R$','').replace('\xa0','').replace('.','').replace(',','.') if preco_promo else ""
                condition_promo_text = condition_promo.text.replace('\xa0','') if condition_promo else ""
                parcelado_text = parcelado.text.replace('R$','').replace('\xa0','').replace('.','').replace(',','.') if parcelado else ""
                imagem = str(img).replace('[', '').replace(']', '')

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
    file_name = "kabum-nintendo.json"
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