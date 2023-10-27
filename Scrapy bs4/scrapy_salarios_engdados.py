import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np


def getdata():

    headers = {'user-agent': 'Mozilla/5.0'}

    list_todos = []
    
    for i in range(1,5):

        resposta = requests.get(f"https://www.glassdoor.com.br/Sal%C3%A1rios/engenheiro-de-dados-sal%C3%A1rio-SRCH_KO0,19_IP{i}.htm?clickSource=searchBtn",
                                headers=headers)

        sopa = resposta.text

        sopa_bonita = BeautifulSoup(sopa,'html.parser')

        list_empresas = sopa_bonita.find_all('h3',
                                        {'data-test':re.compile('salaries-list-item-.*-employer-name')})


        list_salario = sopa_bonita.find_all('div',
                                            {'data-test':re.compile('salaries-list-item-.*-salary-info')})


        list_jobtitle = sopa_bonita.find_all('span',
                                            {'data-test':re.compile('salaries-list-item-.*-job-title')})


        list_salario_count = sopa_bonita.find_all('span',
                                            {'data-test':re.compile('salaries-list-item-.*-salary-count')})


        list_salario_range = sopa_bonita.find_all('span',
                                            {'data-test':re.compile('salaries-list-item-.*-salary-range')})



        for empresas, salario, job, minimo, faixa in zip(list_empresas,list_salario,list_jobtitle,list_salario_count,list_salario_range):
            nome_empresa = empresas.find('a').text
            moeda = salario.contents[1].text
            moeda = moeda[0] + moeda[1]
            str_salario = salario.contents[1].text
            str_salario = str_salario.replace('R$','').replace('\xa0','').replace('.','')
            job_str = job.contents[0].text.title()
            salario_registro = minimo.contents[0].text.replace(' salários','')
            faixa_salario = faixa.contents[0].text.title()



            list_todos.append((nome_empresa,moeda,str_salario,job_str,salario_registro,faixa_salario))

    df = pd.DataFrame(list_todos, columns=['Empresas','Moeda','Salarios','Titulo Emprego','Salario Registrado','Faixa Salario'])

    df['Salarios'] = df['Salarios'].astype(np.float32)
    df['Salario Registrado'] = df['Salario Registrado'].astype(np.int64)

    def extrair_min_max(faixa):
        valores = re.findall(r'\d+\s*Mil|\d+', faixa)
        valores_int = [int(re.sub(r'\s*Mil', '000', valor)) for valor in valores]
        return {'minimo': min(valores_int), 'maximo': max(valores_int)}

    # Aplicar a função para criar as colunas "minimo" e "maximo"
    df[['Salario Minimo', 'Salario Maximo']] = df['Faixa Salario'].apply(extrair_min_max).apply(pd.Series)

    df = df.drop('Faixa Salario', axis=1)

    df.to_json('eng_dados.json', orient='records')







