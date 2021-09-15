"""Methods to return common paths."""

from pathlib import Path


def get_root_path():
    """
    Return the absolute path to the root of this repository.

    Returns:
        Path
            The path to the root directory.
    """
    return Path(__file__).absolute().parents[2]


def get_data_path():
    """Return absolute path to the data directory.

    Returns:
        Path
            The path to the data directory.
    """
    return get_root_path().joinpath("data")


def get_raw_data_path():
    """Return absolute path to the raw data directory.

    Returns:
        Path
            The path to the raw data directory.
    """
    return get_data_path().joinpath("raw")


def get_config_file_path():
    """Return the absolute path to the config file.

    Returns:
        Path
            The path to the config file.
    """
    return get_root_path() / "config" / "config.yaml"
