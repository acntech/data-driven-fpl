"""Make parquet."""

import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
from tqdm import tqdm


def to_parquet(path: str, output_path: str, chunk_size=300000, partition_cols=None):
    """Convert CSV to parquet.

    Args:
        path (str): Path to CSV file.
        output_path (str): Path to directory to store parquet dataset.
        chunk_size (int, optional): Number of CSV lines to read at the time. Defaults to 300000.
        partition_cols (list, optional): List of columns to partition dataset on. Defaults to None.
    """
    num_lines = sum([1 for i in open(path)])
    n_chunks = (
        num_lines // chunk_size if num_lines % chunk_size == 0 else num_lines // chunk_size + 1
    )

    for y, chunk in enumerate(tqdm(pd.read_csv(path, chunksize=chunk_size), total=n_chunks)):
        table = pa.Table.from_pandas(chunk)
        ds.write_dataset(
            table,
            output_path,
            basename_template=f"chunk_{y}_{{i}}",
            format="parquet",
            partitioning=partition_cols,
            existing_data_behavior="overwrite_or_ignore",
            partitioning_flavor="hive",
        )


if __name__ == "__main__":
    to_parquet(
        "data/interim/2021-fpl-data_teams.csv",
        "data/interim/2021_teams_parquet",
        partition_cols=["team_code", "code"],
    )
