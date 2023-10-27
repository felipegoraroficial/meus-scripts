import requests
import json
import pandas as pd

api_key = "7b1b94b8-78ca-4f43-b31c-9b3f4199a1a4" 

def nacao():

    nacao_list = list()

    for i in range(1,11):

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

    for i in range(1,4):

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

    for i in range(1,38):

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

    for i in range(1,929):

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
                "Posição": item['position'],
                "Overall": item['rating'],
                "Pé Bom": item['foot']
                }
            
            jogadores_list.append(infos)

    df = pd.DataFrame(jogadores_list)

    return df
jogadores_data = jogadores()



