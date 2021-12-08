"""Make parquet."""

import uuid

import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq
from tqdm import tqdm

from fpl.utils.helpers import timer


@timer
def write_df_to_dataset(
    dataframe: pd.core.frame.DataFrame, output_path: str, partition_columns=None
):
    """Write dataframe to parquet dataset.

    Args:
        df (pd.core.frame.DataFrame): Dataframe to write to dataset.
        output_path (str): Path to dataset root dir.
        partition_columns (list, optional): Columns to partition the dataset on. Defaults to None.
    """
    table = pa.Table.from_pandas(dataframe)
    ds.write_dataset(
        table,
        output_path,
        format="parquet",
        partitioning=partition_columns,
        existing_data_behavior="overwrite_or_ignore",
        partitioning_flavor="hive",
        basename_template=str(f"{uuid.uuid4()}-{{i}}"),
    )


@timer
def csv_to_parquet(path: str, output_path: str, chunk_size=300000, partition_columns=None):
    """Convert CSV to parquet.

    Args:
        path (str): Path to CSV file.
        output_path (str): Path to directory to store parquet dataset.
        chunk_size (int, optional): Number of CSV lines to read at the time. Defaults to 300000.
        partition_columns (list, optional): List of columns to partition dataset on. Defaults to None.
    """
    num_lines = sum([1 for i in open(path)])
    n_chunks = (
        num_lines // chunk_size if num_lines % chunk_size == 0 else num_lines // chunk_size + 1
    )

    for chunk in tqdm(pd.read_csv(path, chunksize=chunk_size), total=n_chunks):
        write_df_to_dataset(chunk, output_path, partition_columns=partition_columns)


@timer
def get_parquet(path: str, columns=None, filter=None):
    """Get dataframe from parquet.

    Args:
        path (str):
        columns (list, optional): Holds name of columns to read out from dataset. Defaults to None.
        filter (tupple, optional): Holds  key, value to filter on. Defaults to None.

    Returns:
        pandas.core.frame.DataFrame: Returns dataset as dataframe
    """
    if filter:
        filter = ds.field(filter[0]) == filter[1]
    dataset = ds.dataset(path, format="parquet", partitioning="hive")
    return dataset.to_table(filter=filter, columns=columns).to_pandas()


if __name__ == "__main__":
    csv_to_parquet(
        "data/interim/2020-fpl-data_teams.csv",
        "data/interim/2020_teams_parquet",
        partition_columns=["code"],
    )
