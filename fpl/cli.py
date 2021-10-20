"""Cli module."""
import click

from fpl.data import BlobImporter


@click.group()
def data():
    """CLI group."""
    print("This is the command group of data operations!")


@data.command(name="download", help="Download all new blobs from container.")
def download():
    """Download all blobs."""
    blob_import = BlobImporter()
    blob_import.download_blobs_in_containers()


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
