import pandas as pd
from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient,__version__
from azure.core.pipeline.transport import RequestsTransport
from io import BytesIO
import io

account_name = 'nome do blob'
account_key = 'sua key'
containername = 'nome do container'
transport = RequestsTransport(connection_verify = False)

def ler_blob_1_sheet():

    blob_name = 'nomearquivo.xlsx'

    blbo_service_client = BlobServiceClient(account_url= f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key,
                                            transport=transport)
    container_client = blbo_service_client.get_container_client(containername)
    blob_client = container_client.get_blob_client(blob_name)

    blob_data = blob_client.download_blob().readall()
    df = pd.read_excel(io.BytesIO(blob_data), sheet_name="sua sheet name", header=0, engine="openpyxl")

    return df
df_blob_1_sheet = ler_blob_1_sheet()


def ler_blob_mais_sheet():

    blob_name = 'nomearquivo.xlsx'

    blbo_service_client = BlobServiceClient(account_url= f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key,
                                            transport=transport)
    container_client = blbo_service_client.get_container_client(containername)
    blob_client = container_client.get_blob_client(blob_name)

    blob_data = blob_client.download_blob().readall()
    excel_data = pd.ExcelFile(BytesIO(blob_data))

    all_data = {}
    for sheet_name in excel_data.sheet_names:
        shee_df = excel_data.parse(sheet_name)
        all_data[sheet_name] = shee_df

    df = pd.concat(all_data.values(), ignore_index=True)

    return df
df_blob_1_sheet = ler_blob_mais_sheet()