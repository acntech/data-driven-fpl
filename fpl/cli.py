"""Cli module."""
import os

import click

from fpl.data import download_all, json_to_csv

# Load environmental variables if it exist or use default value.
STORAGE_ACCOUNT = os.getenv(
    "STORAGE_ACCOUNT_URL", "https://martinfplstats1337.blob.core.windows.net/"
)


@click.group()
def data():
    """CLI group."""
    print(f"Using storage account {STORAGE_ACCOUNT}")


@data.command(name="download", help="Download all new blobs from container.")
@click.option(
    "--container",
    "-c",
    type=click.STRING,
    help="Name of container to download from",
    default="2021-fpl-data",
)
def download(container):
    """Download all blobs."""
    download_all(STORAGE_ACCOUNT, container)


@data.command(name="to-csv", help="Convert JSON to CSV")
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
    type=click.Choice(["elements", "teams"], case_sensitive=False),
    default="elements",
    help="Transform either elements or teams to CSV",
)
def to_csv(data_dir, entity):
    """Convert to CSV."""
    json_to_csv(data_dir, entity)
