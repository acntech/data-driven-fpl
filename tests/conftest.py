"""Definitions for global test fixtures."""
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest
import yaml
from click.testing import CliRunner

RAW_DATA_DIR = "test_data/test_raw"
INTERIM_ELEMENTS_CSV = "test_data/test_interim/test_elements.csv"
INTERIM_TEAMS_CSV = "test_data/test_interim/test_teams.csv"
INTERIM_PARQUET = "test_data/test_interim/test_parquet"
PROCESSED_DATASET = ""


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

    with open(config_file_path, "w", encoding="utf-8") as file:
        yaml.dump(config_file, file)

    return config_file_path


@pytest.fixture(scope="function", name="mock_raw_data_path")
def fixture_mock_raw_data_path(tmp_path):
    raw_data_1 = {
        "events": [{"id": 1, "is_current": True}],
        "phases": [{"id": 1, "name": "Overall", "start_event": 1, "stop_event": 38}],
        "teams": [{"code": 3, "draw": 0, "form": None, "id": 1}],
        "elements": [{"chance_of_playing_next_round": None, "chance_of_playing_this_round": None}],
        "download_time": "2020-09-12 10:24:34.036515",
    }
    raw_data_2 = {
        "events": [{"id": 2, "is_current": False}],
        "phases": [{"id": 2, "name": "Overall", "start_event": 4, "stop_event": 22}],
        "teams": [{"code": 5, "draw": 0, "form": None, "id": 1}],
        "elements": [{"chance_of_playing_next_round": 0.98, "chance_of_playing_this_round": 0.99}],
        "download_time": "2020-09-11 10:24:34.036515",
    }
    raw_data_content = [raw_data_1, raw_data_2]
    raw_data_path = Path(tmp_path) / "2020-fpl-data"  # .joinpath("test_raw_data")
    raw_data_path.mkdir()
    raw_file_paths = [
        raw_data_path.joinpath("test_raw_file_1.json"),
        raw_data_path.joinpath("test_raw_file_2.json"),
    ]
    for raw_file, raw_data in zip(raw_file_paths, raw_data_content):
        with open(raw_file, "w") as outfile:
            json.dump(raw_data, outfile)
    return raw_data_path
