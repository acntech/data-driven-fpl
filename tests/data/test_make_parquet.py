"""Test to_parquet."""
import os
from pathlib import Path

import pandas as pd

from fpl.data.make_parquet import to_parquet


def test_to_parquet(tmpdir):
    """Test that parquet creates dataset correctly."""
    print(str(tmpdir))
    parquet_path = Path(str(tmpdir), "test_parquet")
    parquet_path.mkdir()

    to_parquet(
        "test_data/test_interim/test_elements.csv",
        str(tmpdir) + "/test_parquet",
        partition_cols=["code"],
        chunk_size=500,
    )

    # Assert number of partition folders is the same as number of unique id's in dataset.
    assert len(os.listdir(parquet_path)) == 527

    # Assert that there are two chunks as the CSV is read in two chunks.
    assert os.listdir(next(parquet_path.iterdir())) == ["chunk_0_0", "chunk_1_0"]

    # Assert that "code" is found in dataframe and contains 527 unique values
    temp_df = pd.read_parquet(parquet_path)
    assert temp_df["code"].nunique() == 527
