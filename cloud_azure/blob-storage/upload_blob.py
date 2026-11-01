"""Upload a local file to Azure Blob Storage using environment configuration."""
import argparse
import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient


def upload_to_blob(local_file_path, container_name, blob_name):
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    with BlobServiceClient.from_connection_string(connection_string) as service:
        blob = service.get_blob_client(container=container_name, blob=blob_name)
        with open(local_file_path, "rb") as data:
            blob.upload_blob(data, overwrite=True)
    print(f"Uploaded: {blob_name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--container", default=os.getenv("AZURE_STORAGE_CONTAINER"))
    parser.add_argument("--blob-name")
    args = parser.parse_args()
    if not os.getenv("AZURE_STORAGE_CONNECTION_STRING"):
        parser.error("Set AZURE_STORAGE_CONNECTION_STRING before uploading.")
    if not args.container:
        parser.error("Set AZURE_STORAGE_CONTAINER or pass --container.")
    if not args.file.is_file():
        parser.error("The input file does not exist.")
    upload_to_blob(args.file, args.container, args.blob_name or args.file.name)


if __name__ == "__main__":
    main()
