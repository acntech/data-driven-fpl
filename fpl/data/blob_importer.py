"""DataImporter class definition."""
from pathlib import Path

from azure.storage.blob import ContainerClient
from progress.bar import Bar

from fpl.utils import configs, paths


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
            config_file_path = paths.get_config_file_path()
        self.__config_file_path = config_file_path
        self.__config = configs.get_config(self.__config_file_path)

        if raw_data_path is None:
            raw_data_path = paths.get_raw_data_path()
        self.__raw_data_path = raw_data_path

    def download_blobs_in_containers(self):
        """Download all blobs in configured container to raw data directory."""
        storage_account_url = self.__config["azure"]["STORAGE_ACCOUNT_URL"]
        container_names = self.__config["azure"]["STORAGE_CONTAINERS"]
        for container_name in container_names:
            data_path = Path(self.__raw_data_path, container_name)
            data_path.mkdir(parents=True, exist_ok=True)

            container_client = ContainerClient.from_container_url(
                storage_account_url + "/" + container_name
            )
            blob_list = [blob["name"] for blob in container_client.list_blobs()]
            existing_files = [f.name for f in data_path.iterdir() if ".json" in f.name]
            blobs_to_download = [blob for blob in blob_list if blob not in existing_files]

            blob_bar = Bar(f"Downloading blobs from {container_name}", max=len(blobs_to_download))
            for blob in blobs_to_download:
                with open(Path(data_path, blob), "w", encoding="utf8") as file:
                    data = container_client.get_blob_client(blob=blob).download_blob().readall()
                    file.write(data.decode("utf-8"))
                    blob_bar.next()
            blob_bar.finish()
