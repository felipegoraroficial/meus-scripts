from google.oauth2 import service_account
from google.cloud import storage
import pandas as pd
import json
from pandas import json_normalize

google_credencial = service_account.Credentials.from_service_account_file("C:\\Users\\felip\\OneDrive\\Cursos e Certificados\\Data Scientis\\GoogleCloud\\credencial.json")
bucket_name = 'airflow_pipelines'
json_file_name = 'pokemon_file.json'

def read_file_bucket(bucket_name,json_file_name,google_credencial):

    storage_client = storage.Client(credentials=google_credencial)

    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(json_file_name)

    content = blob.download_as_text()

    df = pd.read_json(content)

    df = json_normalize(df['pokemon_list'])

    return df
df = read_file_bucket(bucket_name,json_file_name,google_credencial)

print(f"The file {json_file_name} in Bucket {bucket_name} is loading")

print(df)
