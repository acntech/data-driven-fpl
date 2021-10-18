"""Cli module."""
import os

import click

from fpl.data import download_all

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
