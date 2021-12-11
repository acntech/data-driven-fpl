"""Cli module."""
import click

from fpl.data import BlobImporter, DataConverter


@click.group()
def data():
    """CLI group."""
    print("This is the command group of data operations!")


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
    default="data/raw/2020-fpl-data",
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
