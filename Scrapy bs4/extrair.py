import requests
from bs4 import BeautifulSoup
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

    # Transforme a lista 'list_todos' em JSON e salve em um arquivo
    with open('list_todos.json', 'w') as f:
        json.dump(list_todos, f)

    return resposta.status_code, list_todos

# Chame a função get_data() e obtenha o status do request e a lista 'list_todos'
status_code, list_todos = get_data()