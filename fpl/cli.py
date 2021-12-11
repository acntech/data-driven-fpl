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
def to_parquet():
    """TODO: Implement command line inferface to convert csv to parquet."""
    csv_to_parquet()
