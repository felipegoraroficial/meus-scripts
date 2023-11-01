import requests
import json
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account

api_key = "7b1b94b8-78ca-4f43-b31c-9b3f4199a1a4" 
google_credencial = service_account.Credentials.from_service_account_file("C:\\Users\\felip\\OneDrive\\Cursos e Certificados\\Data Scientis\\GoogleCloud\\credencial.json")


def nacao():

    nacao_list = list()

    for i in range(1,10):

        url = f"https://futdb.app/api/nations?page={i}" 
        


        headers = {"X-AUTH-TOKEN": api_key}
        
        response = json.loads(requests.request("GET", url=url, headers=headers).text)


        for item in response['items']:

            infos = {
                "ID Nacionalidade": item['id'],
                "Nacionalidade": item['name'],
                }
            
            nacao_list.append(infos)

    df = pd.DataFrame(nacao_list)

    return df
nacao_data = nacao()

def liga():

    liga_list = list()

    for i in range(1,3):

        url = f"https://futdb.app/api/leagues?page={i}" 
        


        headers = {"X-AUTH-TOKEN": api_key}
        
        response = json.loads(requests.request("GET", url=url, headers=headers).text)


        for item in response['items']:

            infos = {
                "ID Liga": item['id'],
                "Liga": item['name'],
                "ID Nacionalidade": item['nationId'],
                "Genero": item['gender'],
                }
            
            liga_list.append(infos)

    df = pd.DataFrame(liga_list)

    return df
liga_data = liga()

def clube():

    clube_list = list()

    for i in range(1,37):

        url = f"https://futdb.app/api/clubs?page={i}" 
        


        headers = {"X-AUTH-TOKEN": api_key}
        
        response = json.loads(requests.request("GET", url=url, headers=headers).text)


        for item in response['items']:

            infos = {
                "ID Clube": item['id'],
                "Clube": item['name'],
                "ID Liga": item['league'],
                }
            
            clube_list.append(infos)

    df = pd.DataFrame(clube_list)

    return df
clube_data = clube()

def jogadores():

    jogadores_list = list()

    for i in range(1,928):

        url = f"https://futdb.app/api/players?page={i}" 


        headers = {"X-AUTH-TOKEN": api_key}
        
        response = json.loads(requests.request("GET", url=url, headers=headers).text)


        for item in response['items']:

            infos = {
                "ID": item['id'],
                "ID Clube": item['club'],
                "ID Liga": item['league'],
                "ID Nacionalidade": item['nation'],
                "Nome": item['name'],
                "Idade": item['age'],
                "Data Nascimento": item['birthDate'],
                "Posição": item['position'],
                "Overall": item['rating'],
                "Pé Bom": item['foot'],
                "Overall": item['rating'],
                "Altura": item['height'],
                "Peso": item['weight'],
                "Genero": item['gender'],
                "Chute": item['shooting'],
                "Passe": item['passing'],
                "Drible": item['dribbling'],
                "Defesa": item['defending'],
                "Fisico": item['physicality'],
                "Atributo de Goleiro": item['goalkeeperAttributes'],
                }
            
            jogadores_list.append(infos)

    df = pd.DataFrame(jogadores_list)

    return df
jogadores_data = jogadores()

def tratar_dados(jogadores_data,clube_data,liga_data,nacao_data):

    # Mesclagem encadeada dos dataframes
    fifa = jogadores.merge(clube[['ID Clube', 'Clube']], left_on='ID Clube', right_on='ID Clube', how='left')\
                .merge(liga[['ID Liga', 'Liga', 'Genero']], left_on='ID Liga', right_on='ID Liga', how='left')\
                .rename(columns={'Genero_x': 'Genero', 'Genero_y': 'Genero Liga'})\
                .merge(nacao[['ID Nacionalidade', 'Nacionalidade']], left_on='ID Nacionalidade', right_on='ID Nacionalidade', how='left')

    # Preenchimento de valores NaN
    fifa.fillna({'Genero Liga': 'Não se Aplica', 'Atributo de Goleiro': 0, 'IMC': 0}, inplace=True)

    # Conversão de tipos
    fifa['Atributo de Goleiro'] = fifa['Atributo de Goleiro'].astype(int)
    fifa['Altura'] = fifa['Altura'] / 100

    # Cálculo do IMC
    fifa['IMC'] = fifa['Peso'] / (fifa['Altura'] ** 2)

    # Classificação do IMC
    def classificar_imc(imc):
        if imc == 0:
            return "Não se Aplica"
        elif 0 < imc < 18.5:
            return "Abaixo do Peso"
        elif 18.5 <= imc < 24.9:
            return "Peso Normal"
        elif 24.9 <= imc < 29.9:
            return "Sobrepeso"
        else:
            return "Obeso"

    fifa['Classificacao IMC'] = fifa['IMC'].apply(classificar_imc)

    return fifa
fifa = tratar_dados(jogadores_data,clube_data,liga_data,nacao_data)

bucket_name = "airflow_pipelines"
bucket = storage.Client(credentials=google_credencial).get_bucket(bucket_name)
blob = bucket.blob("fifa_file.json")
print(f"Salvando arquivo em: {bucket_name}")
blob.upload_from_string(data=json.dumps(fifa), content_type='application/json')
