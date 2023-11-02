import pandas as pd
from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient,__version__
from azure.core.pipeline.transport import RequestsTransport
from io import BytesIO
import io

account_name = 'nome do blob'
account_key = 'sua key'
containername = 'nome do container'
transport = RequestsTransport(connection_verify = False)

data = {
    'Coluna1': [1, 2, 3],
    'Coluna2': ['A', 'B', 'C']
}
df = pd.DataFrame(data)

def salvar_arquivo(df): 
    
    blob_name = 'nome do arquivo.xlsx'

    blbo_service_client = BlobServiceClient(account_url= f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key,
                                            transport=transport)
    container_client = blbo_service_client.get_container_client(containername)
    blob_client = container_client.get_blob_client(blob_name)

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    blob_client.upload_blob(output, overwrite=True)

