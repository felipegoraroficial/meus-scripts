from google.oauth2 import service_account
from google.cloud import storage

google_credencial = service_account.Credentials.from_service_account_file("C:\\Users\\felip\\OneDrive\\Cursos e Certificados\\Data Scientis\\GoogleCloud\\credencial.json")

def delete_bucket(bucket_name):


    storage_client = storage.Client(credentials=google_credencial)

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(f"Bucket {bucket.name} deleted")


if __name__ == "__main__":
    delete_bucket(bucket_name="ast_teste_criacao_bucket")