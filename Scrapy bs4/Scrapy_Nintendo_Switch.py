import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

headers = {'user-agent': 'Mozilla/5.0'}
list_todos = []

def scrap_magazine_luiza():

    for page_number in range(1,17):

        resposta = requests.get(f"https://www.magazineluiza.com.br/busca/nintendo+switch/?page={page_number}",
                                headers=headers)

        sopa = resposta.text

        sopa_bonita = BeautifulSoup(sopa,'html.parser')

        list_titulo = sopa_bonita.find_all('h2',{'data-testid':'product-title'})

        list_preco_promo = sopa_bonita.find_all('p',{'data-testid':'price-value'})

        list_condition_promo = sopa_bonita.find_all('span',{'data-testid':'in-cash'})

        list_parcelamento = sopa_bonita.find_all('p',{'data-testid':'installment'})


        for titulo, preco_promo,condition_promo, parcelado in zip(list_titulo,list_preco_promo,list_condition_promo,list_parcelamento):
            titulo = titulo.text
            moeda = preco_promo.text
            moeda = moeda[0] + moeda[1]
            preco_promo = preco_promo.text.replace('R$','').replace('\xa0','').replace('.','').replace(',','.')
            condition_promo = condition_promo.text
            parcelado = parcelado.text.replace('R$','').replace('\xa0','').replace('.','').replace(',','.')


            list_todos.append((titulo,moeda,preco_promo,condition_promo,parcelado))

    df = pd.DataFrame(list_todos, columns=['titulo','moeda','preco_promo','condition_promo','parcelado'])

    return df

data_nintendo = scrap_magazine_luiza()

def tratar_data(data_nintendo):

    data_nintendo['preco_promo'] = data_nintendo['preco_promo'].astype(np.float64).round(2)

    def extrair_memoria(info):
            # Usar regex para encontrar padrões "GB" ou "Gb" ou "gb" seguidos por números
        padrao = r'(\d+)\s*(G[gBb])'
        resultado = re.search(padrao, info)
        if resultado:
            # Se encontrado, retornar a correspondência
            return resultado.group(0)
        else:
            # Se não encontrado, retornar uma string vazia
            return '-'

    # Aplicar a função e criar a nova coluna "Memoria"
    data_nintendo['memoria'] = data_nintendo['titulo'].apply(extrair_memoria)

    oled = data_nintendo['titulo'].str.contains('Oled', case=False)
    oled = oled.replace({True: 'Sim', False: 'Nao'})
    data_nintendo['oled'] = oled

    lite = data_nintendo['titulo'].str.contains('Lite', case=False)
    lite = lite.replace({True: 'Sim', False: 'Nao'})
    data_nintendo['lite'] = lite

    controle = data_nintendo['titulo'].str.contains('Joy-con', case=False)
    controle = controle.replace({True: 'Sim', False: 'Nao'})
    data_nintendo['joy_con'] = controle

    data_nintendo['marca'] = 'Nintendo'

    data_nintendo['console'] = 'Nintendo Switch'

    return data_nintendo

console_game = tratar_data(data_nintendo)

console_game.to_csv('console_nintendo_switch.csv',index=False)

