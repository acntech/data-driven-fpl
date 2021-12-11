"""Test to_parquet."""
import os
from pathlib import Path

import pyarrow.dataset as ds

from fpl.data.make_parquet import csv_to_parquet, get_parquet


def test_to_parquet(tmpdir):
    """Test that parquet creates dataset correctly."""
    parquet_path = Path(str(tmpdir), "test_parquet")
    parquet_path.mkdir()

    csv_to_parquet(
        "test_data/test_interim/test_elements.csv",
        str(tmpdir) + "/test_parquet",
        partition_columns=["team_code"],
        chunk_size=400,
    )

    # Assert number of partition folders is the same as number of unique id's in dataset.
    assert len(os.listdir(parquet_path)) == 2

    # Assert that there are two chunks as the CSV is read in two chunks.
    assert len(os.listdir(next(parquet_path.iterdir()))) == 3

    # Assert that "code" is found in dataframe and contains 2 unique values
    dataset = ds.dataset(parquet_path, format="parquet", partitioning="hive")
    temp_df = dataset.to_table(columns=["team_code", "minutes"]).to_pandas()

    assert temp_df["team_code"].nunique() == 2


def test_get_parquet():
    """Test get_parquet."""
    df = get_parquet("test_data/test_interim/test_parquet")
    assert len(df) == 2028
    assert len(df.groupby(by=["code", "gameweek"]).last()) == 78

    df = get_parquet("test_data/test_interim/test_parquet", columns=["code", "minutes"])
    assert len(df.columns) == 2

    df = get_parquet("test_data/test_interim/test_parquet", filter=("code", 118748))
    assert len(df) == 1014
