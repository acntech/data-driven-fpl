"""Test CLI."""
from pathlib import Path, PosixPath

import fpl.data
from fpl.cli import data


class Recorder(object):
    """Recorder class.

    Records whatever is passed to monkeypatch mock.
    """

    called = False
    args = None
    kwargs = None

    @classmethod
    def reset(cls):
        """Reset recorder state."""
        cls.called = False
        cls.args = None
        cls.kwargs = None


def _mock_csv_to_parquet(*args, **kwargs):
    Recorder.called = True
    Recorder.args = args
    Recorder.kwargs = kwargs


def test_to_parquet_no_parquet(runner, monkeypatch, tmp_root):
    """Test CLI where no parquet dataset exist."""
    monkeypatch.setattr(fpl.cli, "csv_to_parquet", _mock_csv_to_parquet)
    tmp_root.set_interim(csv=True, parquet=False)
    monkeypatch.chdir(str(tmp_root))

    # Assert default
    runner.invoke(data, ["csv-to-parquet"])
    assert Recorder.called is True
    assert Recorder.args == (
        "data/interim/2021-fpl-data_elements.csv",
        Path("data/interim/2021_elements_parquet"),
    )
    assert Recorder.kwargs == {"chunk_size": 300000, "partition_columns": ()}
    Recorder.reset()


def test_to_parquet_parquet_exist(runner, monkeypatch, tmp_root):
    """Test CLI where parquet dataset exist in output location."""
    monkeypatch.setattr(fpl.cli, "csv_to_parquet", _mock_csv_to_parquet)
    tmp_root.set_interim(csv=True, parquet=True)
    monkeypatch.chdir(str(tmp_root))

    # Assert default
    runner.invoke(data, ["csv-to-parquet"])
    assert Recorder.called is False
    assert Recorder.args is None
    assert Recorder.kwargs is None
    Recorder.reset()

    # Asserting with force
    runner.invoke(data, ["csv-to-parquet", "--force"])
    assert Recorder.called is True
    assert Recorder.args == (
        "data/interim/2021-fpl-data_elements.csv",
        Path("data/interim/2021_elements_parquet"),
    )
    assert Recorder.kwargs == {"chunk_size": 300000, "partition_columns": ()}
    Recorder.reset()


def test_to_parquet_all_arguments(runner, monkeypatch, tmp_root):
    """Test CLI with all arguments changed."""
    monkeypatch.setattr(fpl.cli, "csv_to_parquet", _mock_csv_to_parquet)
    tmp_root.set_interim(csv=True, parquet=False)
    monkeypatch.chdir(str(tmp_root))

    csv_input_path = f"{str(tmp_root.interim_path)}/2021-fpl-data_teams.csv"

    runner.invoke(
        data,
        [
            "csv-to-parquet",
            "--force",
            "-i" f"{csv_input_path}",
            "-o" "test",
            "-c 1",
            "-p code",
            "-p team_code",
        ],
    )
    assert Recorder.called is True
    assert Recorder.args == (
        csv_input_path,
        PosixPath("test"),
    )
    assert Recorder.kwargs == {"chunk_size": 1, "partition_columns": (" code", " team_code")}
