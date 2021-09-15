"""DataImporter class definition."""
from pathlib import Path

from azure.storage.blob import ContainerClient
from tqdm import tqdm

from fpl.utils import config, paths


class BlobImporter:
    """DataImporter class."""

    def __init__(self, config_file_path=None, raw_data_path=None):
        """Set configuration parameters.

        Args:
            config_file_path (Path, optional)
                Path to config file. If set to None, the config file is retrieved
                from config directory.
            raw_data_path (Path, optional)
                Path to raw data file. If set to None, the config file is retrieved
                from config directory.
        """
        if config_file_path is None:
            self.__config_file_path = paths.get_config_file_path()
        self.__config = config.get_config(self.__config_file_path)
        if raw_data_path is None:
            self.__raw_data_path = paths.get_raw_data_path()

    def download_all_blobs_in_container(self):
        """Download all blobs in configured container to raw data directory."""
        connection_string = self.__config["azure"]["STORAGE_ACCOUNT_URL"]
        container_name = self.__config["azure"]["FPL_2021_CONTAINER"]
        container = ContainerClient.from_container_url(connection_string + "/" + container_name)
        blob_list = [blob["name"] for blob in container.list_blobs()]
        existing_files = [f.name for f in self.__raw_data_path.iterdir() if ".json" in f.name]
        blobs_to_download = [blob for blob in blob_list if blob not in existing_files]

        for blob in tqdm(blobs_to_download, desc=f"Downloading blobs from {container_name}"):
            with open(Path(self.__raw_data_path, blob), "w", encoding="utf8") as file:
                data = container.get_blob_client(blob=blob).download_blob().readall()
                file.write(data.decode("utf-8"))
