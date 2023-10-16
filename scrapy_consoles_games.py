import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def get_kabum():

    headers = {'user-agent': 'Mozilla/5.0'}

    list_todos = []

    page_number = 1

    while True:

        resposta = requests.get(f"https://www.kabum.com.br/gamer/nintendo/consoles-nintendo?page_number={page_number}&page_size=20&facet_filters=&sort=most_searched",
                                headers=headers)

        sopa = resposta.text

        sopa_bonita = BeautifulSoup(sopa,'html.parser')

        list_consoles = sopa_bonita.find_all('div',class_='sc-93fa31de-7 gopyRO productCard')

        list_preco = sopa_bonita.find_all('span',class_='sc-6889e656-2 bYcXfg priceCard')

        if not list_consoles:
        # Se não houver mais resultados, saia do loop
            break

        
        for nome, preco in zip(list_consoles,list_preco):
            console = nome.find('h2').text
            str_preco = preco.contents[0].text
            str_preco = str_preco.replace('R$','').replace('\xa0','').replace('.','').replace(',','.')


            list_todos.append((console,str_preco))
        
        page_number += 1

    df = pd.DataFrame(list_todos, columns=['Info','Preco'])

    df['Preco'] = df['Preco'].astype(np.float64).round(2)

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
    df['Memoria'] = df['Info'].apply(extrair_memoria)

    oled = df['Info'].str.contains('Oled', case=False)
    oled = oled.replace({True: 'Sim', False: 'Nao'})
    df['Oled'] = oled

    lite = df['Info'].str.contains('Lite', case=False)
    lite = lite.replace({True: 'Sim', False: 'Nao'})
    df['Lite'] = lite

    controle = df['Info'].str.contains('Joy-con', case=False)
    controle = controle.replace({True: 'Sim', False: 'Nao'})
    df['Joy-Con'] = controle

    df['Marca'] = 'Nintendo'

    df['Console'] = 'Nintendo Switch'

    df = df.drop('Info', axis=1)

    df = df[['Marca','Console','Preco','Lite','Oled','Joy-Con','Memoria']]

    df.to_json('consoles_games.json', orient='records')



