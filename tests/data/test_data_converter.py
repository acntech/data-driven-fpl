"""Module for testing DataConverter class."""
from pathlib import Path

import pandas as pd
import pytest

from fpl.data.data_converter import DataConverter


class TestDataConverter:
    """Tests for DataConverter class with test data."""

    @staticmethod
    @pytest.mark.parametrize("entity", ["elements", "phases", "teams"])
    def test_convert_json_to_csv(tmp_path, entity, mock_raw_data_path):
        """Test convertion json to csv on entity."""
        test_interim_data_path = tmp_path.joinpath("test_interim")
        expected_interim_file_path = Path(
            tmp_path, test_interim_data_path.name, mock_raw_data_path.name + "_" + entity
        ).with_suffix(".csv")

        data_converter = DataConverter(
            entity=entity,
            raw_data_path=mock_raw_data_path,
            interim_data_path=test_interim_data_path,
        )

        data_converter.convert_json_to_csv_on_entity()

        assert expected_interim_file_path.is_file()

        interim_result_csv_file_df = pd.read_csv(expected_interim_file_path)
        assert not interim_result_csv_file_df.empty

        expected_interim_file_path.unlink()
