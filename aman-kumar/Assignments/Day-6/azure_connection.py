from azure.storage.blob import BlobServiceClient
import os

class AzureConnection:
    def __init__(self, connection_string, container_name):
        """
        Initialize the AzureConnection class with the connection string and container name.
        """
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def download_log_file(self, blob_name, download_path):
        """
        Download a log file from Azure Blob Storage.
        :param blob_name: Name of the blob (file) in the container.
        :param download_path: Local path to save the downloaded file.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(download_path, "wb") as file:
                file.write(blob_client.download_blob().readall())
            print(f"File '{blob_name}' downloaded successfully to '{download_path}'.")
        except Exception as e:
            print(f"Error downloading file: {e}")

    def list_blobs(self):
        """
        List all blobs (files) in the container.
        """
        try:
            blobs = self.container_client.list_blobs()
            print("Blobs in the container:")
            for blob in blobs:
                print(f"- {blob.name}")
        except Exception as e:
            print(f"Error listing blobs: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your Azure Storage account connection string and container name
    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=datalakeaman7397;AccountKey=5OO8LWRNY3I+ernjNsmac7Mc3kOO3h0zRXTGUrcBwnfKXCsX57u8LhZN3kA3tSFlhHAuzgcDs+3K+ASt+M5EeQ==;EndpointSuffix=core.windows.net"
    CONTAINER_NAME = "source"

    # Initialize AzureConnection
    azure_conn = AzureConnection(CONNECTION_STRING, CONTAINER_NAME)

    # List blobs in the container
    azure_conn.list_blobs()

    # Download a specific log file
    BLOB_NAME = "SSH.log"  # Replace with the name of your log file
    
    # Create 'Downloads' folder path in current directory
    downloads_dir = os.path.join(os.getcwd(), "Downloads")

    # Create the folder if it doesn't exist
    os.makedirs(downloads_dir, exist_ok=True)

    # Define full path to save SSH.log inside Downloads
    DOWNLOAD_PATH = os.path.join(downloads_dir, "SSH.log")
    azure_conn.download_log_file(BLOB_NAME, DOWNLOAD_PATH)