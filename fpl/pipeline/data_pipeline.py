"""Data pipeline module."""
import numpy as np
import tensorflow as tf

from fpl.data.make_parquet import get_parquet


def get_parquet_dataset(path: str, seq_len: int, num_features: int) -> tf.data.Dataset:
    """Return Dataset from parquet.

    Args:
        path (str): Path to parquet dataset.
        seq_len (int): Number of timesteps.
        num_features (int): Number of features.

    Returns:
        tf.data.Dataset: Dataset.
    """

    def _chunks(lst, n):
        """Yield n-sized chunks from lst."""
        for i in range(0, len(lst)):
            yield lst[i - n : i]

    def _pad_to_length(x, m):
        """Pad chunks to have same number of time steps."""
        return np.pad(x, ((m - x.shape[0], 0), (0, 0)), mode="constant")

    def _ingest_parquet(path: str, seq_len: int) -> tuple:
        """Return generator.

        Args:
            path (str): Path to transformed parquet dataset.
            seq_len (int): Number of time steps.

        Yields:
            Iterator[tuple]: Input data, Labels
        """
        # pylint: disable=unexpected-keyword-arg
        players = get_parquet(path, columns=["code"], print_time=False)["code"].unique().tolist()

        # For each player (element) in dataset
        for player in players:
            dataframe = get_parquet(path, filter=("code", player), print_time=False).sort_values(
                by=["season", "gameweek"]
            )
            # For each chunk in player data yield window.
            for chunk in _chunks(dataframe.loc[:, dataframe.columns != "web_name"], 10):
                x_input = chunk.loc[
                    :,
                    ~chunk.columns.isin(
                        ["team_code", "code", "gameweek", "season", "total_points", "target"]
                    ),
                ].fillna(0.0)
                y_target = chunk[["target"]].fillna(0)
                yield _pad_to_length(x_input, seq_len), _pad_to_length(y_target, seq_len)

    return tf.data.Dataset.from_generator(
        lambda: _ingest_parquet(path, seq_len),
        output_signature=(
            tf.TensorSpec(shape=(seq_len, num_features), dtype=tf.float32, name="input data"),
            tf.TensorSpec(shape=(seq_len, 1), dtype=tf.int32, name="labels"),
        ),
    )
