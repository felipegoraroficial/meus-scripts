import requests
import pandas as pd
import json
from google.cloud import storage
from google.oauth2 import service_account

google_credencial = service_account.Credentials.from_service_account_file("C:\\Users\\felip\\OneDrive\\Cursos e Certificados\\Data Scientis\\GoogleCloud\\credencial.json")



def extract_pokemon():

    

    url = "https://pokeapi.co/api/v2/pokemon/"
    pokemon_list = {'pokemon_list': list()}

    while url != None:
        payload={}
        headers = {}
        response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
        url = response["next"]

        for item in response["results"]:
            pokemon_name = item["name"]
            url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
            response_pokemon = json.loads(requests.request("GET", url_pokemon, headers=headers, data=payload).text)

            infos = {
                "name": pokemon_name,
                "id": response_pokemon["id"],
                "height": response_pokemon["height"],
                "weight": response_pokemon["weight"],
                "is_default": response_pokemon["is_default"]
            }

            pokemon_list['pokemon_list'].append(infos)
            print(response_pokemon["id"])

            return pokemon_list
        
pokemon_list = extract_pokemon()

df_pokemon = pd.DataFrame(pokemon_list)
df_pokemon.to_json('Data/pokemon_file.json', orient='records', lines=True)

bucket_name = "airflow_pipelines"
bucket = storage.Client(credentials=google_credencial).get_bucket(bucket_name)
blob = bucket.blob("pokemon_file.json")
print(f"Salvando arquivo em: {bucket_name}")
blob.upload_from_string(data=json.dumps(pokemon_list), content_type='application/json')