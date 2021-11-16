"""The main module."""
from fpl import __version__
from fpl.cli import data


def start_script():
    """Demo only."""
    data()
    print(__version__)


if __name__ == "__main__":
    data()
