"""Cli module."""
import shutil
import sys
from pathlib import Path

import click

from fpl.data import BlobImporter, DataConverter, csv_to_parquet


@click.group()
def data():
    """CLI group."""


@data.command(name="download", help="Download all new blobs from container.")
def download():
    """Download all blobs."""
    blob_import = BlobImporter()
    blob_import.download_blobs_in_containers()


@data.command(name="csv_on_entity", help="Class to extract desired CSV files")
@click.option(
    "--data-dir",
    "-d",
    type=click.Path(exists=True),
    default="data/raw/2021-fpl-data",
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
    data_converter = DataConverter(data_dir, entity)
    data_converter.convert_json_to_csv_on_entity()


@data.command(name="csv-to-parquet", help="Convert CSV to parquet")
@click.option(
    "--input",
    "-i",
    "input_path",
    type=click.Path(exists=True),
    default="data/interim/2021-fpl-data_elements.csv",
    help="Path to csv file to transform",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    help="Path to parquet dataset root dir",
    default="data/interim/2021_elements_parquet",
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
