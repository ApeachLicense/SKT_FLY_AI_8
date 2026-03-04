import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=ratiotile;AccountKey=REDACTED_CREDENTIAL;EndpointSuffix=core.windows.net"

AZURE_CONTAINER_NAME = "ssssss"


def upload_to_blob(local_file_path, container_name, blob_name):
    # 1. Azure Portal에서 복사한 연결 문자열을 입력하세요.
    connect_str = AZURE_CONNECTION_STRING

    try:
        # 2. BlobServiceClient 생성
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # 3. 컨테이너 클라이언트 생성 (컨테이너가 없으면 새로 생성 가능)
        container_client = blob_service_client.get_container_client(container_name)

        # 만약 컨테이너가 없다면 생성 (선택 사항)
        # container_client.create_container()

        # 4. Blob 클라이언트 생성 (업로드할 파일 객체)
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        print(f"파일 업로드 중: {local_file_path}")

        # 5. 파일 업로드 실행
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"업로드 완료: {blob_name}")

    except Exception as ex:
        print(f"오류 발생: {ex}")



upload_to_blob(r'C:\Users\jwkim\Desktop\english\go.png', 'ssssss', 'go.png')

