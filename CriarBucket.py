from google.oauth2 import service_account
from google.cloud import storage

google_credencial = service_account.Credentials.from_service_account_file("C:\\Users\\felip\\OneDrive\\Cursos e Certificados\\Data Scientis\\GoogleCloud\\formidable-app-401523-2b7f82d9dec0.json")

def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client(credentials=google_credencial)

    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created")


if __name__ == "__main__":
    create_bucket(bucket_name="ast_teste_criacao_bucket")


