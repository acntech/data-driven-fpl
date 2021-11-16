"""Module for testing DataConverter class."""
import pytest
from pathlib import Path
import pandas as pd

from fpl.data.data_converter_class import DataConverter


class TestDataConverter:
    """Tests for DataConverter class with test data.
    """

    data_dir = "test_data/test_raw"
    main_data_folder = "test_data"
    main_interim_folder = "test_interim"

    def generate_expected_interim_file_path(entity):
        expected_interim_file_name = Path(TestDataConverter.data_dir).name + "_" + entity
        return Path("test_data", "test_interim", expected_interim_file_name).with_suffix(".csv")


    @staticmethod
    def test_convert_json_to_csv_on_elements():
        """Test convertion json to csv on entity."""

        entity = "elements"

        expected_interim_file_path = TestDataConverter.generate_expected_interim_file_path(entity)

        data_converter = DataConverter(TestDataConverter.data_dir, entity, \
            TestDataConverter.main_data_folder, TestDataConverter.main_interim_folder)

        data_converter.convert_json_to_csv_on_entity()

        assert expected_interim_file_path.is_file()

        interim_result_csv_file_df = pd.read_csv(expected_interim_file_path)
        assert not interim_result_csv_file_df.empty

        expected_interim_file_path.unlink()


    @staticmethod
    def test_convert_json_to_csv_on_phases():
        """Test convertion json to csv on entity."""

        entity = "phases"

        expected_interim_file_path = TestDataConverter.generate_expected_interim_file_path(entity)

        data_converter = DataConverter(TestDataConverter.data_dir, entity, \
            TestDataConverter.main_data_folder, TestDataConverter.main_interim_folder)

        data_converter.convert_json_to_csv_on_entity()

        assert expected_interim_file_path.is_file()

        interim_result_csv_file_df = pd.read_csv(expected_interim_file_path)
        assert not interim_result_csv_file_df.empty

        expected_interim_file_path.unlink()


    @staticmethod
    def test_convert_json_to_csv_on_teams():
        """Test convertion json to csv on entity."""

        entity = "teams"

        expected_interim_file_path = TestDataConverter.generate_expected_interim_file_path(entity)

        data_converter = DataConverter(TestDataConverter.data_dir, entity, \
            TestDataConverter.main_data_folder, TestDataConverter.main_interim_folder)

        data_converter.convert_json_to_csv_on_entity()

        assert expected_interim_file_path.is_file()

        interim_result_csv_file_df = pd.read_csv(expected_interim_file_path)
        assert not interim_result_csv_file_df.empty

        expected_interim_file_path.unlink()
