"""Definitions for global test fixtures."""
import json
from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="function", name="mock_config_path")
def fixture_mock_config_path(tmp_path):
    """Fixture for creating a config file

    Returns:
        pathlib.Path
            The path to the config file
    """
    config_file_path = Path(tmp_path).joinpath("test_config.yaml")
    config_file = {
        "azure": {
            "STORAGE_ACCOUNT_URL": "https://martinfplstats1337.blob.core.windows.net/",
            "FPL_2020_CONTAINER": "2020-fpl-data",
            "FPL_2021_CONTAINER": "2021-fpl-data",
        }
    }

    with open(config_file_path, "w") as file:
        yaml.dump(config_file, file)

    return config_file_path
