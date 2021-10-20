"""Module for testing BlobImporter."""
import pytest

from fpl.data.blob_importer import BlobImporter
from fpl.utils import configs


class TestBlobImporter:
    """Test class for BlobImporter."""

    @staticmethod
    def test_download_blobs_in_containers(tmp_path, mocker, mock_config_path):
        """Tests BlobImporter.download_all_blobs_in_container.

        Args:
            tmp_path : Path
                Built-in fixture for temporary path.
            mocker : MagicMock
                Built-in fixture for mocking objects.
            mock_config_path : Path
                Mocked config path.
        """
        mock_blob_name = "mock_blob.json"
        mock_container_client = mocker.patch(
            "fpl.data.blob_importer.ContainerClient.from_container_url"
        )
        mock_list_blobs = mocker.patch(
            "fpl.data.blob_importer.ContainerClient.from_container_url.list_blobs",
            return_value=[{"name": mock_blob_name}],
        )
        mock_download_blob = mocker.patch(
            "fpl.data.blob_importer.ContainerClient.from_container_url.get_blob_client.download_blob.readall",
            return_value=b"mock_blob_content",
        )

        mock_container_client.return_value.list_blobs = mock_list_blobs
        mock_container_client.return_value.get_blob_client.return_value.download_blob.return_value.readall = (
            mock_download_blob
        )
        mock_config = configs.get_config(mock_config_path)

        blob_importer = BlobImporter(config_file_path=mock_config_path, raw_data_path=tmp_path)
        blob_importer.download_blobs_in_containers()

        mock_container_client.assert_called() == len(mock_config["azure"]["STORAGE_CONTAINERS"])
        mock_list_blobs.assert_called() == len(mock_config["azure"]["STORAGE_CONTAINERS"])
        mock_download_blob.assert_called() == len(mock_config["azure"]["STORAGE_CONTAINERS"])

        # Rewrite to recurively test that each dir in data/raw holds a json.
        downloaded_files = [f.name for f in tmp_path.glob("**/*") if ".json" in f.name]
        assert downloaded_files == [f"{mock_blob_name}" for i in range(len(downloaded_files))]
