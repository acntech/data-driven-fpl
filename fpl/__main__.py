"""The main module."""
from fpl import __version__
from fpl.data_import.blob_importer import BlobImporter


def start_script():
    """Demo only."""
    blob_import = BlobImporter()
    blob_import.download_all_blobs_in_container()
    print(__version__)


if __name__ == "__main__":
    start_script()
