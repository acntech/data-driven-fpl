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
def to_csv():
    """Convert to CSV."""
    # TODO: Add entry to start convertion of json to CSV from command line
    # CLI must support change of source directory and the entities "teams" and "elements"
    print("FILL INN LOGIC!")
