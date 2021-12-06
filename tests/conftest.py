"""Definitions for global test fixtures."""
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


@pytest.fixture
def elements_df():
    """Return elements DF."""
    return pd.read_csv(INTERIM_ELEMENTS_CSV)


@pytest.fixture
def teams_df():
    """Return teams DF."""
    return pd.read_csv(INTERIM_TEAMS_CSV)


@pytest.fixture
def runner():
    """Return Click CLI runner."""
    return CliRunner()


@pytest.fixture
def tmp_root(tmpdir):
    """Return mock root."""

    class TmpRoot:
        """TmpRoot class."""

        def __init__(self, root):
            """Initialize TmpRoot.

            Args:
                root (str): Path to repo root.
            """
            self.old_root = Path(".").absolute()
            self.root_path = Path(root)
            self.raw_path = None
            self.interim_path = None
            self.processed_path = None

        def __str__(self):
            return str(self.root_path)

        @staticmethod
        def _del(path):
            path = Path(path)
            if path.is_dir():
                shutil.rmtree(path)
            if path.is_file():
                path.unlink()
            return None

        def _get_old_path(self, path):
            return Path(self.old_root, path)

        def set_raw(self, data=True):
            """Set up raw data folder.

            Args:
                data (bool, optional): Add data to raw folder. Defaults to True.
            """
            self.raw_path = self.root_path / "data" / "raw"
            TmpRoot._del(self.raw_path)
            self.raw_path.mkdir(parents=True, exist_ok=True)
            if data:
                for file in self._get_old_path(RAW_DATA_DIR).iterdir():
                    shutil.copy(
                        file,
                        self.raw_path,
                    )

        def set_interim(self, csv=True, parquet=True):
            """Set up interim folder.

            Args:
                csv (bool, optional): Copy csv data files. Defaults to True.
                parquet (bool, optional): Copy Paruqet dataset. Defaults to True.
            """
            self.interim_path = self.root_path / "data" / "interim"
            TmpRoot._del(self.interim_path)
            self.interim_path.mkdir(parents=True, exist_ok=True)
            if csv:
                shutil.copy(
                    str(self._get_old_path(INTERIM_ELEMENTS_CSV)),
                    str(self.interim_path / "2021-fpl-data_elements.csv"),
                )
                shutil.copy(
                    str(self._get_old_path(INTERIM_TEAMS_CSV)),
                    str(self.interim_path / "2021-fpl-data_teams.csv"),
                )

            if parquet:
                shutil.copytree(
                    str(self._get_old_path(INTERIM_PARQUET)),
                    str(self.interim_path / "2021_elements_parquet"),
                    dirs_exist_ok=True,
                )

        def set_processed(self, data=True):
            """Setup processed folder.

            Args:
                data (bool, optional): Copy processed dataset. Defaults to True.
            """
            self.processed_path = self.root_path / "data" / "processed"
            TmpRoot._del(self.processed_path)
            self.processed_path.mkdir(parents=True, exist_ok=True)
            if data:
                pass

        def set_all(self, data=True):
            """Set up all data folders.

            Args:
                data (bool, optional): Copy all data. Defaults to True.
            """
            self.data_path = self.root_path / "data"
            self.set_raw(data=data)
            self.set_interim(csv=data, parquet=data)
            self.set_processed(data=data)

    return TmpRoot(tmpdir)
