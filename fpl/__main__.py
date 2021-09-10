"""The main module."""
from fpl.data.get_data import download_all


def start_script():
    """Start the script."""
    download_all("2021-fpl-data")


if __name__ == "__main__":
    start_script()
