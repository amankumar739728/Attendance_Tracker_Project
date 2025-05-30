import os
from azure_connection import AzureConnection
from dotenv import load_dotenv

load_dotenv()

"""

 #1.Check if the file already exists in the Downloads folder If it does, skip the download.
 #2.If it doesn't, download the file from Azure Blob Storage and save it to the Downloads folder.
 
"""
 
#This script downloads a log file from Azure Blob Storage and searches for a keyword in the log file.
def download_log_from_azure():
    CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME")
    BLOB_NAME = os.environ.get("AZURE_BLOB_NAME")
    if not CONNECTION_STRING or not CONTAINER_NAME or not BLOB_NAME:
        raise ValueError("Please set the environment variables for Azure Storage connection string, container name, and blob name.")

    # Ensure Downloads directory exists
    downloads_dir = os.path.join(os.getcwd(), "Downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    # Check if the file already exists
    download_path = os.path.join(downloads_dir, BLOB_NAME)
    if os.path.exists(download_path):
        print(f"File '{BLOB_NAME}' already exists in Downloads folder. Skipping download.")
    else:
        print("Starting download...")
        azure_conn = AzureConnection(CONNECTION_STRING, CONTAINER_NAME)
        azure_conn.download_log_file(BLOB_NAME, download_path)
        print("Download complete.")

    return download_path

def search_log(filename, keyword):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if keyword.lower() in line.lower():
                    yield line.strip()
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error: {e}")

def show_batch(generator, size=10):
    # zip used to combines the two lists, element by element:
    batch = [entry for _, entry in zip(range(size), generator)]
    if batch:
        print(f"\n{'='*50}\nShowing {len(batch)} results:\n{'='*50}")
        for i, entry in enumerate(batch, 1):
            print(f"{i}. {entry}")
        return False
    print("\nNo more results.")
    return True

def main():
    filename = download_log_from_azure()  # Automatically download log file from Azure Storage
    #serch for keyword==(POSSIBLE BREAK-IN ATTEMPT)
    keyword = input("Enter keyword to search for: ").strip()
    if not keyword:
        print("Keyword cannot be empty.")
        return

    print(f"\nSearching for '{keyword}' in {filename}...")
    generator = search_log(filename, keyword)
    
    done = show_batch(generator)
    while not done:
        user_action = input("\nType 'next' for more or 'q' to quit: ").strip().lower()
        if user_action == 'q':
            print("Search terminated by user.")
            break
        elif user_action == 'next':
            done = show_batch(generator)
        else:
            print("Invalid input. Type 'next' to see more results or 'q' to quit.")

if __name__ == "__main__":
    main()
