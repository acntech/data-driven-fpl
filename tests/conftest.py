"""Definitions for global test fixtures."""
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml


@pytest.fixture(scope="function", name="mock_config_path")
def fixture_mock_config_path(tmp_path):
    """Fixture for creating a config file.

    Returns:
        pathlib.Path
            The path to the config file.
    """
    config_file_path = Path(tmp_path).joinpath("test_config.yaml")
    config_file = {
        "azure": {
            "STORAGE_ACCOUNT_URL": "https://mock-url.net/",
            "STORAGE_CONTAINERS": ["container1", "container2"],
        }
    }

    with open(config_file_path, "w") as file:
        yaml.dump(config_file, file)

    return config_file_path


@pytest.fixture
def elements_df():
    return pd.read_csv("test_data/test_interim/test_elements.csv")


@pytest.fixture
def teams_df():
    return pd.read_csv("test_data/test_interim/test_teams.csv")
