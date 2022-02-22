"""Cli module."""
import shutil
import sys
from pathlib import Path

import click

from fpl.data import BlobImporter, DataConverter, csv_to_parquet
from fpl.pipeline.experiment import experiment


@click.group(help="The FPL CLI!")
def root():
    """Root cli."""


@click.group(help="Data operation.")
def data():
    """CLI group."""


@data.command(name="download", help="Download all new blobs from container.")
def download():
    """Download all blobs."""
    blob_import = BlobImporter()
    blob_import.download_blobs_in_containers()


@data.command(name="to-csv", help="Convert data dumps to csv")
@click.option(
    "--data-dir",
    "-d",
    type=click.Path(exists=True),
    default="data/raw",
    help="Path to data-dir to transform",
)
@click.option(
    "--entity",
    "-e",
    type=click.Choice(["elements", "teams", "fixtures"], case_sensitive=False),
    default="elements",
    help="Transform elements, phases or teams to CSV",
)
def csv_on_entity(data_dir, entity):
    """Convert to CSV."""
    data_converter = DataConverter(entity=entity, raw_data_path=data_dir)
    data_converter.convert_json_to_csv_on_entity()


@data.command(name="to-parquet", help="Convert CSV to parquet")
@click.option(
    "--input",
    "-i",
    "input_path",
    type=click.Path(exists=True),
    default="data/interim/raw_elements.csv",
    help="Path to csv file to transform",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    help="Path to parquet dataset root dir",
    default="data/interim/elements_parquet",
)
@click.option(
    "--chunk-size", "-c", "chunk_size", help="Number of lines in each chunk to read", default=300000
)
@click.option(
    "--partition",
    "-p",
    "partition_columns",
    help="Pass columns to partition on",
    default=None,
    multiple=True,
)
@click.option("--force", is_flag=True)
def to_parquet(input_path, output_path, chunk_size, partition_columns, force):
    """Convert to Parquet."""
    output_path = Path(output_path)

    if output_path.is_dir() and any(output_path.iterdir()) and not force:
        click.echo(
            click.style(
                "WARNING: Parquet destination is not empty. If you REALLY wanna do this, pass "
                "--force to overwrite. All old data will be lost. \nNow exiting",
                fg="yellow",
                bold=True,
            )
        )
        sys.exit()
    elif force:
        shutil.rmtree(output_path, ignore_errors=True)

    csv_to_parquet(
        input_path, output_path, chunk_size=chunk_size, partition_columns=partition_columns
    )


@click.group(name="pipe", help="Pipeline operations.")
def pipe():
    """Experiment group."""


@pipe.command(name="experiment", help="Run experiment pipeline")
def run_experiment():
    """Experiment entry."""
    experiment()
