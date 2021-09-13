"""Download data from Azure."""
import os
from pathlib import Path

from azure.storage.blob import ContainerClient
from dotenv import load_dotenv
from tqdm import tqdm

# Load environmental variables from .env it it exist or use default value.
load_dotenv()
STORAGE_ACCOUNT = os.getenv(
    "STORAGE_ACCOUNT_URL", "https://martinfplstats1337.blob.core.windows.net/"
)


def download_all(container_name: str, data_dir_path="data/raw"):
    """Download all new blobs to disk.

    Args:
        container_name (str): Storage account URL
        data_dir_path (str, optional): Path to download directory. Defaults to "data/raw".
    """
    # Connect to the container
    container_client = ContainerClient.from_container_url(STORAGE_ACCOUNT + "/" + container_name)

    download_path = Path(data_dir_path, container_name)
    download_path.mkdir(parents=True, exist_ok=True)

    # List all blobs in container and all .json files in download dir.
    blobs = [blob["name"] for blob in container_client.list_blobs()]

    # Get names of blobs found in container but not in directory.
    files_on_disk = [file.name for file in download_path.iterdir() if ".json" in file.name]

    # Compare  files on disk to blobs in container. Keep only names of blobs not found on disk.
    blobs_to_download = [blob for blob in blobs if blob not in files_on_disk]

    # Download all new blobs and write to disk.
    for blob in tqdm(blobs_to_download, desc="Downloading new blobs"):
        with open(Path(download_path, blob), "w", encoding="utf8") as file:
            data = container_client.get_blob_client(blob=blob).download_blob().readall()
            file.write(data.decode("utf-8"))
